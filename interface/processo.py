import PySimpleGUI as psg

class InterfaceProcesso:

    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None
    

    def tela_cadastrar_processo(self, usuario):
        settings = psg.UserSettings()
        psg.user_settings_filename(path='.')
        while True:
            layout_cadastro = [
                [psg.Text('Preencha os campos abaixo:')],
                [psg.Text('CPF do Autor:', size=(20, 1)), psg.InputText('', key='autor')],
                [psg.Text('OAB do Advogado Autor:', size=(20, 1)), psg.InputText('', key='codOAB_advogado_autor')],
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
                return self.__controlador.controlador_execucao.init_module_inicial_parte(usuario)
            else:
                settings['-filename-'] = values['-IN-']
                return values
            
    def tela_processos_vinculados(self, processos_vinculados):
        while True:
            layout_processos_vinculados = []
            for processo in processos_vinculados:
                item = [psg.Text(f'ID do Processo: {processo.id_processo}'), psg.Text(f'Matrícula do Juiz: {processo.juiz}'), psg.Button('Vizualizar', key=f'{processo.id_processo}')]
                frame = [psg.Frame('', [item])]
                layout_processos_vinculados.append(frame)
                
            layout = [
                [psg.Text('Processos vinculados:')],
                layout_processos_vinculados,
                [psg.Button('Voltar')]
            ]            
            self.__window = psg.Window('Processos Vinculados').Layout(layout)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == psg.WIN_CLOSED:
                break
            else:
                return event                

    def tela_todos_processos(self, todos_processos):
        while True:
            headings = ['ID Processo', 'Matrícula Juiz', 'OAB Advogado Autor', '             ']
            header = [[psg.Text('  ')] + [psg.Text(h, size=(17,1)) for h in headings]]
            rows = [[psg.Text(processo.id_processo, size=(22,1), pad=(0,0)), psg.Text(processo.juiz, size=(22,1), pad=(0,0)), psg.Text(processo.codOAB_advogado_autor, size=(22,1), pad=(0,0)), psg.Button('Visualizar')] for processo in todos_processos]
            layout_todos_processos = header + rows      
            layout = [
                [psg.Text('Todos os Processos cadastrados')],
                layout_todos_processos,
                [psg.Button('Voltar')]
            ]            
            self.__window = psg.Window('Todos Processos Cadastrados').Layout(layout)
            event, values = self.__window.Read()
            self.__window.Close()
            if event == 'Voltar' or event == psg.WIN_CLOSED:
                break
    
    def tela_processo(self, usuario, processo):
        settings = psg.UserSettings()
        psg.user_settings_filename(path='.')        

        parte1 = [[psg.Text(f'Parte autora: {processo.autor}', size=(20, 1))],
                    [psg.Text(f'Advogado da parte autora: {processo.codOAB_advogado_autor}', size=(20, 1))]] 
        
        parte2 = [[psg.Text(f'Parte ré: {processo.reu}', size=(20, 1))],
                    [psg.Text(f'Advogado da parte ré: {processo.codOAB_advogado_reu}', size=(20, 1))]]

        layout_cadastro = [
            [psg.Text(f'Processo n. {processo.id_processo}')],
            [psg.Column(parte1, vertical_alignment='t'), psg.Column(parte2)],
            [psg.Listbox([self.__controlador.andamentoProcesso(processo)], s=(20,10), key='in-ato'), psg.Button('->'), psg.Output(s=(40,10), key='out-ato')],
            [psg.Button('ok'), psg.Button('Voltar')]
        ]
        
        while True:
            self.__window = psg.Window('Acompanhamento processual', element_justification='center').Layout(layout_cadastro)
            event, values = self.__window.Read()
            texto = self.__controlador.abrirDocumento(values['in-ato'][0][0], processo)
            print(texto)           
            if event == 'Voltar':
                return self.__controlador.controlador_execucao.init_module_inicial_parte(usuario)

        self.__window.Close()

            # else:
            #     settings['-filename-'] = values['-IN-']
            #     return values
    
    def teste(self):

        layout = [ [psg.Text('Your typed chars appear here:'), psg.Text('', key='_OUTPUT_')],
            [psg.Input(do_not_clear=True, key='_IN_')],
            [psg.Output(size=(80, 20), key='_OUT_')],
            [psg.Button('Show'), psg.Button('Exit')]
        ]
        window = psg.Window('Window Title').Layout(layout).Finalize()

        # Make the Output Element "read only"
        window.Element('_OUT_')._TKOut.output.bind("<Key>", lambda e: "break")

        while True:             # Event Loop
            event, values = window.Read()
            print(event, values)
            if event is None or event == 'Exit':
                break
            if event == 'Show':
                # change the "output" element to be the value of "input" element
                window.FindElement('_OUTPUT_').Update(values['_IN_'])
        window.Close()
                    


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
