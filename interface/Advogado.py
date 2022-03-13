import PySimpleGUI as psg


class InterfaceAdvogado:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_Advogado(self):
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os dados abaixo:')],
                [psg.Text('Nome:', size=(20, 1)), psg.InputText('', key='nome')],
                [psg.Text('Login/Código OAB:', size=(20, 1)), psg.InputText('', key='cod_OAB')],
                [psg.Text('CPF', size = (20, 1)), psg.InputText('', key='cpf')],
                [psg.Text('Senha:', size=(20, 1)), psg.InputText('', key='password', password_char='*')],
                [psg.Button('Enviar Dados'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window('Cadastrar Advogado').Layout(layout_cadastro)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                return self.__controlador.controlador_execucao.interface.tela_cadastro()
            else:
                return values
            
    def tela_inicial_advogado(self, cadastro):
        while True:
            
            left_col = [
                [psg.Text(f'Nome: {cadastro.nome}')],
                [psg.Text(f'OAB: {cadastro.cod_OAB}')]
            ]
            right_col = [
                [psg.Text(f'CPF: {cadastro.cpf}')]
            ]
            layout_inicial = [
                [psg.Text('Bem vindo!')],
                [psg.Column(left_col, element_justification='c', pad=(18,0)), psg.VSeperator(),
                    psg.Column(right_col, element_justification='l')],
                [psg.Button('Editar cadastro', key='editar')],
                [psg.Button('Exibir processos vinculados', key='vinculados')],
                [psg.Button('Exibir todos os processos', key='processos')],
                [psg.Button('Deslogar')]
            ]
            self.__window = psg.Window('Tela inicial').Layout(layout_inicial)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'editar':
                self.tela_editar_advogado(cadastro)
            elif event == 'vinculados':
                self.__controlador.exibir_processos_advogado()
            elif event == 'processos':
                self.__controlador.exibir_todos_processos_advogado()
            elif event == 'Deslogar':
                return self.__controlador.controlador_execucao.interface.tela_inicial()
            elif event == psg.WIN_CLOSED:
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
