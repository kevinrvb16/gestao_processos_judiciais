import PySimpleGUI as psg


class InterfaceJuiz:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_juiz(self, cpf):
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os dados abaixo:')],
                [psg.Text('Nome do Juiz', size=(20, 1)), psg.InputText('', key='nome')],
                [psg.Text('Matricula do Juiz', size=(20, 1)), psg.InputText('', key='matricula')],
                [psg.Text(f'Login                                  {cpf}')],
                [psg.Text('Senha', size=(20, 1)), psg.InputText('', key='password', password_char='*')],
                [psg.Button('Enviar Dados'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window('Cadastrar Juiz').Layout(layout_cadastro)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                return values

    def get_informacao(self, msg_cabecalho, msg_corpo):
        layout_info = [
            [psg.Text(msg_corpo, size=(30, 1)), psg.InputText('')],
            [psg.Button('Remover'), psg.Button('Voltar')]
        ]
        tela_get_info = psg.Window(msg_cabecalho).Layout(layout_info)
        button, values = tela_get_info.Read()
        tela_get_info.Close()
        return button, values[0]

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
