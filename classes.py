
from typing import List, Optional, Union

class Disciplina:
    def __init__(self, codigo, nome, cred_aula, cred_trab, ch, ce, cp, atpa):
        self.codigo:str = codigo
        self.nome:str = nome
        self.creditos_aula:int = int(cred_aula)
        self.creditos_trabalho:int = int(cred_trab)
        self.carga_horaria:int = int(ch)
        self.carga_estagio:int = int(ce) if ce else 0
        self.carga_cpcc:int = int(cp) if cp else 0
        self.carga_atpa:int = int(atpa) if atpa else 0
        self.requisitos:List[str] = []

class Curso:
    def __init__(self, nome, unidade, duracao_ideal, duracao_min, duracao_max):
        self.nome:str = nome
        self.unidade:Unidade = unidade
        self.duracao_ideal:int = int(duracao_ideal)
        self.duracao_minima:int = int(duracao_min)
        self.duracao_maxima:int = int(duracao_max)
        self.obrigatorias:List[Disciplina] = []
        self.optativas_livres:List[Disciplina] = []
        self.optativas_eletivas:List[Disciplina] = []

class Unidade:
    def __init__(self, nome):
        self.nome:str = nome
        self.cursos:List[Curso] = []