from interface.atoProcessual import InterfaceAtoProcessual
from interface.processo import InterfaceProcesso
from arquivos.processoDAO import ProcessoDAO
from entities.parte import Parte
from entities.advogado import Advogado
from entities.juiz import Juiz
from controllers.validadorCPF import ValidadorCPF
from datetime import date
from sys import platform
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
    
    @property
    def processo_dao(self):
        return self.__processo_dao

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
                else:
                    self.__interface_processo.aviso('CPF do réu inválido')
                    continue                
                if arquivo_anexado:        
                    anexo = self.salvarDocumento(anexo)            
                    id_processo = self.atribui_id(cpf_autor)
                    id_juiz = juiz_controller.sortear_juiz()
                    sucesso_add = self.__processo_dao.add(cod_OAB, cpf_autor, cpf_reu, anexo, id_juiz, id_processo, eh_sigiloso)
                    if eh_sigiloso:
                        self.solicita_sigilo(id_processo)
                    if sucesso_add:
                        self.__interface_processo.aviso('Processo cadastrado com sucesso')
                else:
                    self.__interface_processo.aviso('Anexe um arquivo válido')
                    continue    
            else:
                self.__interface_processo.aviso('Campos obrigatórios não preenchidos')
                continue                    
            break
    
    def atribui_id(self, cpf_autor):
        lista_processo = self.__processo_dao.get_all()
        cpf_sem_pontuacao = cpf_autor.translate(str.maketrans('', '', string.punctuation))
        id_processo = int(cpf_sem_pontuacao + str(len(lista_processo) + 1))
        return id_processo        
                
    def realizar_ato_processual(self, usuario, id_processo):
        processo = self.__processo_dao.get(int(id_processo))
        if ((usuario.cod_OAB == processo.codOAB_advogado_autor) and not ('Autora' in processo.intimacao())) or\
            ((usuario.cod_OAB == processo.codOAB_advogado_reu) and not ('Ré' in processo.intimacao())):
                self.__interface_ato_processual.aviso('Não há intimações abertas para este usuário')
                return self.exibir_informacoes_processo(usuario, processo)
        else:
            while True:
                andamentos = self.andamentoProcesso(processo)
                atos = ['Inicial', 'Contestação', 'Réplica', 'Alegações finais', 'Alegações finais',
                        'Apelação', 'Contrarrazões']
                for andamento in andamentos:
                    if andamento in atos:
                        atos.remove(andamento)     
                ato = atos[0]               
                valores = self.__interface_ato_processual.tela_realizar_ato(ato)
                eh_urgente = valores[0]
                nome_anexo= valores['-IN-']
                arquivo_anexado = self.verifica_anexo(nome_anexo)
                if arquivo_anexado:
                    anexo = self.salvarDocumento(nome_anexo, processo, ato)
                    data = date.today()
                    self.salvar_data(data, id_processo)
                    self.solicita_urgencia(eh_urgente, id_processo)
                    self.salvar_anexo(anexo, id_processo)
                    self.__interface_processo.aviso('   Processo atualizado com Sucesso ')
                    processo.intimacao = []
                    return self.exibir_informacoes_processo(usuario, processo)
                else:
                    self.__interface_processo.aviso('   Anexe um arquivo    ')
                    continue
    
    def verifica_anexo(self, nome_anexo):
        nome_anexo_desmembrado= nome_anexo.split('.')
        
        if os.path.isfile(nome_anexo) and nome_anexo_desmembrado[len(nome_anexo_desmembrado) - 1] == 'txt':
            return True
        return False
        
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
    
    def despachar(self, juiz, processo):
        while True:
            valores = self.__interface_ato_processual.despachar_processo(processo)
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
                                    situacao = self.situacaoProcesso(processo)
                                    if situacao == 'Alegações finais':
                                        ato = 'Sentença'
                                    elif situacao == 'Contrarrazões':
                                        ato = 'Acórdão'
                                    elif situacao == 'Contestação':
                                        ato = 'Saneador'
                                    else:
                                        ato = 'Despacho'
                                    anexo = self.salvarDocumento(anexo, processo, ato)
                                    data = date.today()
                                    self.salvar_data(data, int(id_processo))
                                    self.salvar_anexo(anexo, int(id_processo))
                                    self.__interface_processo.aviso('   Processo atualizado com Sucesso ')
                                    if valores['Autora']:
                                        self.__processo_dao.add_intimacao(['Autora'], processo.id_processo)
                                    elif valores['Ré']:
                                        self.__processo_dao.add_intimacao(['Ré'], processo.id_processo)
                                    else:
                                        self.__processo_dao.add_intimacao(['Autora', 'Ré'], processo.id_processo)                                    
                                else:
                                    self.__interface_processo.aviso('   Selecione as partes a serem intimadas   ')
                                    continue
                            else:
                                self.__interface_processo.aviso('   Anexe um arquivo    ')
                                continue
                        else:
                            self.__interface_processo.aviso('   Esse processo não está pronto para ser despachado    ')
                            return self.despachar(juiz, processo)
                    else:
                        self.__interface_processo.aviso('   Esse processo já está finalizado    ')
                        return self.despachar(juiz, processo)
                else:
                    self.__interface_processo.aviso('   Somente o juiz do processo pode proferir despachos    ')
                    return self.despachar(juiz, processo)
            return self.controlador_execucao.init_module_inicial_juiz(juiz)

    def exibir_processos_vinculados(self, usuario):
        todos_processos = self.__processo_dao.get_all()
        processos_vinculados = []
        for processo in todos_processos:
            if isinstance(usuario, Advogado):
                if usuario.cod_OAB in [processo.codOAB_advogado_autor, processo.codOAB_advogado_reu]:
                    processos_vinculados.append(processo)
            elif isinstance(usuario, Parte):
                if usuario.cpf in [processo.autor, processo.reu]:
                    processos_vinculados.append(processo)
            elif isinstance(usuario, Juiz):
                if usuario.matricula == processo.juiz:
                    processos_vinculados.append(processo)
        opcao = self.__interface_processo.tela_processos_vinculados(processos_vinculados)
        if opcao == 'Voltar':
            if isinstance(usuario, Advogado):
                return self.controlador_execucao.init_module_inicial_advogado(usuario)
            elif isinstance(usuario, Parte):
                return self.controlador_execucao.init_module_inicial_parte(usuario)
            elif isinstance(usuario, Juiz):
                return self.controlador_execucao.init_module_inicial_juiz(usuario)      
        elif opcao and self.__processo_dao.get(int(opcao)):
            proc = self.__processo_dao.get(int(opcao))
            return self.exibir_informacoes_processo(usuario, proc)
        else:
            return self.controlador_execucao.init_module_inicial_advogado(usuario)
        
    def exibir_todos_processos(self, usuario):
        todos_processos = self.__processo_dao.get_all()
        opcao = self.__interface_processo.tela_todos_processos(todos_processos)
        if opcao:
            processo = self.__processo_dao.get(opcao)
            return self.exibir_informacoes_processo(usuario, processo)
        else:
            return
    
    def exibir_informacoes_processo(self, usuario, processo):
        reu = self.controlador_execucao.parte_controller.parte_dao.get(processo.reu)
        adv_reu = self.controlador_execucao.advogado_controller.advogado_dao.get(reu.advogado)
        processo.codOAB_advogado_reu = adv_reu.cod_OAB
        self.__processo_dao.salvar()
        opcao = self.__interface_processo.tela_processo(processo)
        if opcao == 'Peticionar':
            if isinstance(usuario, Advogado):
                return self.realizar_ato_processual(usuario, processo.id_processo)
            elif isinstance(usuario, Juiz):
                return self.despachar(usuario, processo)

    def eJuizDoProcesso(self, juiz, processo):
        return str(juiz.matricula) == str(processo.juiz)

    def situacaoProcesso(self, processo):
        sequenciaDocumentos = processo.get_anexos()
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            situacao = sequenciaDocumentos[-1].split('/')[-1].split('.')[0]
        elif platform == "win32":
            situacao = sequenciaDocumentos[-1].split('\\')[-1].split('.')[0]
        return situacao
    
    def emAndamento(self, processo):
        return self.situacaoProcesso(processo) != 'Finalizado'
    
    def estaConcluso(self, processo):
        return  len(processo.intimacao()) == 0

    def verificaIntimaçao(self, valores):
        return valores[0] or valores[1] or valores[2]
    
    def andamentoProcesso(self, processo):
        sequenciaDocumentos = processo.get_anexos()
        andamentos = []
        for i in range(len(sequenciaDocumentos)):
            if platform == "linux" or platform == "linux2" or platform == "darwin":
                andamentos.append(sequenciaDocumentos[i].split('/')[-1].split('.')[0])
            elif platform == "win32":
                andamentos.append(sequenciaDocumentos[i].split('\\')[-1].split('.')[0])
        return andamentos
    
    def getDiretorio(self, processo):
        listaAnexos = processo.get_anexos()
        anexo = listaAnexos[-1]
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            caminho = anexo.split('/')[:-1]
            path = '/'.join(caminho)
        elif platform == "win32":
            caminho = anexo.split('\\')[:-1]
            path = '\\'.join(caminho)
        return path
    
    def abrirDocumento(self, anexo, processo = None):
        if not processo:
            arquivo = open(anexo, 'r')
        else:
            dir = self.getDiretorio(processo)
            dir = os.path.join(dir, anexo)
            dir = dir + '.txt'
            arquivo = arquivo = open(dir, 'r')
        conteudo = arquivo.read()        
        return conteudo
    
    def salvarDocumento(self, anexo, processo = None, ato = None):
        cwd = os.getcwd()
        if not processo:
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
            path = os.path.join(path, 'Inicial.txt')
        else:
            path = self.getDiretorio(processo)
            path = os.path.join(path, f'{ato}.txt')
        arquivo = open(anexo, 'r')
        conteudo = arquivo.read()
        arquivo = open(path, 'w+')
        arquivo.write(conteudo)
        arquivo.close()
        return path
