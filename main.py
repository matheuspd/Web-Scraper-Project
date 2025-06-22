from functions import (
    listar_cursos_por_unidades,
    consultar_curso,
    consultar_disciplina,
    consultar_todos_os_cursos,
    consultar_disciplinas_em_varios_cursos
)
from web_scraping import web_scraping
from rich.console import Console
from typing import List
from classes import Unidade

console = Console()

def main():

    # Número máximo de unidades a processar
    limite_unidades = int(console.input("[bold #57a8ff]Digite o número máximo de unidades a processar: "))

    # Inicia o processo de web scraping
    unidades:List[Unidade] = web_scraping(limite_unidades)

    # Entrada do usuário para consultas
    while True:
        console.print("Digite o número correspondente a pesquisa que deseja realizar:", style="bold #57a8ff")
        console.print("1. Listar cursos por unidades")
        console.print("2. Dados de um determinado curso")
        console.print("3. Dados de todos os cursos")
        console.print("4. Dados de uma disciplina, inclusive quais cursos ela faz parte")
        console.print("5. Disciplinas que são usadas em mais de um curso")
        console.print("0. Sair")
        option:str = input().strip()
        
        if(option == "0"):
            console.print("Até a próxima! 👋", style="bold #cc0000")
            break
        elif(option == "1"):
            listar_cursos_por_unidades(unidades)
        elif(option == "2"):
            # Exemplo: "Bacharelado em Lazer e Turismo (Ciclo Básico) - vespertino"
            curso:str = console.input("[bold #57a8ff]Digite o curso que deseja consultar:\n").strip()
            consultar_curso(unidades, curso)
        elif(option == "3"):
            consultar_todos_os_cursos(unidades)
        elif(option == "4"):
            # Exemplo: "ACH0021"
            disciplina:str = console.input("[bold #57a8ff]Digite o código da disciplina que deseja consultar:\n").strip()
            consultar_disciplina(unidades, disciplina)
        elif(option == "5"):
            consultar_disciplinas_em_varios_cursos(unidades)
        else:
            console.print("Opção inválida. Tente novamente.", style="bold #cc0000")

        console.input("[bold #57a8ff]Pressione Enter para continuar...[/]")

if __name__ == "__main__":
    main()