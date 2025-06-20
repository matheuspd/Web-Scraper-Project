from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

from classes import Curso, Disciplina, Unidade

limite_unidades = int(input("Digite o número máximo de unidades a processar: "))

# Setup do navegador
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")  # coloque a URL correta

# Espera o carregamento da unidade
wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))
opcoes_unidade = select_unidade.options[1:1 + limite_unidades]  # limitar a 3 unidades (por exemplo)

unidades = []

for unidade_option in opcoes_unidade:
    nome_unidade = unidade_option.text.strip()
    select_unidade.select_by_visible_text(nome_unidade)

    # Aguarda carregar cursos
    wait.until(EC.presence_of_element_located((By.ID, "comboCurso")))
    select_curso = Select(driver.find_element(By.ID, "comboCurso"))
    cursos_opcoes = select_curso.options[1:]  # ignora primeira

    unidade = Unidade(nome_unidade)

    for curso_option in cursos_opcoes:
        select_curso.select_by_visible_text(curso_option.text)
        driver.find_element(By.ID, "enviar").click()
        
        try:
            # Espera ou aba aparecer OU botão "Fechar"
            WebDriverWait(driver, 20).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Fechar']]")),
                    EC.element_to_be_clickable((By.ID, "step2-tab"))                    
                )
            )

            # Tenta localizar popup e clicar em fechar se existir
            botoes_fechar = driver.find_elements(By.XPATH, "//button[span[text()='Fechar']]")
            if botoes_fechar:
                print(f"⚠️ Curso inválido: {curso_option.text}. Pulando.")
                botoes_fechar[0].click()
                wait.until(EC.element_to_be_clickable((By.ID, "comboUnidade")))
                continue  # pula para o próximo curso

        except TimeoutException:
            print(f"❌ Timeout ao processar curso: {curso_option.text}")
            continue  # também pula se nada aparecer

        # Aguarda aba ativa
        wait.until(EC.presence_of_element_located((By.ID, "step2-tab")))
        driver.find_element(By.ID, "step4-tab").click()  # Grade Curricular

        # Espera grade carregar
        wait.until(EC.presence_of_element_located((By.ID, "gradeCurricular")))
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        nome_curso = soup.find('span', class_='curso').text.strip()
        # DEBUGGING
        # print(nome_curso)
        dur_ideal = soup.find('span', class_='duridlhab').text.strip()
        dur_min = soup.find('span', class_='durminhab').text.strip()
        dur_max = soup.find('span', class_='durmaxhab').text.strip()

        curso = Curso(nome_curso, nome_unidade, dur_ideal, dur_min, dur_max)

        grade_div = soup.find('div', id='gradeCurricular')
        if grade_div:
            linhas = grade_div.find_all('tr')
            for tr in linhas:
                tds = tr.find_all('td')
                if len(tds) == 8 and tds[0].find('a'):  # linha de disciplina
                    codigo = tds[0].text.strip()
                    nome = tds[1].text.strip()
                    cred_aula = tds[2].text.strip()
                    cred_trab = tds[3].text.strip()
                    ch = tds[4].text.strip()
                    ce = tds[5].text.strip()
                    cp = tds[6].text.strip()
                    atpa = tds[7].text.strip()
                    disc = Disciplina(codigo, nome, cred_aula, cred_trab, ch, ce, cp, atpa)
                    # SEPARAR DISCIPLINAS OBRIGATORIAS, ELETIVAS E LIVRES
                    curso.obrigatorias.append(disc)
                    # VER TAMBEM REQUISITOS

        unidade.cursos.append(curso)
        driver.find_element(By.ID, "step1-tab").click()
        wait.until(EC.element_to_be_clickable((By.ID, "comboUnidade")))

    unidades.append(unidade)

def listar_cursos_por_unidades(unidades):
    for unidade in unidades:
        print(f"\n📍 Unidade: {unidade.nome}")
        if not unidade.cursos:
            print("  (Sem cursos encontrados)")
        else:
            for curso in unidade.cursos:
                print(f"  - {curso.nome}")

def consultar_curso(unidades, nome_curso):
    for unidade in unidades:
        for curso in unidade.cursos:
            if curso.nome.lower() == nome_curso.lower():
                print(f"\n🎓 Curso: {curso.nome}")
                print(f"🏫 Unidade: {curso.unidade}")
                print(f"📚 Duração ideal: {curso.duracao_ideal} semestres")
                print(f"📉 Duração mínima: {curso.duracao_minima} semestres")
                print(f"📈 Duração máxima: {curso.duracao_maxima} semestres")

                # MUDAR PRINT PARA CARGA HORARIA ESTAGIO E OUTRAS 2
                print("\n📘 Disciplinas obrigatórias:")
                for d in curso.obrigatorias:
                    print(f"XXX - {d.codigo} | {d.nome} | {d.creditos_aula}A/{d.creditos_trabalho}T | CH: {d.carga_horaria}")
                
                print("\n📘 Disciplinas optativas eletivas:")
                for d in curso.optativas_eletivas:
                    print(f"YYY - {d.codigo} | {d.nome} | {d.creditos_aula}A/{d.creditos_trabalho}T | CH: {d.carga_horaria}")
                
                print("\n📘 Disciplinas optativas livres:")
                for d in curso.optativas_livres:
                    print(f"ZZZ - {d.codigo} | {d.nome} | {d.creditos_aula}A/{d.creditos_trabalho}T | CH: {d.carga_horaria}")

                return curso
    print(f"⚠️ Curso '{nome_curso}' não encontrado.")
    return None

def consultar_disciplina(unidades, codigo_busca):
    codigo_busca = codigo_busca.strip().lower()
    cursos_que_possuem = []
    disciplina_encontrada = None

    for unidade in unidades:
        for curso in unidade.cursos:
            for d in curso.obrigatorias:
                if d.codigo.lower() == codigo_busca:
                    if not disciplina_encontrada:
                        disciplina_encontrada = d
                    cursos_que_possuem.append((curso.nome, unidade.nome))

    if not disciplina_encontrada:
        print(f"⚠️ Nenhuma disciplina encontrada com o código '{codigo_busca}'.")
        return

    d = disciplina_encontrada
    print(f"\n📖 Disciplina: {d.nome} ({d.codigo})")
    print(f"📘 Créditos: {d.creditos_aula}A / {d.creditos_trabalho}T")
    print(f"⏱️ CH: {d.carga_horaria}, Estágio: {d.carga_estagio}, CPCC: {d.carga_cpcc}, ATPA: {d.carga_atpa}")

    print("\n📚 Presente nos cursos:")
    for curso_nome, unidade_nome in cursos_que_possuem:
        print(f" - {curso_nome} ({unidade_nome})")

# Consulta 1
listar_cursos_por_unidades(unidades)

# Consulta 2
consultar_curso(unidades, "Bacharelado em Biotecnologia (Ciclo Básico) - integral") # por nome
# Consulta 4
consultar_disciplina(unidades, "ACH0021") # por código

driver.quit()
