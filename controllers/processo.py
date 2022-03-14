from interface.atoProcessual import InterfaceAtoProcessual
from interface.processo import InterfaceProcesso
from arquivos.processoDAO import ProcessoDAO
from entities.parte import Parte
from entities.advogado import Advogado
from entities.juiz import Juiz
from controllers.validadorCPF import ValidadorCPF
from datetime import date
import random
import os
import numpy as np
import pickle
import string

class ProcessoController:

    def __init__(self, controlador_execucao):
        self.__interface_processo = InterfaceProcesso(self)
        self.__interface_ato_processual = InterfaceAtoProcessual(self)
        self.__processo_dao = ProcessoDAO()
        self.__controlador_execucao = controlador_execucao
        self.__np_array_de_urgencia = np.array([])
        self.__np_array_de_sigilo = np.array([])
        self.__np_array_de_processos = np.array([])

    @property
    def controlador_execucao(self):
        return self.__controlador_execucao

    def cadastrar_processo(self, usuario):
        while True:
            valores = self.__interface_processo.tela_cadastrar_processo(usuario)
            cadastro_ok = self.verifica_cadastro_completo(valores)
            
            if cadastro_ok:
                juiz_controller = self.__controlador_execucao.juiz_controller
                advogado_controlador = self.__controlador_execucao.advogado_controller
                parte_controlador = self.__controlador_execucao.parte_controller
                validador_cpf = ValidadorCPF()
                cod_OAB = valores['codOAB_advogado_autor']
                cpf_autor = valores['autor']
                eh_sigiloso = valores['eh_sigiloso']
                print(valores)
                cpf_reu = valores['reu']
                anexo = valores['-IN-']
                advogado_encontrado = False
                cpf_valido_autor = False
                cpf_encontrado_autor = False
                cpf_valido_reu = False
                arquivo_anexado = False
                advogado_encontrado = advogado_controlador.verifica_cod_OAB(cod_OAB)
                if advogado_encontrado:
                    cpf_valido_autor = validador_cpf.valida_cpf(cpf_autor)
                else:
                    self.__interface_processo.aviso('Advogado não encontrado')
                    continue
                
                if cpf_valido_autor:
                    cpf_encontrado_autor = parte_controlador.verifica_cpf_parte(cpf_autor)
                else:
                    self.__interface_processo.aviso('CPF do autor inválido')
                    continue
                
                if cpf_encontrado_autor:
                    cpf_valido_reu = validador_cpf.valida_cpf(cpf_reu)
                else:
                    self.__interface_processo.aviso('CPF do autor não cadastrado')
                    continue
                
                if cpf_valido_reu:
                    arquivo_anexado = self.verifica_anexo(anexo)
                    anexo = self.cadastrarInicial(anexo)
                else:
                    self.__interface_processo.aviso('CPF do réu inválido')
                    continue
                
                if arquivo_anexado:                    
                    id_processo = self.atribui_id(cpf_autor)
                    id_juiz = juiz_controller.sortear_juiz()
                    print(id_juiz)
                    sucesso_add = self.__processo_dao.add(cod_OAB, cpf_autor, cpf_reu, anexo, id_juiz, id_processo, eh_sigiloso)
                    if eh_sigiloso:
                        self.solicita_sigilo(id_processo)
                    if sucesso_add:
                        self.__interface_processo.aviso('Processo cadastrado com sucesso')
                else:
                    self.__interface_processo.aviso('Anexe um arquivo')
                    continue    
            else:
                self.__interface_processo.aviso('Campos obrigatórios não preenchidos')
                continue
                    
            break
    
    def atribui_id(self, cpf_autor):
        lista_processo = self.__processo_dao.get_all()
        print('lista Processo tamanho:')
        print(len(lista_processo))
        cpf_sem_pontuacao = cpf_autor.translate(str.maketrans('', '', string.punctuation))
        id_processo = int(cpf_sem_pontuacao + str(len(lista_processo) + 1))
        return id_processo
        
                
    def realizar_ato_processual(self, id_processo):
        while True:
            valores = self.__interface_ato_processual.tela_realizar_ato()
            eh_urgente = valores[0]
            nome_anexo= valores['-IN-']
            arquivo_anexado = self.verifica_anexo(nome_anexo)
            if arquivo_anexado:
                data = date.today()
                self.salvar_data(data, id_processo)
                self.solicita_urgencia(eh_urgente, id_processo)
                self.salvar_anexo(nome_anexo, id_processo)
                self.__interface_processo.aviso('   Processo atualizado com Sucesso ')
            else:
                self.__interface_processo.aviso('   Anexe um arquivo    ')
                continue
            break
    
    def verifica_anexo(self, nome_anexo):
        if nome_anexo == '':
            return False
        if nome_anexo.split('.') == None:
            return False
        return True
        
    def verifica_cadastro_completo(self, values):
        if values['-IN-'] == '' or values['autor'] == '' or values['codOAB_advogado_autor'] == '' or values['eh_sigiloso'] == '' or values['reu'] == '':
            self.__interface_processo.close_tela_principal()
            return False
        return True
    
    def salvar_data(self, data, id_processo):
        self.__processo_dao.add_data(data, id_processo)
        
    def salvar_anexo(self, data, id_processo):
        self.__processo_dao.add_anexo(data, id_processo)

    def solicita_urgencia(self, eh_urgente, id_processo):
        
        lista = np.array(id_processo)
        print('Lista Urgencia:')
        print(lista)
        
        arquivo = open('listaUrgencia.txt', 'r')
        conteudo = arquivo.read()
        
        arquivo = open('listaUrgencia.txt', 'w+')
        conteudo += str(lista) + '\n'
        arquivo.write(conteudo)
        arquivo.close()
        
        print('\nConteudo no listaUrgencia.txt:\n', conteudo)
        arquivo.close()

    def solicita_sigilo(self, id_processo):
        lista = np.array(id_processo)
        print('Lista Sigilo:')
        print(lista)

        arquivo = open('listaSigilo.txt', 'r')
        conteudo = arquivo.read()
        
        arquivo = open('listaSigilo.txt', 'w+')
        conteudo += str(lista) + ', '
        arquivo.write(conteudo)
        arquivo.close()

        print('\nConteudo no listaSigilo.txt:\n', conteudo)
        arquivo.close()


    def listar_Processos(self):
        dic_nome_num_Processos = {}
        lista_processos = self.__processo_dao.get_all()
        for processo in lista_processos:
            dic_nome_num_Processos[processo.get_eh_urgente] = processo.id_processo
        print(dic_nome_num_Processos)

    
    def despachar(self, juiz):
        while True:
            valores = self.__interface_ato_processual.despachar_processo()
            if valores:
                id_processo = valores['processo_id'].strip()
                processo = self.__processo_dao.get(int(id_processo))
                anexo = valores['Browse']
                if self.eJuizDoProcesso(juiz, processo):
                    if self.emAndamento(processo):
                        if self.estaConcluso(processo):
                            arquivo_anexado = self.verifica_anexo(anexo)
                            if arquivo_anexado:
                                if  self.verificaIntimaçao((valores['Autora'],valores['Ré'],valores['Ambas'])):
                                    data = date.today()
                                    self.salvar_data(data, int(id_processo))
                                    self.salvar_anexo(anexo, int(id_processo))
                                    self.__interface_processo.aviso('   Processo atualizado com Sucesso ')
                                    return self.__controlador_execucao.interface.tela_inicial()
                                else:
                                    self.__interface_processo.aviso('   Selecione as partes a serem intimadas   ')
                                    continue
                            else:
                                self.__interface_processo.aviso('   Anexe um arquivo    ')
                                continue
                        else:
                            self.__interface_processo.aviso('   Esse processo não está pronto para ser despachado    ')
                            return self.despachar(juiz)
                    else:
                        self.__interface_processo.aviso('   Esse processo já está finalizado    ')
                        return self.despachar(juiz)
                else:
                    self.__interface_processo.aviso('   Somente o juiz do processo pode proferir despachos    ')
                    return self.despachar(juiz)
            else:
                return
            
    def exibir_processos_vinculados(self, cadastro):
        todos_processos = self.__processo_dao.get_all()
        processos_vinculados = []
        for processo in todos_processos:
            if isinstance(cadastro, Advogado):
                if cadastro.cod_OAB in [processo.codOAB_advogado_autor, processo.codOAB_advogado_reu]:
                    processos_vinculados.append(processo)
            elif isinstance(cadastro, Parte):
                if cadastro.cpf == processo.autor:
                    processos_vinculados.append(processo)
            elif isinstance(cadastro, Juiz):
                if cadastro.matricula == processo.juiz:
                    processos_vinculados.append(processo)
        self.__interface_processo.tela_processos_vinculados(processos_vinculados)
        
    def exibir_todos_processos(self):
        self.__interface_processo.tela_todos_processos()
    
    def eJuizDoProcesso(self, juiz, processo):
        return str(juiz.cpf) == str(processo.juiz)
    
    def emAndamento(self, processo):
        return processo.get_anexos()[-1].split('/')[-1].split('.')[0] != 'Finalizado'
    
    def estaConcluso(self, processo):
        nome_arquivo = processo.get_anexos()[-1].split('/')[-1].split('.')[0]
        print(nome_arquivo)
        return  (nome_arquivo != 'Despacho')

    def verificaIntimaçao(self, valores):
        return valores[0] or valores[1] or valores[2]
    
    def andamentoProcesso(self, processo):
        sequenciaDocumentos = processo.get_anexos()
        andamentos = []
        for i in range(len(sequenciaDocumentos)):
            andamentos.append(sequenciaDocumentos[i].split('/')[-1].split('.')[0])
        return andamentos
    
    def atosPartes(self):
        return ['Inicial', 'Contestação', 'Réplica', 'Alegações finais', 'Alegações finais',
        'Apelação', 'Contrarrazões']
    
    def cadastrarInicial(self, anexo):
        cwd = os.getcwd()
        diretorio = False
        while not diretorio:
            final = str(random.randrange(1,10000))
            try:
                path = os.path.join(cwd, 'Anexos', final)
                os.makedirs(path)
            except:
                pass
            if os.path.exists(path):
                diretorio = True
        arquivo = open(anexo, 'r')
        conteudo = arquivo.read()
        path = path = os.path.join(path, 'Inicial.txt')
        arquivo = open(path, 'w+')
        arquivo.write(conteudo)
        arquivo.close()
        return path
    
    def situacaoProcesso(self, processo):
        andamentos = processo.get_anexos()
        situacao = andamentos[-1].split('/')[-1].split('.')[0]
        return situacao



