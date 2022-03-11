from interface.atoProcessual import InterfaceAtoProcessual
from interface.processo import InterfaceProcesso
from arquivos.processoDAO import ProcessoDAO
from controllers.validadorCPF import ValidadorCPF
from datetime import date
import numpy as np
import pickle

class ProcessoController:

    def __init__(self, controlador_execucao):
        self.__interface_processo = InterfaceProcesso(self)
        self.__interface_ato_processual = InterfaceAtoProcessual(self)
        self.__processo_dao = ProcessoDAO()
        self.__controlador_execucao = controlador_execucao
        self.__np_array_de_urgencia = np.array([])
        self.__np_array_de_sigilo = np.array([])
        self.__np_array_de_processos = np.array([])
        

    def cadastrar_processo(self):
        while True:
            valores = self.__interface_processo.tela_cadastrar_processo()
            cadastro_ok = self.verifica_cadastro_completo(valores)
            
            if cadastro_ok:
                juiz_controller = self.__controlador_execucao.juiz_controller()
                advogado_controlador = self.__controlador_execucao.advogado_controller()
                parte_controlador = self.__controlador_execucao.parte_controller()
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
                    cpf_encontrado_autor = parte_controlador.verifica_cpf_jah_existente(cpf_autor)
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
                    id_processo = self.atribui_id()
                    id_juiz = juiz_controller.sortear_juiz()
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
    
    def atribui_id(self):
        lista_processo = self.__processo_dao.get_all()
        id_processo = len(lista_processo) + 1
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
                if(eh_urgente):
                   self.solicita_urgencia(eh_urgente, id_processo)
                self.salvar_anexo(nome_anexo, id_processo)
                self.__interface_processo.aviso('   Processo atualizado com Sucesso ')
            else:
                self.__interface_processo.aviso('   Anexe um arquivo    ')
                continue
            break
    
    def despachar(self, id_processo):
        return False
    
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
        
        arquivo = open('listaUrgencia.txt', 'r')
        conteudo = arquivo.read()
        
        arquivo = open('listaUrgencia.txt', 'w+')
        conteudo += str(lista) + '\n'
        arquivo.write(conteudo)
        arquivo.close()
        
    def solicita_sigilo(self, id_processo):
        lista = np.array(id_processo)

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

