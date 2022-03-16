import pickle
from entities.advogado import Advogado


class AdvogadoDAO:
    def __init__(self, datasource='Advogado.pkl'):
        self.datasource = datasource
        self.object_cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.object_cache, open(self.datasource, 'wb'))

    def __load(self):
        self.object_cache = pickle.load(open(self.datasource, 'rb'))

    def add(self, nome, cpf, senha, logado, cod_OAB):
        if (isinstance(nome, str) and
                isinstance(cpf, str) and
                isinstance(senha, str) and
                isinstance(cod_OAB, str)):
            novo_Advogado = Advogado(nome, cpf, senha, logado, cod_OAB)
            self.object_cache[novo_Advogado.cod_OAB] = novo_Advogado
            self.__dump()
            return True
        return False

    def get(self, key):
        if isinstance(key, str):
            try:
                return self.object_cache[key]
            except KeyError:
                return None

    def remove(self, key):
        if isinstance(key, str):
            try:
                self.object_cache.pop(key)
                self.__dump()
                return True
            except KeyError:
                return False

    def get_all(self):
        return self.object_cache.values()
