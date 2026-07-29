import PySimpleGUI as sg
from telas_crud import (
    tela_cliente, 
    tela_pedido, 
    tela_servico, 
    tela_orcamento, 
    tela_peca, 
    tela_pagamento,
    tela_consultas # <-- Importação da nova tela
)

def menu_principal():
    sg.theme('DarkBlue')
    
    layout = [
        [sg.Text('SISTEMA NOVA DPS INFORMÁTICA', font=('Helvetica', 20, 'bold'))],
        [sg.Text('Selecione o módulo que deseja gerenciar:', font=('Helvetica', 11))],
        [sg.Text('')],
        [sg.Button('1. Clientes', size=(25, 2))],
        [sg.Button('2. Pedidos', size=(25, 2))],
        [sg.Button('3. Serviços', size=(25, 2))],
        [sg.Button('4. Orçamentos', size=(25, 2))],
        [sg.Button('5. Peças', size=(25, 2))],
        [sg.Button('6. Pagamentos', size=(25, 2))],
        [sg.Button('7. Consultas & Relatórios', size=(25, 2), button_color=('white', 'green'))], # <-- Botão de destaque
        [sg.Text('')], 
        [sg.Button('Sair', size=(15, 2), button_color=('white', 'red'))]
    ]

    window = sg.Window('Nova DPS Informática - Menu Principal', layout, element_justification='c')

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        
        if event == '1. Clientes':
            window.hide(); tela_cliente(); window.un_hide()
        elif event == '2. Pedidos':
            window.hide(); tela_pedido(); window.un_hide()
        elif event == '3. Serviços':
            window.hide(); tela_servico(); window.un_hide()
        elif event == '4. Orçamentos':
            window.hide(); tela_orcamento(); window.un_hide()
        elif event == '5. Peças':
            window.hide(); tela_peca(); window.un_hide()
        elif event == '6. Pagamentos':
            window.hide(); tela_pagamento(); window.un_hide()
        elif event == '7. Consultas & Relatórios': # <-- Ação do botão 7
            window.hide(); tela_consultas(); window.un_hide()

    window.close()

if __name__ == '__main__':
    menu_principal()