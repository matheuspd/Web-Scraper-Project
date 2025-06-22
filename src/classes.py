from typing import List

class Disciplina:
    """
    Representa uma disciplina com seus atributos principais.
    Atributos:
        codigo (str): Código identificador da disciplina.
        nome (str): Nome da disciplina.
        creditos_aula (int): Créditos relacionados a aulas teóricas.
        creditos_trabalho (int): Créditos relacionados a trabalhos.
        carga_horaria (int): Carga horária total da disciplina.
        carga_estagio (int): Carga horária de estágio.
        carga_cpcc (int): Carga horária de atividades Práticas como Componentes Curriculares.
        carga_atpa (int): Carga horária de atividades Teórico-Práticas de Aprofundamento.
    """
    def __init__(self, codigo, nome, cred_aula, cred_trab, ch, ce, cp, atpa):
        self.codigo: str = codigo
        self.nome: str = nome
        self.creditos_aula: int = int(cred_aula)
        self.creditos_trabalho: int = int(cred_trab)
        self.carga_horaria: int = int(ch)
        self.carga_estagio: int = int(ce) if ce else 0
        self.carga_cpcc: int = int(cp) if cp else 0
        self.carga_atpa: int = int(atpa) if atpa else 0

class Curso:
    """
    Representa um curso de graduação de uma unidade da USP.
    Atributos:
        nome (str): Nome completo do curso.
        unidade (str): Nome da unidade responsável pelo curso.
        duracao_ideal (int): Duração ideal do curso em semestres.
        duracao_minima (int): Duração mínima possível do curso.
        duracao_maxima (int): Duração máxima permitida do curso.
        obrigatorias (List[Disciplina]): Lista de disciplinas obrigatórias.
        optativas_livres (List[Disciplina]): Lista de disciplinas optativas livres.
        optativas_eletivas (List[Disciplina]): Lista de disciplinas optativas eletivas.
    """
    def __init__(self, nome, unidade, duracao_ideal, duracao_min, duracao_max):
        self.nome: str = nome
        self.unidade: str = unidade
        self.duracao_ideal: int = int(duracao_ideal)
        self.duracao_minima: int = int(duracao_min)
        self.duracao_maxima: int = int(duracao_max)
        self.obrigatorias: List[Disciplina] = []
        self.optativas_livres: List[Disciplina] = []
        self.optativas_eletivas: List[Disciplina] = []

class Unidade:
    """
    Representa uma unidade da USP (ex: EEL, EACH, FFLCH).
    Atributos:
        nome (str): Nome da unidade.
        cursos (List[Curso]): Lista de cursos ofertados pela unidade.
    """
    def __init__(self, nome):
        self.nome: str = nome
        self.cursos: List[Curso] = []
