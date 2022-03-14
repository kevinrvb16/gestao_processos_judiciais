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
    def controlador_execucao(self):
        return self.__controlador_execucao
    
    @property
    def parte_dao(self):
        return self.__parte_dao

    def cadastrar_parte(self):
        while True:
            valores = self.__interface_parte.tela_cadastrar_parte()
            advogado_controlador = self.__controlador_execucao.advogado_controller
            cadastro_ok = self.verifica_cadastro_completo(valores)

            if cadastro_ok:
                parte_controlador = self.__controlador_execucao.parte_controller
                validador_cpf = ValidadorCPF()
                nome = valores['nome']
                advogado = valores['advogado']
                cpf = valores['cpf']
                senha = valores['password']

                parte_ja_cadastrada = parte_controlador.verifica_cpf_parte(cpf)

                if not parte_ja_cadastrada:
                    cpf_valido_parte = validador_cpf.valida_cpf(cpf)
                else:
                    self.__interface_parte.aviso('Parte já cadastrada')
                    continue

                if cpf_valido_parte:
                    advogado_encontrado = advogado_controlador.verifica_cod_OAB(advogado)
                else:
                    self.__interface_parte.aviso('CPF inválido')
                    continue

                if advogado_encontrado:
                    sucesso_add = self.__parte_dao.add(nome, cpf, senha, advogado, False)
                else:
                    self.__interface_parte.aviso('Advogado não cadastrado')
                    continue
                
                if sucesso_add:
                    self.__interface_parte.aviso('Parte cadastrada com sucesso')
            else:
                self.__interface_parte.aviso('Campos obrigatórios não preenchidos')
                continue
            break
        
    def criar_processo(self, usuario):
        self.__controlador_execucao.init_module_cadastrar_processo(usuario)
        
    def exibir_processos_parte(self, cadastro):
        self.__controlador_execucao.init_module_exibir_processos_vinculados(cadastro)
        
    def editar_parte(self, parte, opcao, novo_dado):
        if opcao == 0:
            parte.nome = novo_dado
        elif opcao == 1:
            parte.senha = novo_dado
        elif opcao == 2:
            parte.advogado = novo_dado
        self.__parte_dao.remove(parte.cpf)
        sucesso_edicao = self.__parte_dao.add(parte.nome,
                                                parte.cpf,
                                                parte.senha,
                                                True, parte.advogado)
        if sucesso_edicao:
            self.__interface_parte.aviso('   Edicao sobre parte efetuada.   ')
        else:
            self.__interface_parte.aviso('Erro em edicao de parte. Repita a operação.')

    def verifica_cadastro_completo(self, values):
        if values['nome'] == '' or values['password'] == '' or values['advogado'] == '':
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

    def verifica_cpf_parte(self, cpf):
        verificacao = self.__parte_dao.get(cpf)
        if verificacao is None:
            return False
        return True

    def get_nome_parte_by_cpf(self, cpf: str):
        parte = self.__parte_dao.get(cpf)
        return parte.nome
