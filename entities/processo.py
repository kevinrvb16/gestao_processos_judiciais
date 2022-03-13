class Processo:

    def __init__(self, codOAB_advogado_autor: int, autor: str,  id_processo: int, reu: str,  juiz: int):
        self.__anexos = []
        self.__autor = autor
        self.__codOAB_advogado_autor = codOAB_advogado_autor
        self.__codOAB_advogado_reu = -1
        self.__data = []
        self.__eh_sigiloso = False
        self.__eh_urgente = False
        self.__id_processo = id_processo
        self.__juiz = juiz
        self.__reu = reu

    def get_anexos(self):
        return self.__anexos

    def set_anexos(self, anexos):
        self.__anexos.append(anexos)

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, autor):
        self.__autor = autor

    @property
    def codOAB_advogado_autor(self):
        return self.__codOAB_advogado_autor

    @codOAB_advogado_autor.setter
    def codOAB_advogado_autor(self, codOAB_advogado_autor):
        self.__codOAB_advogado_autor = codOAB_advogado_autor

    @property
    def codOAB_advogado_reu(self):
        return self.__codOAB_advogado_reu

    @codOAB_advogado_reu.setter
    def codOAB_advogado_reu(self, codOAB_advogado_reu):
        self.__codOAB_advogado_reu = codOAB_advogado_reu

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data.append(data)

    def get_eh_sigiloso(self):
        return self.__eh_sigiloso

    def set_eh_sigiloso(self, eh_sigiloso):
        self.__eh_sigiloso = eh_sigiloso

    def get_eh_urgente(self):
        return self.__eh_urgente

    def set_eh_urgente(self, eh_urgente):
        self.__eh_urgente = eh_urgente

    @property
    def id_processo(self):
        return self.__id_processo

    @id_processo.setter
    def id_processo(self, id_processo):
        self.__id_processo = id_processo

    @property
    def juiz(self):
        return self.__juiz

    @juiz.setter
    def juiz(self, juiz):
        self.__juiz = juiz

    @property
    def reu(self):
        return self.__reu

    @reu.setter
    def reu(self, reu):
        self.__reu = reu





    
