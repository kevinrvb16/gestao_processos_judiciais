from interface.parte import InterfaceParte
from arquivos.parteDAO import ParteDAO
from controllers.validadorCPF import ValidadorCPF
import hashlib


class ParteController:
    
    def __init__(self, controlador_execucao):
        self.__interface_parte = InterfaceParte(self)
        self.__parte_dao = ParteDAO()
        self.__controlador_execucao = controlador_execucao

    @property
    def parte_dao(self):
        return self.__parte_dao

    def cadastrar_parte(self):
        while True:
            cpf = ValidadorCPF().solicita_cpf_cadastro()
            if cpf is None:
                break
            existe_cpf = self.verifica_cpf_jah_existente(cpf)
            if existe_cpf:
                self.__interface_parte.aviso('\nCPF já foi cadastrado!')
                continue
            while True:
                try:
                    valores = self.__interface_parte.tela_cadastrar_parte(cpf)
                    cadastro_ok = self.verifica_cadastro_completo(valores)
                except TypeError:
                    break
                if not cadastro_ok:
                    self.__interface_parte.aviso('\nCampo(s) obrigatórios não preenchidos')
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
                sucesso_add = self.__parte_dao.add(valores['nome'],
                                                           cpf,
                                                           senha,
                                                           False)
                if not sucesso_add:
                    self.__interface_parte.aviso('Erro no cadastro')
                break
            break
        
    def criar_processo(self):
        self.__controlador_execucao.init_module_cadastrar_processo()
        
    def exibir_processos_parte(self):
        self.__controlador_execucao.init_module_exibir_processos_parte()

    def verifica_cadastro_completo(self, values):
        if values['nome'] == '' or values['password'] == '':
            self.__interface_parte.close_tela_principal()
            return False
        return True
    
    def exibir_opcoes_parte(self, usuario):
        self.__interface_parte.tela_inicial_parte(usuario)

    def listar_parte(self):
        dic_nome_num_partes = {}
        lista_partes = self.__parte_dao.get_all()
        for parte in lista_partes:
            dic_nome_num_partes[parte.nome] = parte.cpf
        self.__interface_parte.mostrar_lista(dic_nome_num_partes)

    def verifica_cpf_jah_existente(self, cpf):
        verificacao = self.__parte_dao.get(cpf)
        if verificacao is None:
            return False
        return True

    def get_nome_parte_by_cpf(self, cpf: str):
        juiz = self.__parte_dao.get(cpf)
        return parte.nome
