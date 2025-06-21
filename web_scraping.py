from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

from globals import unidades
from classes import Unidade, Curso, Disciplina

def web_scraping(limite_unidades:int):

    # Setup do navegador
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

    # Espera o carregamento da unidade
    wait.until(EC.presence_of_element_located((By.ID, "comboUnidade")))
    select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))
    opcoes_unidade = select_unidade.options[1:1 + limite_unidades]  # limitar a 3 unidades (por exemplo)

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

    driver.quit()
