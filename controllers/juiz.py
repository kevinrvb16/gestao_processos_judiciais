from interface.juiz import InterfaceJuiz
from arquivos.juizDAO import JuizDAO
from controllers.validadorCPF import ValidadorCPF
import string
import random


class JuizController:
    
    def __init__(self, controlador_execucao):
        self.__interface_juiz = InterfaceJuiz(self)
        self.__juiz_dao = JuizDAO()
        self.__controlador_execucao = controlador_execucao
    
    @property
    def controlador_execucao(self):
        return self.__controlador_execucao

    @property
    def juiz_dao(self):
        return self.__juiz_dao

    def cadastrar_juiz(self):
        while True:
            valores = self.__interface_juiz.tela_cadastrar_juiz()
            cadastro_ok = self.verifica_cadastro_completo(valores)

            if cadastro_ok:
                validador_cpf = ValidadorCPF()
                nome = valores['nome']
                matricula = valores['matricula']
                cpf = valores['cpf']
                senha = valores['password']

                juiz_ja_cadastrado = self.verifica_matricula_jah_existente(matricula)

                if not juiz_ja_cadastrado:
                    cpf_valido_juiz = validador_cpf.valida_cpf(cpf)
                else:
                    self.__interface_juiz.aviso('Juiz já cadastrado')
                    continue

                if cpf_valido_juiz:
                    cpf_sem_pontuacao = cpf.translate(str.maketrans('', '', string.punctuation))
                    sucesso_add = self.__juiz_dao.add(nome, cpf_sem_pontuacao, matricula, senha)
                else:
                    self.__interface_juiz.aviso('CPF inválido')
                    continue

                if sucesso_add:
                    self.__interface_juiz.aviso('Juiz cadastrado com sucesso')
            else:
                self.__interface_juiz.aviso('Campos obrigatórios não preenchidos')
                continue
            break                
                
        
    def exibir_opcoes_juiz(self, usuario):
        self.__interface_juiz.tela_inicial_juiz(usuario)
        
    def exibir_processos_juiz(self, usuario):
        self.__controlador_execucao.init_module_exibir_processos_vinculados(usuario)
    
    def exibir_todos_processos_juiz(self):
        self.__controlador_execucao.init_module_exibir_todos_processos_juiz()
        
    def editar_juiz(self, juiz, opcao, novo_dado):
        if opcao == 0:
            juiz.nome = novo_dado
        elif opcao == 1:
            juiz.senha = novo_dado
        self.__juiz_dao.remove(juiz.matricula)
        sucesso_edicao = self.__juiz_dao.add(juiz.nome,
                                                juiz.cpf,
                                                juiz.matricula,
                                                juiz.senha)
        if sucesso_edicao:
            self.__interface_juiz.aviso('   Edicao sobre juiz efetuada.   ')
        else:
            self.__interface_juiz.aviso('Erro em edicao de juiz. Repita a operação.')
        
    def sortear_juiz(self):
        lista_juizes = self.__juiz_dao.get_all()
        lista_matricula = []
        for juiz in lista_juizes:
            lista_matricula.append(juiz.matricula)
        return random.choice(lista_matricula)

    def verifica_matricula_jah_existente(self, matricula):
        verificacao = self.__juiz_dao.get(matricula)
        if verificacao is None:
            return False
        return True
    
    def verifica_cadastro_completo(self, values):
        if values['nome'] == '' or values['password'] == '' or values['matricula'] == '':
            self.__interface_juiz.close_tela_principal()
            return False
        
        return True


    def listar_juiz(self):
        dic_nome_num_juizes = {}
        lista_juizes = self.__juiz_dao.get_all()
        for juiz in lista_juizes:
            dic_nome_num_juizes[juiz.nome] = juiz.cpf
        self.__interface_juiz.mostrar_lista(dic_nome_num_juizes)


    def get_nome_juiz_by_matricula(self, matricula: str):
        juiz = self.__juiz_dao.get(matricula)
        return juiz.nome
