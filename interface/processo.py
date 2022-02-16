import PySimpleGUI as psg

class InterfaceProcesso:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_processo(self):
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os campos abaixo:')],
                [psg.Text('OAB do Advogado Autor:', size=(20, 1)), psg.InputText('', key='codOAB_advogado_autor')],
                [psg.Text('CPF do Autor:', size=(20, 1)), psg.InputText('', key='autor')],
                [psg.Text('Solicitar Sigilo:')],
                [psg.Radio('Sim:     ',"RADIO", size=(10, 1)),
                psg.Radio('Não:     ',"RADIO", size=(10, 1))],
                [psg.Text('CPF do réu:', size=(20, 1)), psg.InputText('', key='reu')],
                [psg.Text('Anexe aqui seu arquivo:', size=(20, 1)), psg.Button('Anexar')],
                [psg.Button('Cadastrar'), psg.Button('Voltar')]
            ]
            tela_cadastro = psg.Window('Cadastrar Processo').Layout(layout_cadastro)
            event, values = tela_cadastro.Read()
            tela_cadastro.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                return values
            
    def tela_realizar_ato(self):
        while True:
            layout_ato_processual = [
                [psg.Text('Preencha os campos abaixo:', size=(30, 1))],
                [psg.Text('', size=(30, 1))],
                [psg.Checkbox('Solicitar urgência:     ',"CHECKBOX", size=(30, 1))],
                [psg.Text('Anexe aqui seu arquivo:', size=(30, 1)), psg.Button('Anexar')],
                [psg.Button('Enviar'), psg.Button('Voltar')]
            ]
            tela_realizar_ato = psg.Window('Tela Realizar Ato').Layout(layout_ato_processual)
            event, values = tela_realizar_ato.Read()
            tela_realizar_ato.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                return values
                
    def aviso(self, msg):
        layout_aviso = [
            [psg.Text(msg)],
            [psg.Ok()]
        ]
        tela_aviso = psg.Window('Aviso').Layout(layout_aviso)
        tela_aviso.Read()
        tela_aviso.Close()