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
    """
    Função principal do programa.
    Executa o processo de:
    - Coleta de dados via web scraping do site JúpiterWeb.
    - Exibição de um menu interativo para consultar dados de unidades, cursos e disciplinas.
    """

    # Número máximo de unidades a processar
    while True:
        try:
            limite_unidades = int(console.input("[bold #57a8ff]Digite o número máximo de unidades a processar: "))
            if limite_unidades < 1:
                console.print("❌ O número deve ser maior que zero.", style="bold red")
                continue
            break
        except ValueError:
            console.print("❌ Entrada inválida. Digite um número inteiro.", style="bold red")

    # Inicia o processo de web scraping e armazena o resultado na lista de unidades
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
            # Finaliza o programa
            console.print("Até a próxima! 👋", style="bold #cc0000")
            break

        elif(option == "1"):
            # Lista os cursos por unidade
            listar_cursos_por_unidades(unidades)

        elif(option == "2"):
            # Solicita ao usuário o nome do curso para consulta
            curso:str = console.input("[bold #57a8ff]Digite o curso que deseja consultar:\n").strip()
            # Exemplo: "Bacharelado em Lazer e Turismo (Ciclo Básico) - vespertino"
            consultar_curso(unidades, curso)

        elif(option == "3"):
            # Exibe dados de todos os cursos disponíveis
            consultar_todos_os_cursos(unidades)

        elif(option == "4"):
            # Solicita ao usuário o código da disciplina
            disciplina:str = console.input("[bold #57a8ff]Digite o código da disciplina que deseja consultar (Exemplo: ACH0021):\n").strip()
            # Exemplo: "ACH0021"
            consultar_disciplina(unidades, disciplina)

        elif(option == "5"):
            # Mostra disciplinas que aparecem em mais de um curso
            consultar_disciplinas_em_varios_cursos(unidades)

        else:
            # Opção inválida
            console.print("Opção inválida. Tente novamente.", style="bold #cc0000")

        console.input("[bold #57a8ff]Pressione Enter para continuar...[/]")

if __name__ == "__main__":
    main()