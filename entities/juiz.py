from entities.usuario import Usuario


class Juiz(Usuario):

    def __init__(self, nome: str, login: str, matricula: int, senha: str):
        super().__init__(nome, login, senha, logado)
        self.__matricula = matricula

    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, matricula: int):
        self.__matricula = matricula

