import PySimpleGUI as psg

class InterfaceAtoProcessual:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None
            
    def tela_realizar_ato(self, ato):
        settings = psg.UserSettings()
        psg.user_settings_filename(path='.')
        while True:
            layout_ato_processual = [
                [psg.Text('Preencha os campos abaixo:', size=(30, 1))],
                [psg.Text('', size=(30, 1))],
                [psg.Text(f'Ato processual a ser realizado:      {ato}', size=(30, 1))],
                [psg.Checkbox('Solicitar urgência:     ', size=(30, 1))],
                [psg.Text('Anexe aqui seu arquivo:', size=(30, 1))],
                [psg.Input(psg.user_settings_get_entry('-filename-', ''), key='-IN-'), psg.FileBrowse()],
                [psg.Button('Enviar'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window('Tela Realizar Ato').Layout(layout_ato_processual)
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

    def despachar_processo(self, processo):
        settings = psg.UserSettings()
        psg.user_settings_filename(path='.')
        while True:
            layout_despachar_processo = [
                [psg.Text('Despachar processo', size=(30, 1))],
                [psg.Text('Número do processo: '), psg.Input(default_text=f'{processo.id_processo}', disabled=True, key='processo_id')],
                [psg.Text('', size=(30, 1))],
                [psg.Text('Anexe aqui seu arquivo:', size=(30, 1))],
                [psg.Input(psg.user_settings_get_entry('-filename-', ''), key='-IN-'), psg.FileBrowse()],
                [psg.Frame('Selecione as partes cujos advogados devem ser intimados', layout = [
                    [psg.Checkbox('Autora', key = 'Autora',),
                     psg.Checkbox('Ré', key = 'Ré'),
                     psg.Checkbox('Ambas', key = 'Ambas')]])],
                [psg.Button('Enviar'), psg.Button('Voltar')]
            ]
            despachar_processo = psg.Window('Despachar').Layout(layout_despachar_processo)
            self.__window = despachar_processo
            event, values = despachar_processo.Read()
            despachar_processo.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                settings['-filename-'] = values['-IN-']
                return values
            
            
    def close_tela_principal(self):
        self.__window.Close()



                
