from entities.usuario import Usuario


class Advogado(Usuario):

    def __init__(self, nome: str, cpf: str, senha: str, logado: bool, cod_OAB: str):
        super().__init__(nome, cpf, senha, logado)
        self.__cod_OAB = cod_OAB
        
    @property
    def cod_OAB(self):
        return self.__cod_OAB
    
    @cod_OAB.setter
    def cod_OAB(self, cod_OAB):
        self.__cod_OAB = cod_OAB


