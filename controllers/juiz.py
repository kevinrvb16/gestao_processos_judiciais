from interface.juiz import InterfaceJuiz
from arquivos.juizDAO import JuizDAO
from controllers.validadorCPF import ValidadorCPF
import hashlib
import random


class JuizController:
    
    def __init__(self, controlador_execucao):
        self.__interface_juiz = InterfaceJuiz(self)
        self.__juiz_dao = JuizDAO()
        self.__controlador_execucao = controlador_execucao
    
    @property
    def juiz_dao(self):
        return self.__juiz_dao

    def cadastrar_juiz(self):
        while True:
            cpf = ValidadorCPF().solicita_cpf_cadastro()
            if cpf is None:
                break
            existe_cpf = self.verifica_cpf_jah_existente(cpf)
            if existe_cpf:
                self.__interface_juiz.aviso('\nCPF já foi cadastrado!')
                continue
            while True:
                try:
                    valores = self.__interface_juiz.tela_cadastrar_juiz(cpf)
                    cadastro_ok = self.verifica_cadastro_completo(valores)
                except TypeError:
                    break
                if not cadastro_ok:
                    self.__interface_juiz.aviso('\nCampo(s) obrigatórios não preenchidos')
                    continue
                senha = valores['password']
                # try:
                #     senha_utf = senha.encode('utf-8')
                #     sha1hash = hashlib.sha1()
                #     sha1hash.update(senha_utf)
                #     senha_hash = sha1hash.hexdigest()
                # except Exception:
                #     self.__tela_login.aviso('Erro ao gerar senha')
                #     break
                sucesso_add = self.__juiz_dao.add(valores['nome'],
                                                           cpf,
                                                           valores['matricula'],
                                                           senha)
                print(valores['nome'], cpf, valores['matricula'], senha)

                if not sucesso_add:
                    self.__interface_juiz.aviso('Erro no cadastro')
                break
            break
        
    def sortear_juiz(self):
        lista_juizes = self.__juiz_dao.get_all()
        lista_cpf = []
        for juiz in lista_juizes:
            lista_cpf.append(juiz.cpf)
        return random.choice(lista_cpf)

    def verifica_cpf_jah_existente(self, cpf):
        verificacao = self.__juiz_dao.get(cpf)
        if verificacao is None:
            return False
        return True
    
    def verifica_cadastro_completo(self, values):
        if values['nome'] == '' or values['password'] == '':
            self.__interface_juiz.close_tela_principal()
            return False
        return True


    def listar_juiz(self):
        dic_nome_num_juizes = {}
        lista_juizes = self.__juiz_dao.get_all()
        for juiz in lista_juizes:
            dic_nome_num_juizes[juiz.nome] = juiz.cpf
        self.__interface_juiz.mostrar_lista(dic_nome_num_juizes)


    def get_nome_juiz_by_cpf(self, cpf: str):
        juiz = self.__juiz_dao.get(cpf)
        return juiz.nome
    
    def editar_juiz(self, juiz, opcao, novo_dado):
        if opcao == 0:
            juiz.nome = novo_dado
        elif opcao == 1:
            juiz.matricula = novo_dado
        elif opcao == 2:
            juiz.cpf = novo_dado
        elif opcao == 3:
            juiz.senha = novo_dado
        self.__juiz_dao.remove(juiz.matricula)
        sucesso_edicao = self.__juiz_dao.add(juiz.nome,
                                                juiz.cpf,
                                                juiz.matricula,
                                                juiz.senha)
        if sucesso_edicao:
            self.__tela_juiz.aviso('   Edicao sobre juiz efetuada.   ')
        else:
            self.__tela_juiz.aviso('Erro em edicao de juiz. Repita a operação.')
            
    def remover_juiz(self, juiz):
        self.__juiz_dao.remove(juiz.matricula)
        self.__tela_juiz.aviso('juiz removido com sucesso.')
        
    def mostrar_detalhes_juiz(self, cpf_juiz):
        juiz = self.__juiz_dao.get(cpf_juiz)
        self.__tela_juiz.tela_mostrar_detalhes_juiz(juiz)