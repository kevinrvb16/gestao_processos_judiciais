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

    def parte_controller(self):
        return self.__controlador_parte

    def advogado_controller(self):
        return self.__controlador_advogado
    
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
        
    def init_module_despachar(self):
        self.__controlador_processo.despachar()

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
                print(cadastro.senha)
                if senha == cadastro.senha:
                    if valores['Parte']:
                        pass
                    elif valores['Advogado']:
                        return self.init_module_efetuar_ato_processual()
                    elif valores['Juiz']:
                        return self.__controlador_juiz.mostrar_detalhes_juiz(valores[0])
                else:
                    self.__interface_sistema.aviso('Senha incorreta')
                    return self.login()
            else:
                self.__interface_sistema.aviso('Usuário inexistente')
                return self.login()
        return self.interface.tela_inicial()

                
