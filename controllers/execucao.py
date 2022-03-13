from controllers.juiz import JuizController
from controllers.parte import ParteController
from controllers.Advogado import AdvogadoController
from controllers.processo import ProcessoController
from interface.execucao import InterfaceSistema

class ControladorSistema:
    def __init__(self):
        self.__controlador_juiz = JuizController(self)
        self.__controlador_parte = ParteController(self)
        self.__controlador_advogado = AdvogadoController(self)
        self.__interface_sistema = InterfaceSistema(self)
        self.__controlador_processo = ProcessoController(self)

    @property
    def interface(self):
        return self.__interface_sistema


    def juiz_controller(self):
        return self.__controlador_juiz

    # @property
    def parte_controller(self):
        return self.__controlador_parte

    # @property
    def advogado_controller(self):
        return self.__controlador_advogado
    
    # @property
    def processo_controller(self):
        return self.__controlador_processo
    
    def init_module_juiz(self):
        self.__controlador_juiz.cadastrar_juiz()

    def init_module_parte(self):
        self.__controlador_parte.cadastrar_parte()

    def init_module_advogado(self):
        self.__controlador_advogado.cadastrar_Advogado()
        
    def init_module_cadastrar_processo(self):
        self.__controlador_processo.cadastrar_processo()
        
    def init_module_efetuar_ato_processual(self):
        self.__controlador_processo.realizar_ato_processual(1)
        
    def init_module_despachar(self, usuario):
        self.__controlador_processo.despachar(usuario)
        
    def init_module_inicial_juiz(self, usuario):
        self.__controlador_juiz.exibir_opcoes_juiz(usuario)
        
    def init_module_inicial_advogado(self, usuario):
        self.__controlador_advogado.exibir_opcoes_advogado(usuario)
        
    def init_module_inicial_parte(self, usuario):
        self.__controlador_parte.exibir_opcoes_parte(usuario)
        
    def init_module_exibir_processos_parte(self):
        self.__controlador_processo.exibir_processos_vinculados()
    
    def init_module_exibir_processos_juiz(self):
        self.__controlador_processo.exibir_processos_vinculados()
        
    def init_module_exibir_processos_advogado(self):
        self.__controlador_processo.exibir_processos_vinculados()
        
    def init_module_exibir_todos_processos_juiz(self):
        self.__controlador_processo.exibir_todos_processos()
    
    def init_module_exibir_todos_processos_advogado(self):
        self.__controlador_processo.exibir_todos_processos()

    def login(self):
        botao, valores = self.__interface_sistema.tela_login()
        if botao == 'Confirmar':
            usuario = valores['Login'].strip()
            senha = valores['Senha']
            if valores['Parte']:
                cadastro = self.__controlador_parte.parte_dao.get(usuario)
            elif valores['Advogado']:
                cadastro = self.__controlador_advogado.advogado_dao.get(usuario)
            elif valores['Juiz']:
                cadastro = self.__controlador_juiz.juiz_dao.get(usuario)
            if cadastro:
                if senha == cadastro.senha:
                    if valores['Parte']:
                        return self.init_module_inicial_parte(cadastro)
                    elif valores['Advogado']:
                        return self.init_module_inicial_advogado(cadastro)
                    elif valores['Juiz']:
                        return self.init_module_inicial_juiz(cadastro)
                else:
                    self.__interface_sistema.aviso('Senha incorreta')
                    return self.login()
            else:
                self.__interface_sistema.aviso('Usuário inexistente')
                return self.login()
        return self.interface.tela_inicial()

                
