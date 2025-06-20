from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Caminho para o chromedriver (ajuste conforme necessário)
#CHROMEDRIVER_PATH = "/usr/bin/chromedriver"  # ou o caminho onde você extraiu o ChromeDriver

# Inicializa o WebDriver
#service = Service(CHROMEDRIVER_PATH)
#options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # descomente para rodar sem abrir a janela

driver = webdriver.Chrome()

# Acessa um site
driver.get("https://www.google.com")

# Aguarda a página carregar
time.sleep(2)

# Interage com a barra de pesquisa
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.submit()

# Aguarda os resultados
time.sleep(3)

# Pega o título da página de resultados
print("Título da página:", driver.title)

# Fecha o navegador
driver.quit()
