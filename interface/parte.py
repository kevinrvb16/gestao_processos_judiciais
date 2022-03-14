import PySimpleGUI as psg


class InterfaceParte:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_parte(self):
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os dados abaixo:')],
                [psg.Text('Nome:', size=(20, 1)), psg.InputText('', key='nome')],
                [psg.Text('Advogado Padrão:', size=(20, 1)), psg.InputText('', key='advogado')],
                [psg.Text('Login/CPF', size = (20, 1)), psg.InputText('', key='cpf')],
                [psg.Text('Senha:', size=(20, 1)), psg.InputText('', key='password', password_char='*')],
                [psg.Button('Enviar Dados'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window('Cadastrar Parte').Layout(layout_cadastro)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                return self.__controlador.controlador_execucao.interface.tela_cadastro()
            else:
                return values
    
            
    def tela_inicial_parte(self, cadastro):
        while True:
            left_col = [
                [psg.Text(f'Nome: {cadastro.nome}')],
                [psg.Text(f'Advogado padrão: {cadastro.advogado}')]
            ]
            right_col = [
                [psg.Text(f'CPF: {cadastro.cpf}')]
            ]
            layout_inicial = [
                [psg.Text('Bem vindo!')],
                [psg.Column(left_col, element_justification='c', pad=(18,0)), psg.VSeperator(),
                    psg.Column(right_col, element_justification='l')],
                [psg.Button('Editar cadastro', key='editar')],
                [psg.Button('Exibir processos vinculados', key='exibirProcessosVinculados')],
                [psg.Button('Cadastrar processo',key='cadProcesso')],
                [psg.Button('Deslogar')]
            ]
            self.__window = psg.Window('Tela inicial').Layout(layout_inicial)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'editar':
                self.tela_editar_parte(cadastro)
            elif event == 'cadProcesso':
                self.__controlador.criar_processo(cadastro)
            elif event == 'exibirProcessosVinculados':
                self.__controlador.exibir_processos_parte(cadastro)
            elif event == 'Deslogar':
                return self.__controlador.controlador_execucao.interface.tela_inicial()
            elif event == psg.WIN_CLOSED:
                break
            else:
                return values
            
    def tela_editar_parte(self, parte):
        while True:
            layout_altera = [
                [psg.Text('Escolha alteracao a ser feita no parte:')],
                [psg.Radio('Nome     ', "RADIO", default=True, size=(15, 1))],
                [psg.Radio('Senha     ', "RADIO", size=(15, 1))],
                [psg.Radio('Advogado Padrão     ', "RADIO", size=(15, 1))],
                [psg.Button('Enviar'), psg.Button('Voltar')]
            ]
            tela_altera = psg.Window(
                'Alterar Detalhes da parte').Layout(layout_altera)

            event, values = tela_altera.read()
            tela_altera.Close()
            if event == psg.WIN_CLOSED or event == 'Voltar':
                tela_altera.Close()
                return -1
            else:
                if values[0]:
                    layout_nome_alt = [
                        [psg.Text('Novo nome:', pad=(50, 0))],
                        [psg.InputText('', size=(30, 1), pad=(30, 0))],
                        [psg.Button('Enviar', pad=(30, 5))],
                        [psg.Button('Voltar', pad=(0, 5))],
                    ]
                    tela_nome_alt = psg.Window(
                        'Alterar nome').Layout(layout_nome_alt)
                    event_nome_alt, values_dado_alt = tela_nome_alt.read()
                    tela_nome_alt.Close()

                    if event_nome_alt == 'Enviar':
                        if values_dado_alt[0] == '':
                            self.aviso('O campo de Alterar Nome deve ser preenchido')
                            continue
                        self.__controlador.editar_parte(
                            parte, 0, values_dado_alt[0])
                        break
                    else:
                        continue
                
                elif values[1]:
                    layout_senha_alt = [
                        [psg.Text('Nova Senha:', pad=(50, 0))],
                        [psg.InputText('', size=(30, 1), pad=(30, 0))],
                        [psg.Button('Enviar', pad=(30, 5))],
                        [psg.Button('Voltar', pad=(0, 5))],
                    ]
                    tela_senha_alt = psg.Window(
                        'Alterar Senha').Layout(layout_senha_alt)
                    event_senha_alt, values_dado_alt = tela_senha_alt.read()
                    tela_senha_alt.Close()

                    if event_senha_alt == 'Enviar':
                        if values_dado_alt[0] == '':
                            self.aviso(
                                'O campo de Nova Senha deve ser preenchido')
                            continue
                        self.__controlador.editar_parte(
                            parte, 1, values_dado_alt[0])
                        break
                    else:
                        continue
                    
                elif values[2]:
                    layout_senha_alt = [
                        [psg.Text('Novo Advogado:', pad=(50, 0))],
                        [psg.InputText('', size=(30, 1), pad=(30, 0))],
                        [psg.Button('Enviar', pad=(30, 5))],
                        [psg.Button('Voltar', pad=(0, 5))],
                    ]
                    tela_senha_alt = psg.Window(
                        'Alterar Advogado').Layout(layout_senha_alt)
                    event_senha_alt, values_dado_alt = tela_senha_alt.read()
                    tela_senha_alt.Close()

                    if event_senha_alt == 'Enviar':
                        if values_dado_alt[0] == '':
                            self.aviso(
                                'O campo de Novo Advogado deve ser preenchido')
                            continue
                        self.__controlador.editar_parte(
                            parte, 2, values_dado_alt[0])
                        break
                    else:
                        continue
                else:
                    self.aviso('Selecione uma opção válida')
            
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
