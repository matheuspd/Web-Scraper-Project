from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from typing import List
from classes import Unidade, Curso, Disciplina

def web_scraping(limite_unidades:int) -> List[Unidade]:

    # Setup do navegador
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

    # Espera o carregamento da unidade
    wait.until(lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1)
    select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))
    opcoes_unidade = select_unidade.options[1:1 + limite_unidades]  # limitar a 3 unidades (por exemplo)

    unidades:List[Unidade] = []

    for unidade_option in opcoes_unidade:
        nome_unidade = unidade_option.text.strip()
        select_unidade.select_by_visible_text(nome_unidade)

        # Aguarda carregar cursos
        wait.until(lambda d: len(Select(d.find_element(By.ID, "comboCurso")).options) > 1)
        select_curso = Select(driver.find_element(By.ID, "comboCurso"))
        cursos_opcoes = select_curso.options[1:]  # ignora primeira

        unidade = Unidade(nome_unidade)

        for curso_option in cursos_opcoes:
            select_curso.select_by_visible_text(curso_option.text)
            driver.find_element(By.ID, "enviar").click()
            
            try:
                # Espera ou aba aparecer OU botão "Fechar" após popup de "Aguarde" fechar
                WebDriverWait(driver, 20).until_not(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
                )

                # Tenta localizar popup e clicar em fechar se existir
                botoes_fechar = driver.find_elements(By.XPATH, "//button[span[text()='Fechar']]")
                if botoes_fechar:
                    print(f"⚠️ Curso inválido: {curso_option.text}. Pulando.")
                    botoes_fechar[0].click()
                    wait.until(EC.element_to_be_clickable((By.ID, "comboCurso")))
                    continue  # pula para o próximo curso

            except TimeoutException:
                print(f"❌ Timeout ao processar curso: {curso_option.text}")
                continue  # também pula se nada aparecer

            # Aguarda aba ativa
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
            )
            driver.find_element(By.ID, "step4-tab").click()  # Grade Curricular

            # Espera grade carregar
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            nome_curso = soup.find('span', class_='curso').text.strip()
            dur_ideal = soup.find('span', class_='duridlhab').text.strip()
            dur_min = soup.find('span', class_='durminhab').text.strip()
            dur_max = soup.find('span', class_='durmaxhab').text.strip()

            curso = Curso(nome_curso, nome_unidade, dur_ideal, dur_min, dur_max)

            grade_div = soup.find('div', id='gradeCurricular')
            if grade_div:
                linhas = grade_div.find_all('tr')
                categoria_atual = 0  # obrigatoria: 0, eletiva: 1 e livre: 2
                for tr in linhas:
                    tds = tr.find_all('td')

                    # Detecta categoria pela presença de texto em apenas 1 coluna
                    if len(tds) == 1:
                        texto = tds[0].text.strip().lower()
                        if "obrigatórias" in texto:
                            categoria_atual = 0
                        elif "optativas eletivas" in texto:
                            categoria_atual = 1
                        elif "optativas livres" in texto:
                            categoria_atual = 2 
                        continue  # pula linha de título

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
                        if categoria_atual == 0:
                            curso.obrigatorias.append(disc)
                        elif categoria_atual == 1:
                            curso.optativas_eletivas.append(disc)
                        elif categoria_atual == 2:
                            curso.optativas_livres.append(disc)
                        # VER TAMBEM REQUISITOS

            unidade.cursos.append(curso)
            driver.find_element(By.ID, "step1-tab").click()
            WebDriverWait(driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde')]"))
            )
            wait.until(EC.element_to_be_clickable((By.ID, "comboUnidade")))

        unidades.append(unidade)

    driver.quit()
    return unidades
