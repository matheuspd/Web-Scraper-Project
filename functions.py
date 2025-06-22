from typing import List, Optional
from classes import Unidade, Curso, Disciplina
from collections import defaultdict
from rich.console import Console
from rich.table import Table

console = Console()

def listar_cursos_por_unidades(unidades: List[Unidade]) -> None:
    for unidade in unidades:
        table = Table(title=f"📍 Unidade: {unidade.nome}", style="bold #57a8ff")
        table.add_column("Cursos", style="cyan")
        if not unidade.cursos:
            table.add_row("(Sem cursos encontrados)")
        else:
            for curso in unidade.cursos:
                table.add_row(curso.nome)
        console.print(table)
        print()

def consultar_curso(unidades: List[Unidade], nome_curso: str) -> Optional[Curso]:
    for unidade in unidades:
        for curso in unidade.cursos:
            if curso.nome.lower() == nome_curso.lower():
                console.print(f"\n🎓 Curso: {curso.nome}", style="bold #57a8ff")
                console.print(f"🏫 Unidade: {curso.unidade}", style="bold #57a8ff")
                console.print(
                    f"📚 Duração: ideal {curso.duracao_ideal} / "
                    f"mínima {curso.duracao_minima} / máxima {curso.duracao_maxima} semestres",
                    style="bold #57a8ff"
                )

                def _print_table(title: str, disciplinas: List[Disciplina]) -> None:
                    table = Table(title=title, style="bright_blue")
                    table.add_column("Código", style="cyan", no_wrap=True)
                    table.add_column("Nome", style="magenta")
                    table.add_column("A/T", justify="center", style="green")
                    table.add_column("CH", justify="right")
                    table.add_column("CE", justify="right")
                    table.add_column("CP", justify="right")
                    table.add_column("ATPA", justify="right")
                    for d in disciplinas:
                        table.add_row(
                            d.codigo,
                            d.nome,
                            f"{d.creditos_aula}A/{d.creditos_trabalho}T",
                            str(d.carga_horaria),
                            str(d.carga_estagio),
                            str(d.carga_cpcc),
                            str(d.carga_atpa)
                        )
                    console.print(table)

                print()
                _print_table("📘 Disciplinas Obrigatórias", curso.obrigatorias)
                print()
                _print_table("📘 Disciplinas Optativas Eletivas", curso.optativas_eletivas)
                print()
                _print_table("📘 Disciplinas Optativas Livres", curso.optativas_livres)

                return curso

    console.print(f"⚠️ Curso '{nome_curso}' não encontrado.", style="bold red")
    return None

def consultar_todos_os_cursos(unidades: List[Unidade]):
    for unidade in unidades:
        for curso in unidade.cursos:
            consultar_curso(unidades, curso.nome)

def consultar_disciplina(unidades: List[Unidade], codigo_busca: str) -> Optional[Disciplina]:
    codigo = codigo_busca.strip().lower()
    cursos_que_possuem: List[tuple[str, str]] = []
    disciplina_encontrada: Optional[Disciplina] = None

    for unidade in unidades:
        for curso in unidade.cursos:
            for d in curso.obrigatorias:
                if d.codigo.lower() == codigo:
                    if not disciplina_encontrada:
                        disciplina_encontrada = d
                    cursos_que_possuem.append((curso.nome, unidade.nome))

    if not disciplina_encontrada:
        console.print(f"⚠️ Nenhuma disciplina encontrada com o código '{codigo_busca}'.", style="bold red")
        return None

    d = disciplina_encontrada
    console.print(f"\n📖 Disciplina: {d.nome} ({d.codigo})", style="bold #57a8ff")
    print()

    details = Table(show_header=False, style="bright_blue")
    details.add_column("Campo", style="cyan")
    details.add_column("Valor", style="magenta")
    details.add_row("Créditos Aula/Trabalho", f"{d.creditos_aula}A/{d.creditos_trabalho}T")
    details.add_row("Carga Horária", str(d.carga_horaria))
    details.add_row("Estágio", str(d.carga_estagio))
    details.add_row("CPCC", str(d.carga_cpcc))
    details.add_row("ATPA", str(d.carga_atpa))
    console.print(details)
    print()

    table_cursos = Table(title="📚 Presente nos cursos", style="bold #57a8ff")
    table_cursos.add_column("Curso", style="magenta")
    table_cursos.add_column("Unidade", style="cyan")
    for nome_curso, nome_unidade in cursos_que_possuem:
        table_cursos.add_row(nome_curso, nome_unidade)
    console.print(table_cursos)

    return disciplina_encontrada


def consultar_disciplinas_em_varios_cursos(unidades: List[Unidade]) -> None:
    mapa_disciplinas = defaultdict(list)  # chave: código, valor: lista de (nome, curso, unidade, tipo)

    for unidade in unidades:
        for curso in unidade.cursos:
            for d in curso.obrigatorias:
                mapa_disciplinas[d.codigo.lower()].append((d.nome, curso.nome, unidade.nome, "Obrigatória"))
            for d in curso.optativas_eletivas:
                mapa_disciplinas[d.codigo.lower()].append((d.nome, curso.nome, unidade.nome, "Optativa Eletiva"))
            for d in curso.optativas_livres:
                mapa_disciplinas[d.codigo.lower()].append((d.nome, curso.nome, unidade.nome, "Optativa Livre"))

    # Filtra apenas disciplinas que ocorrem em mais de um curso
    disciplinas_repetidas = {cod: infos for cod, infos in mapa_disciplinas.items() if len(infos) > 1}

    if not disciplinas_repetidas:
        console.print("⚠️ Nenhuma disciplina encontrada em mais de um curso.", style="bold red")
        return

    for codigo, ocorrencias in disciplinas_repetidas.items():
        nome = ocorrencias[0][0]
        title = f"📖 {nome} ({codigo.upper()}) aparece em {len(ocorrencias)} cursos"
        table = Table(title=title, style="bold #57a8ff")
        table.add_column("Curso", style="magenta")
        table.add_column("Unidade", style="cyan")
        table.add_column("Tipo", style="green")
        for _, curso, unidade, tipo in ocorrencias:
            table.add_row(curso, unidade, tipo)
        console.print(table)
        print()