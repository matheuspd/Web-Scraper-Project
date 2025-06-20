
class Disciplina:
    def __init__(self, codigo, nome, cred_aula, cred_trab, ch, ce, cp, atpa):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = int(cred_aula)
        self.creditos_trabalho = int(cred_trab)
        self.carga_horaria = int(ch)
        self.carga_estagio = int(ce) if ce else 0
        self.carga_cpcc = int(cp) if cp else 0
        self.carga_atpa = int(atpa) if atpa else 0
        self.requisitos = []

class Curso:
    def __init__(self, nome, unidade, duracao_ideal, duracao_min, duracao_max):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = int(duracao_ideal)
        self.duracao_minima = int(duracao_min)
        self.duracao_maxima = int(duracao_max)
        self.obrigatorias = []
        self.optativas_livres = []
        self.optativas_eletivas = []

class Unidade:
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []
        