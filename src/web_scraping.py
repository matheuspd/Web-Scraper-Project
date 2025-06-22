from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import List
from classes import Unidade, Curso, Disciplina


def web_scraping(limite_unidades: int) -> List[Unidade]:
    """
    Realiza web scraping no site JúpiterWeb da USP para coletar dados das unidades, cursos e disciplinas.
    Args:
        limite_unidades (int): Número máximo de unidades a serem processadas.
    Returns:
        List[Unidade]: Lista de objetos Unidade contendo os cursos e disciplinas associadas.
    """

    # Inicializa o navegador Chrome e define tempo de espera máximo
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

    # Aguarda o carregamento das opções de unidade no dropdown
    wait.until(lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1)
    select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))
    opcoes_unidade = select_unidade.options[1:]  # Remove a primeira opção vazia/padrão
    total_disponivel = len(opcoes_unidade)

    # Validação do limite
    if limite_unidades > total_disponivel:
        print(f"⚠️ Aviso: Apenas {total_disponivel} unidades estão disponíveis. Ajustando o limite para o total de unidades.")
        limite_unidades = total_disponivel

    # Seleciona apenas as unidades até o limite
    opcoes_unidade = opcoes_unidade[:limite_unidades]

    unidades:List[Unidade] = []

    # Itera sobre as unidades selecionadas
    for unidade_option in opcoes_unidade:
        nome_unidade = unidade_option.text.strip()
        select_unidade.select_by_visible_text(nome_unidade)

        # Aguarda carregamento dos cursos
        wait.until(lambda d: len(Select(d.find_element(By.ID, "comboCurso")).options) > 1)
        select_curso = Select(driver.find_element(By.ID, "comboCurso"))
        cursos_opcoes = select_curso.options[1:]  # ignora a primeira opção "Selecione"

        unidade = Unidade(nome_unidade)

        # Itera sobre os cursos da unidade
        for curso_option in cursos_opcoes:
            select_curso.select_by_visible_text(curso_option.text)
            driver.find_element(By.ID, "enviar").click()

            try:
                # Aguarda o desaparecimento do popup "Aguarde"
                WebDriverWait(driver, 20).until_not(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
                )

                # Fecha o popup "Curso inválido" se aparecer
                botao_fechar = driver.find_elements(By.XPATH, "//button[span[text()='Fechar']]")
                if botao_fechar:
                    print(f"⚠️ Curso inválido: {curso_option.text}. Pulando.")
                    botao_fechar[0].click()
                    wait.until(EC.element_to_be_clickable((By.ID, "comboCurso")))
                    continue

            except TimeoutException:
                print(f"❌ Timeout ao processar curso: {curso_option.text}")
                continue

            # Aguarda o desaparecimento do popup "Aguarde" e acessa aba "Grade Curricular"
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
            )
            driver.find_element(By.ID, "step4-tab").click()

            # Aguarda o carregamento da grade curricular
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
            )

            # Faz o parser do HTML
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extrai informações do curso
            nome_curso = soup.find('span', class_='curso').text.strip()
            dur_ideal = soup.find('span', class_='duridlhab').text.strip()
            dur_min = soup.find('span', class_='durminhab').text.strip()
            dur_max = soup.find('span', class_='durmaxhab').text.strip()
            curso = Curso(nome_curso, nome_unidade, dur_ideal, dur_min, dur_max)

            grade_div = soup.find('div', id='gradeCurricular')
            if grade_div:
                linhas = grade_div.find_all('tr')
                categoria_atual = 0  # 0: obrigatória, 1: eletiva, 2: livre

                for tr in linhas:
                    tds = tr.find_all('td')

                    # Atualiza categoria de disciplina com base em título da seção
                    if len(tds) == 1:
                        texto = tds[0].text.strip().lower()
                        if "obrigatórias" in texto:
                            categoria_atual = 0
                        elif "optativas eletivas" in texto:
                            categoria_atual = 1
                        elif "optativas livres" in texto:
                            categoria_atual = 2
                        continue  # pula para próxima linha

                    # Linha contendo disciplina (espera 8 colunas e link no código)
                    if len(tds) == 8 and tds[0].find('a'):
                        codigo = tds[0].text.strip()
                        nome = tds[1].text.strip()
                        cred_aula = tds[2].text.strip()
                        cred_trab = tds[3].text.strip()
                        ch = tds[4].text.strip()
                        ce = tds[5].text.strip()
                        cp = tds[6].text.strip()
                        atpa = tds[7].text.strip()

                        # Cria a disciplina e adiciona à lista correspondente
                        disc = Disciplina(codigo, nome, cred_aula, cred_trab, ch, ce, cp, atpa)
                        if categoria_atual == 0:
                            curso.obrigatorias.append(disc)
                        elif categoria_atual == 1:
                            curso.optativas_eletivas.append(disc)
                        elif categoria_atual == 2:
                            curso.optativas_livres.append(disc)

            # Retorna para aba de seleção de curso
            unidade.cursos.append(curso)
            driver.find_element(By.ID, "step1-tab").click()
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
            )
            wait.until(EC.element_to_be_clickable((By.ID, "comboUnidade")))

        # Adiciona unidade completa à lista final
        unidades.append(unidade)

    # Encerra o navegador e retorna os dados extraídos
    driver.quit()
    return unidades