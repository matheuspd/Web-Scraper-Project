
from classes import Unidade, Curso, Disciplina
from functions import listar_cursos_por_unidades, consultar_curso, consultar_disciplina
from web_scraping import web_scraping

limite_unidades:int = int(input("Digite o número máximo de unidades a processar: "))

web_scraping(limite_unidades)

# Consulta 1
listar_cursos_por_unidades()

# Consulta 2
consultar_curso("Bacharelado em Biotecnologia (Ciclo Básico) - integral") # por nome
# Consulta 4
consultar_disciplina("ACH0021") # por código


