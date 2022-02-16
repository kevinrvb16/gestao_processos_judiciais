import PySimpleGUI as psg

class InterfaceProcesso:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_processo(self):
        settings = psg.UserSettings()
        psg.user_settings_filename(path='.')
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os campos abaixo:')],
                [psg.Text('OAB do Advogado Autor:', size=(20, 1)), psg.InputText('', key='codOAB_advogado_autor')],
                [psg.Text('CPF do Autor:', size=(20, 1)), psg.InputText('', key='autor')],
                [psg.Text('Solicitar Sigilo:')],
                [psg.Radio('Sim:     ',"RADIO", size=(10, 1), key='eh_sigiloso'),
                psg.Radio('Não:     ',"RADIO", size=(10, 1))],
                [psg.Text('CPF do réu:', size=(20, 1)), psg.InputText('', key='reu')],
                [psg.Text('Anexe aqui seu arquivo:', size=(20, 1))],
                [psg.Input(key='-IN-'), psg.FileBrowse()],
                [psg.Button('Cadastrar'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window('Cadastrar Processo').Layout(layout_cadastro)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                settings['-filename-'] = values['-IN-']
                return values
                
    def aviso(self, msg):
        layout_aviso = [
            [psg.Text(msg)],
            [psg.Ok()]
        ]
        tela_aviso = psg.Window('Aviso').Layout(layout_aviso)
        tela_aviso.Read()
        tela_aviso.Close()
        
    def close_tela_principal(self):
        self.__window.Close()