import PySimpleGUI as psg
from enum import Enum

class InterfaceSistema:
    
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None


    def tela_login(self):
        while True:
            layout_login = [
                [psg.Text('Login:')],
                [psg.Frame('', layout = [
                    [psg.Radio('Parte', 'r1', key = 'Parte'),
                     psg.Radio('Advogado', 'r1', key = 'Advogado'),
                     psg.Radio('Juiz', 'r1', key = 'Juiz')]])],
                [psg.Text('Número de usuário', size=(20, 1)), psg.InputText('', key = 'Login')],
                [psg.Text('Senha', size=(20, 1)), psg.InputText('', key = 'Senha')],

                [psg.Button('Confirmar'), psg.Button('Sair')]
            ]
            self.__window = psg.Window('Login').Layout(layout_login)
            botao, valores = self.__window.Read()
            self.__window.Close()
            break
        return botao, valores



                
    
    def tela_inicial(self):
        psg.theme('Reddit')
        layout = [[psg.Text('Carregando...', font='ANY 13', pad=(100, 10))],
          [psg.Button('Cancelar')]]
        window = psg.Window('Sistema de Gestão de Processos Judiciais').Layout(layout)

        interromper_programa = False
        count = 0
        while count < 150:
            count = count + 1
            event, values = window.Read(timeout=5)
            if event in (None, 'Exit', 'Cancelar'):
                interromper_programa = True
                break
        window.Close()
        if interromper_programa:
            exit(2)
        while True:
            layout_inicia_sistema = [
                [psg.Text('Escolha a opção:')],
                [psg.Radio('Cadastrar     ', "RADIO", size=(10, 1)),
                psg.Radio('Efetuar Login    ', "RADIO", size=(10, 1))],
                [psg.Button('Enviar'), psg.Button('Sair')]
            ]
            tela_inicio_sistema = psg.Window(
                'Iniciar Modulo').Layout(layout_inicia_sistema)
            event, values = tela_inicio_sistema.read()
            if event == psg.WIN_CLOSED or event == 'Sair':
                tela_inicio_sistema.Close()
                exit(1)
            else:
                if values[0]:
                    tela_inicio_sistema.Close()
                    return self.tela_cadastro()
                else:
                    tela_inicio_sistema.Close()
                    return self.__controlador.login()

                    
            
    def tela_cadastro(self):
         while True:
            layout_inicia_sistema = [
                [psg.Text('Cadastrar-se como:')],
                [psg.Radio('Juiz     ', "RADIO", size=(10, 1)),
                psg.Radio('Advogado    ', "RADIO", size=(10, 1)),
                psg.Radio('Parte    ', "RADIO", size=(10, 1))],
                [psg.Button('Enviar'), psg.Button('Sair')]
            ]
            tela_inicio_sistema = psg.Window(
                'Iniciar Modulo').Layout(layout_inicia_sistema)
            event, values = tela_inicio_sistema.read()
            if event == psg.WIN_CLOSED or event == 'Sair':
                tela_inicio_sistema.Close()
                exit(1)
            else:
                if values[0]:
                    Execucao(Modulo.JUIZ)
                    tela_inicio_sistema.Close()
                    self.__controlador.init_module_juiz()
                elif values[1]:
                    Execucao(Modulo.ADVOGADO)
                    tela_inicio_sistema.Close()
                    self.__controlador.init_module_advogado()
                else:
                    Execucao(Modulo.PARTE)
                    tela_inicio_sistema.Close()
                    self.__controlador.init_module_parte()
            
    def aviso(self, msg):
        layout_aviso = [
            [psg.Text(msg)],
            [psg.Ok()]
        ]
        tela_aviso = psg.Window('Aviso').Layout(layout_aviso)
        tela_aviso.Read()
        tela_aviso.Close()
        
class Modulo(Enum):
    JUIZ = 1
    ADVOGADO = 2
    PARTE = 3
class Execucao:
    def __init__(self, modulo):
        self.__modulo = modulo
