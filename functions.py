from typing import List
from classes import Unidade
from collections import defaultdict

def listar_cursos_por_unidades(unidades:List[Unidade]):
    for unidade in unidades:
        print(f"\n📍 Unidade: {unidade.nome}")
        if not unidade.cursos:
            print("  (Sem cursos encontrados)")
        else:
            for curso in unidade.cursos:
                print(f"  - {curso.nome}")


def consultar_curso(unidades:List[Unidade], nome_curso:str):
    for unidade in unidades:
        for curso in unidade.cursos:
            if curso.nome.lower() == nome_curso.lower():
                print(f"\n🎓 Curso: {curso.nome}")
                print(f"🏫 Unidade: {curso.unidade}")
                print(f"📚 Duração ideal: {curso.duracao_ideal} semestres")
                print(f"📉 Duração mínima: {curso.duracao_minima} semestres")
                print(f"📈 Duração máxima: {curso.duracao_maxima} semestres")

                print("\n📘 Disciplinas obrigatórias:")
                for d in curso.obrigatorias:
                    print(f"{d.codigo} | {d.nome} | {d.creditos_aula}A/{d.creditos_trabalho}T | CH: {d.carga_horaria} | CE: {d.carga_estagio} | CP: {d.carga_cpcc} | ATPA: {d.carga_atpa}")
                
                print("\n📘 Disciplinas optativas eletivas:")
                for d in curso.optativas_eletivas:
                    print(f"{d.codigo} | {d.nome} | {d.creditos_aula}A/{d.creditos_trabalho}T | CH: {d.carga_horaria} | CE: {d.carga_estagio} | CP: {d.carga_cpcc} | ATPA: {d.carga_atpa}")
                
                print("\n📘 Disciplinas optativas livres:")
                for d in curso.optativas_livres:
                    print(f"{d.codigo} | {d.nome} | {d.creditos_aula}A/{d.creditos_trabalho}T | CH: {d.carga_horaria} | CE: {d.carga_estagio} | CP: {d.carga_cpcc} | ATPA: {d.carga_atpa}")

                return curso
    print(f"⚠️ Curso '{nome_curso}' não encontrado.")
    return None

def consultar_todos_os_cursos(unidades: List[Unidade]):
    for unidade in unidades:
        for curso in unidade.cursos:
            consultar_curso(unidades, curso.nome)

def consultar_disciplina(unidades:List[Unidade], codigo_busca:str):
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


def consultar_disciplinas_em_varios_cursos(unidades: List[Unidade]):
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
        print("⚠️ Nenhuma disciplina encontrada em mais de um curso.")
        return

    for codigo, ocorrencias in disciplinas_repetidas.items():
        nome = ocorrencias[0][0]
        print(f"\n📖 Disciplina: {nome} ({codigo.upper()}) aparece em {len(ocorrencias)} cursos:")
        for _, curso, unidade, tipo in ocorrencias:
            print(f" - {curso} ({unidade}) [{tipo}]")
