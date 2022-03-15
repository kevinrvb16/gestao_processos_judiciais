from interface.Advogado import InterfaceAdvogado
from arquivos.advogadoDAO import AdvogadoDAO
from controllers.validadorCPF import ValidadorCPF
import string


class AdvogadoController:
    
    def __init__(self, controlador_execucao):
        self.__interface_Advogado = InterfaceAdvogado(self)
        self.__Advogado_dao = AdvogadoDAO()
        self.__controlador_execucao = controlador_execucao

    @property
    def controlador_execucao(self):
        return self.__controlador_execucao

    @property
    def advogado_dao(self):
        return self.__Advogado_dao

    def cadastrar_Advogado(self):
        while True:
            valores = self.__interface_Advogado.tela_cadastrar_Advogado()
            cadastro_ok = self.verifica_cadastro_completo(valores)

            if cadastro_ok:
                advogado_controlador = self.__controlador_execucao.advogado_controller
                validador_cpf = ValidadorCPF()
                nome = valores['nome']
                cod_OAB = valores['cod_OAB']
                cpf = valores['cpf']
                senha = valores['password']

                advogado_ja_cadastrado = advogado_controlador.verifica_cod_OAB(cod_OAB)

                if not advogado_ja_cadastrado:
                    cpf_valido_advogado = validador_cpf.valida_cpf(cpf)
                else:
                    self.__interface_Advogado.aviso('Advogado já cadastrado')
                    continue

                if cpf_valido_advogado:
                    cpf_sem_pontuacao = cpf.translate(str.maketrans('', '', string.punctuation))
                    sucesso_add = self.__Advogado_dao.add(nome, cpf_sem_pontuacao, senha, False, cod_OAB)
                else:
                    self.__interface_Advogado.aviso('CPF inválido')
                    continue

                if sucesso_add:
                    self.__interface_Advogado.aviso('Advogado cadastrado com sucesso')
            else:
                self.__interface_Advogado.aviso('Campos obrigatórios não preenchidos')
                continue
            break
        
    def editar_advogado(self, advogado, opcao, novo_dado):
        if opcao == 0:
            advogado.nome = novo_dado
        elif opcao == 1:
            advogado.senha = novo_dado
        self.__Advogado_dao.remove(advogado.cod_OAB)
        sucesso_edicao = self.__Advogado_dao.add(advogado.nome,
                                                advogado.cpf,
                                                advogado.senha,
                                                True,
                                                advogado.cod_OAB)
        if sucesso_edicao:
            self.__interface_Advogado.aviso('   Edicao sobre advogado efetuada.   ')
        else:
            self.__interface_Advogado.aviso('Erro em edicao de advogado. Repita a operação.')
        
    def exibir_opcoes_advogado(self, usuario):
        self.__interface_Advogado.tela_inicial_advogado(usuario)
        
    def exibir_todos_processos_advogado(self):
        self.__controlador_execucao.init_module_exibir_todos_processos_advogado()

    def exibir_processos_advogado(self, usuario):
        self.__controlador_execucao.init_module_exibir_processos_vinculados(usuario)
        
    def verifica_cadastro_completo(self, values):
        if values['nome'] == '' or values['password'] == '' or values['cod_OAB'] == '':
            self.__interface_Advogado.close_tela_principal()
            return False
        return True


    def listar_Advogado(self):
        dic_nome_num_Advogados = {}
        lista_Advogados = self.__Advogado_dao.get_all()
        for Advogado in lista_Advogados:
            dic_nome_num_Advogados[Advogado.nome] = Advogado.cpf
        self.__interface_Advogado.mostrar_lista(dic_nome_num_Advogados)

    def verifica_cpf_jah_existente(self, cpf):
        advogados = self.__Advogado_dao.get_all()
        print(advogados)
        for advogado in advogados:
            if advogado.cpf == cpf:
                return True
        return False

    def get_nome_Advogado_by_cpf(self, cpf: str):
        advogado = self.__Advogado_dao.get(cpf)
        return advogado.nome
    
    def verifica_cod_OAB(self, cod_OAB):
        verificacao = self.__Advogado_dao.get(cod_OAB)
        if verificacao is None:
            return False
        return True
