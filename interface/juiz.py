import PySimpleGUI as psg


class InterfaceJuiz:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

    def tela_cadastrar_juiz(self, cpf):
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os dados abaixo:')],
                [psg.Text('Nome do Juiz', size=(20, 1)),
                 psg.InputText('', key='nome')],
                [psg.Text('Matricula do Juiz', size=(20, 1)),
                 psg.InputText('', key='matricula')],
                [psg.Text(f'Login                                  {cpf}')],
                [psg.Text('Senha', size=(20, 1)), psg.InputText(
                    '', key='password', password_char='*')],
                [psg.Button('Enviar Dados'), psg.Button('Voltar')]
            ]
            self.__window = psg.Window(
                'Cadastrar Juiz').Layout(layout_cadastro)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
            else:
                return values

    def tela_editar_juiz(self, juiz):
        while True:
            layout_altera = [
                [psg.Text('Escolha alteracao a ser feita no juiz:')],
                [psg.Radio('Nome     ', "RADIO", default=True, size=(15, 1))],
                [psg.Radio('Matrícula     ', "RADIO", size=(15, 1))],
                [psg.Radio('CPF    ', "RADIO", size=(15, 1))],
                [psg.Radio('Senha     ', "RADIO", size=(15, 1))],
                [psg.Button('Enviar'), psg.Button('Voltar')]
            ]
            tela_altera = psg.Window(
                'Alterar Detalhes da juiz').Layout(layout_altera)

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
                            self.aviso('O campo de nome deve ser preenchido')
                            continue
                        self.__controlador.editar_juiz(
                            juiz, 0, values_dado_alt[0])
                        break
                    else:
                        continue
                elif values[1]:
                    layout_matricula_alt = [
                        [psg.Text('Nova Matrícula:', pad=(50, 0))],
                        [psg.InputText('', size=(30, 1), pad=(30, 0))],
                        [psg.Button('Enviar', pad=(30, 5))],
                        [psg.Button('Voltar', pad=(0, 5))],
                    ]
                    tela_matricula_alt = psg.Window(
                        'Alterar Matrícula').Layout(layout_matricula_alt)
                    event_matricula_alt, values_dado_alt = tela_matricula_alt.read()
                    tela_matricula_alt.Close()

                    if event_matricula_alt == 'Enviar':
                        if values_dado_alt[0] == '':
                            self.aviso(
                                'O campo de matrícula deve ser preenchido')
                            continue
                        self.__controlador.editar_juiz(
                            juiz, 1, values_dado_alt[0])
                        break
                    else:
                        continue
                elif values[2]:
                    layout_cpf_alt = [
                        [psg.Text('Novo CPF:', pad=(50, 0))],
                        [psg.InputText('', size=(30, 1), pad=(30, 0))],
                        [psg.Button('Enviar', pad=(30, 5))],
                        [psg.Button('Voltar', pad=(0, 5))],
                    ]
                    tela_cpf_alt = psg.Window(
                        'Alterar CPF').Layout(layout_cpf_alt)
                    event_cpf_alt, values_dado_alt = tela_cpf_alt.read()
                    tela_cpf_alt.Close()

                    if event_cpf_alt == 'Enviar':
                        if values_dado_alt[0] == '':
                            self.aviso(
                                'O campo de CPF deve ser preenchido')
                            continue
                        self.__controlador.editar_juiz(
                            juiz, 2, values_dado_alt[0])
                        break
                    else:
                        continue
                elif values[3]:
                    layout_senha_alt = [
                        [psg.Text('Novo Senha:', pad=(50, 0))],
                        [psg.InputText('', size=(30, 1), pad=(30, 0))],
                        [psg.Button('Enviar', pad=(30, 5))],
                        [psg.Button('Voltar', pad=(0, 5))],
                    ]
                    tela_senha_alt = psg.Window(
                        'Alterar CPF').Layout(layout_senha_alt)
                    event_senha_alt, values_dado_alt = tela_senha_alt.read()
                    tela_senha_alt.Close()

                    if event_senha_alt == 'Enviar':
                        if values_dado_alt[0] == '':
                            self.aviso(
                                'O campo de CPF deve ser preenchido')
                            continue
                        self.__controlador.editar_juiz(
                            juiz, 3, values_dado_alt[0])
                        break
                    else:
                        continue
                else:
                   self.aviso('Selecione uma opção válida')
                   
    def tela_mostrar_detalhes_juiz(self, juiz):
        while True:
            if juiz.nome is None:
                nome = ''
            else:
                nome = juiz.nome
            if juiz.matricula is None:
                matricula = ''
            else:
                matricula = juiz.matricula
            if juiz.cpf is None:
                cpf = ''
            else:
                cpf = juiz.cpf
            if juiz.senha is None:
                senha = ''
            else:
                senha = juiz.senha
            left_col = [
                [psg.Text(f'Nome: {nome}')],
                [psg.Text(f'Matricula: {matricula}')]
            ]
            right_col = [
                [psg.Text(f'CPF: {cpf}')],
                [psg.Text(f'Senha: {senha}')]
            ]
            layout_mostrar = [[psg.Text('Dados do juiz:', pad=(130, 5), font='ANY 12', text_color='black')],
                              [psg.Column(left_col, element_justification='c', pad=(18, 0)), psg.VSeperator(),
                               psg.Column(right_col, element_justification='l')],
                              [psg.Button('Editar', pad=(8, 5)), psg.Button('Excluir', pad=(7, 5)), psg.Button('Voltar', pad=(30, 5))]]
            tela_mostrar = psg.Window('Informacoes sobre juiz').Layout(layout_mostrar)
            event, values = tela_mostrar.read()
            tela_mostrar.Close()
            if event != psg.WIN_CLOSED and event != 'Voltar':
                if event == 'Editar':
                    retorno = self.tela_editar_juiz(juiz)
                    if retorno == -1:
                        continue
                elif event == 'Excluir':
                    self.__controlador.remover_juiz(juiz)
            break


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
