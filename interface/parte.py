import PySimpleGUI as psg


class InterfaceParte:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_parte(self, cpf):
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os dados abaixo:')],
                [psg.Text('Nome:', size=(20, 1)), psg.InputText('', key='nome')],
                [psg.Text('Advogado Padrão:', size=(20, 1)), psg.InputText('', key='advogado')],
                [psg.Text(f'Login:                                  {cpf}')],
                [psg.Text('Senha:', size=(20, 1)), psg.InputText('', key='password', password_char='*')],
                [psg.Button('Enviar Dados'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window('Cadastrar Parte').Layout(layout_cadastro)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                return values
    
            
    def tela_inicial_parte(self, cadastro):
        while True:
            layout_inicial = [
                [psg.Text('Bem vindo!')],
                [psg.Button('Editar cadastro')],
                [psg.Button('Exibir processos vinculados', key='exibirProcessosVinculados')],
                [psg.Button('Cadastrar processo',key='cadProcesso')],
                [psg.Button('Deslogar')]
            ]
            self.__window = psg.Window('Tela inicial').Layout(layout_inicial)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'cadProcesso':
                self.__controlador.criar_processo()
            if event == 'exibirProcessosVinculados':
                self.__controlador.exibir_processos_parte()
            if event == 'Deslogar' or event == psg.WIN_CLOSED:
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
