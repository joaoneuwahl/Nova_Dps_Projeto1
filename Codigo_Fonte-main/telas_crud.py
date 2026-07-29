import PySimpleGUI as sg
from sqlalchemy import text
from conexao_db import engine

# ==========================================
# 1. TELA DE CLIENTES
# ==========================================
def tela_cliente():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('GERENCIAR CLIENTES', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID Cliente (Ex: 21, 22...):'), sg.Input(key='id_cliente', size=(10, 1))],
        [sg.Text('Nome:'), sg.Input(key='nome', size=(40, 1))],
        [sg.Text('Telefone (11 dígitos):'), sg.Input(key='telefone', size=(15, 1))],
        [sg.Text('Email:'), sg.Input(key='email', size=(40, 1))],
        [sg.Button('Salvar'), sg.Button('Listar'), sg.Button('Atualizar'), sg.Button('Excluir'), sg.Button('Voltar')]
    ]
    window = sg.Window('Nova DPS Informática - Clientes', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break
            
        if event == 'Salvar':
            try:
                with engine.begin() as conn:
                    query = text("INSERT INTO cliente (id_cliente, nome, telefone, email) VALUES (:id, :n, :t, :e)")
                    conn.execute(query, {"id": values['id_cliente'], "n": values['nome'], "t": values['telefone'], "e": values['email'] or None})
                sg.popup("Cliente salvo com sucesso!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Listar':
            try:
                with engine.connect() as conn:
                    # ALTERADO: Adicionado 'telefone' na busca do SELECT
                    dados = conn.execute(text("SELECT id_cliente, nome, telefone FROM cliente ORDER BY id_cliente")).fetchall()
                    # ALTERADO: Adicionado o d[2] para printar o telefone de cada um na listagem
                    texto = "\n".join([f"ID: {d[0]} | Nome: {d[1]} | Tel: {d[2]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Vazio.", title="Clientes")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Atualizar':
            # CORRIGIDO: Removido o campo 'endereco' que não existe no layout nem no INSERT
            id_cliente = values['id_cliente'] 
            nome = values['nome']
            telefone = values['telefone']
            email = values['email']
            
            if not id_cliente:
                sg.popup_error("Para atualizar, você precisa digitar o ID do Cliente!")
            else:
                try:
                    with engine.begin() as conn:
                        query = text("""
                            UPDATE cliente 
                            SET nome = :nome, telefone = :telefone, email = :email
                            WHERE id_cliente = :id
                        """)
                        conn.execute(query, {
                            "nome": nome, 
                            "telefone": telefone, 
                            "email": email, 
                            "id": id_cliente
                        })
                    sg.popup("Cliente atualizado com sucesso!")
                except Exception as e:
                    sg.popup_error(f"Erro ao atualizar: {e}")

        if event == 'Excluir':
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM cliente WHERE id_cliente = :id"), {"id": values['id_cliente']})
                sg.popup("Cliente excluído!")
            except Exception as e:
                sg.popup_error(f"Erro ao excluir (verifique se ele tem pedidos): {e}")
    window.close()


# ==========================================
# 2. TELA DE PEDIDOS
# ==========================================
def tela_pedido():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('GERENCIAR PEDIDOS', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID Pedido (Ex: 101, 102...):'), sg.Input(key='id_pedido', size=(10, 1))],
        [sg.Text('ID do Cliente Dono:'), sg.Input(key='id_cliente', size=(10, 1))],
        [sg.Text('Modelo Equipamento:'), sg.Input(key='modelo', size=(40, 1))],
        [sg.Text('Falha:'), sg.Input(key='falha', size=(40, 1))],
        [sg.Text('Status:'), sg.Input(key='status', size=(20, 1))],
        [sg.Text('Data Abertura (AAAA-MM-DD):'), sg.Input(key='data', size=(15, 1))],
        [sg.Button('Salvar'), sg.Button('Listar'), sg.Button('Atualizar'), sg.Button('Excluir'), sg.Button('Voltar')]
    ]
    window = sg.Window('Nova DPS Informática - Pedidos', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break
            
        if event == 'Salvar':
            try:
                with engine.begin() as conn:
                    query = text("""INSERT INTO pedido (id_pedido, id_cliente, modelo_equipamento, descricao_falha, status_pedido, data_abertura) 
                                    VALUES (:id_p, :id_c, :mod, :falha, :st, :dt)""")
                    conn.execute(query, {"id_p": values['id_pedido'], "id_c": values['id_cliente'], "mod": values['modelo'], 
                                         "falha": values['falha'], "st": values['status'], "dt": values['data']})
                sg.popup("Pedido salvo com sucesso!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Listar':
            try:
                with engine.connect() as conn:
                    dados = conn.execute(text("SELECT id_pedido, modelo_equipamento, status_pedido FROM pedido ORDER BY status_pedido, id_pedido")).fetchall()
                    texto = "\n".join([f"Status: {d[2]} | ID: {d[0]} | Modelo: {d[1]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Vazio.", title="Pedidos")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Atualizar':
            id_pedido = values['id_pedido']
            modelo = values['modelo'] # CORRIGIDO: Era values['modelo_equipamento']
            status = values['status'] # CORRIGIDO: Era values['status_pedido']
    
            if not id_pedido:
                sg.popup_error("Digite o ID do Pedido para atualizar!")
            else:
                try:
                    with engine.begin() as conn:
                        query = text("UPDATE pedido SET modelo_equipamento = :modelo, status_pedido = :status WHERE id_pedido = :id")
                        conn.execute(query, {"modelo": modelo, "status": status, "id": id_pedido})
                    sg.popup("Pedido atualizado com sucesso!")
                except Exception as e: 
                    sg.popup_error(f"Erro: {e}")

        if event == 'Excluir':
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM pedido WHERE id_pedido = :id"), {"id": values['id_pedido']})
                sg.popup("Pedido excluído!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")
    window.close()


# ==========================================
# 3. TELA DE SERVIÇOS
# ==========================================
def tela_servico():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('GERENCIAR SERVIÇOS', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID Serviço (Ex: 101, 102...):'), sg.Input(key='id_servico', size=(10, 1))],
        [sg.Text('ID do Pedido:'), sg.Input(key='id_pedido', size=(10, 1))],
        [sg.Text('Tipo de Reparo:'), sg.Input(key='tipo', size=(40, 1))],
        [sg.Text('Status:'), sg.Input(key='status', size=(20, 1))],
        [sg.Button('Salvar'), sg.Button('Listar'), sg.Button('Atualizar'), sg.Button('Excluir'), sg.Button('Voltar')]
    ]
    window = sg.Window('Nova DPS Informática - Serviços', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break
            
        if event == 'Salvar':
            try:
                with engine.begin() as conn:
                    query = text("INSERT INTO servico (id_servico, id_pedido, tipo_reparo, status_servico) VALUES (:id_s, :id_p, :tipo, :st)")
                    conn.execute(query, {"id_s": values['id_servico'], "id_p": values['id_pedido'], "tipo": values['tipo'], "st": values['status']})
                sg.popup("Serviço salvo com sucesso!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Listar':
            try:
                with engine.connect() as conn:
                    dados = conn.execute(text("SELECT id_servico, tipo_reparo, status_servico FROM servico ORDER BY status_servico, id_servico")).fetchall()
                    texto = "\n".join([f"Status: {d[2]} | ID: {d[0]} | Reparo: {d[1]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Vazio.", title="Serviços")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Atualizar':
            id_servico = values['id_servico']
            tipo_reparo = values['tipo'] # CORRIGIDO
            status_servico = values['status'] # CORRIGIDO
    
            if not id_servico:
                sg.popup_error("Digite o ID do Serviço para atualizar!")
            else:
                try:
                    with engine.begin() as conn:
                        query = text("UPDATE servico SET tipo_reparo = :tipo, status_servico = :status WHERE id_servico = :id")
                        conn.execute(query, {"tipo": tipo_reparo, "status": status_servico, "id": id_servico})
                    sg.popup("Serviço atualizado com sucesso!")
                except Exception as e: 
                    sg.popup_error(f"Erro: {e}")

        if event == 'Excluir':
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM servico WHERE id_servico = :id"), {"id": values['id_servico']})
                sg.popup("Serviço excluído!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")
    window.close()


# ==========================================
# 4. TELA DE ORÇAMENTOS
# ==========================================
def tela_orcamento():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('GERENCIAR ORÇAMENTOS', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID Orçamento:'), sg.Input(key='id_orcamento', size=(10, 1))],
        [sg.Text('ID do Serviço:'), sg.Input(key='id_servico', size=(10, 1))],
        [sg.Text('Valor Estimado (Ex: 150.00):'), sg.Input(key='valor', size=(15, 1))],
        [sg.Text('Data (AAAA-MM-DD):'), sg.Input(key='data', size=(15, 1))],
        [sg.Button('Salvar'), sg.Button('Listar'), sg.Button('Atualizar'), sg.Button('Excluir'), sg.Button('Voltar')]
    ]
    window = sg.Window('Nova DPS Informática - Orçamentos', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break
            
        if event == 'Salvar':
            try:
                with engine.begin() as conn:
                    query = text("INSERT INTO orcamento (id_orcamento, id_servico, valor_estimado, data_orcamento) VALUES (:id_o, :id_s, :val, :dt)")
                    conn.execute(query, {"id_o": values['id_orcamento'], "id_s": values['id_servico'], "val": values['valor'], "dt": values['data']})
                sg.popup("Orçamento salvo!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Listar':
            try:
                with engine.connect() as conn:
                    dados = conn.execute(text("SELECT id_orcamento, valor_estimado FROM orcamento")).fetchall()
                    texto = "\n".join([f"ID: {d[0]} | Valor: R$ {d[1]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Vazio.", title="Orçamentos")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Atualizar':
            id_orcamento = values['id_orcamento']
            valor_estimado = values['valor'] # CORRIGIDO
    
            if not id_orcamento:
                sg.popup_error("Digite o ID do Orçamento para atualizar!")
            else:
                try:
                    with engine.begin() as conn:
                        query = text("UPDATE orcamento SET valor_estimado = :est WHERE id_orcamento = :id")
                        conn.execute(query, {"est": valor_estimado, "id": id_orcamento})
                    sg.popup("Orçamento atualizado com sucesso!")
                except Exception as e: 
                    sg.popup_error(f"Erro: {e}")

        if event == 'Excluir':
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM orcamento WHERE id_orcamento = :id"), {"id": values['id_orcamento']})
                sg.popup("Orçamento excluído!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")
    window.close()


# ==========================================
# 5. TELA DE PEÇAS
# ==========================================
def tela_peca():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('GERENCIAR PEÇAS', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID Peça:'), sg.Input(key='id_peca', size=(10, 1))],
        [sg.Text('ID do Orçamento:'), sg.Input(key='id_orcamento', size=(10, 1))],
        [sg.Text('Tipo da Peça:'), sg.Input(key='tipo', size=(30, 1))],
        [sg.Text('Fornecedor:'), sg.Input(key='fornecedor', size=(30, 1))],
        [sg.Text('Custo (Ex: 89.90):'), sg.Input(key='custo', size=(15, 1))],
        [sg.Text('Data Compra (AAAA-MM-DD):'), sg.Input(key='data', size=(15, 1))],
        [sg.Button('Salvar'), sg.Button('Listar'), sg.Button('Atualizar'), sg.Button('Excluir'), sg.Button('Voltar')]
    ]
    window = sg.Window('Nova DPS Informática - Peças', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break
            
        if event == 'Salvar':
            try:
                with engine.begin() as conn:
                    query = text("""INSERT INTO peca (id_peca, id_orcamento, tipo_peca, fornecedor, custo_unitario, data_compra) 
                                    VALUES (:id_p, :id_o, :tipo, :forn, :custo, :dt)""")
                    conn.execute(query, {"id_p": values['id_peca'], "id_o": values['id_orcamento'], "tipo": values['tipo'], 
                                         "forn": values['fornecedor'], "custo": values['custo'], "dt": values['data']})
                sg.popup("Peça salva!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Listar':
            try:
                with engine.connect() as conn:
                    dados = conn.execute(text("SELECT id_peca, tipo_peca FROM peca")).fetchall()
                    texto = "\n".join([f"ID: {d[0]} | Peça: {d[1]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Vazio.", title="Peças")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Atualizar':
            id_peca = values['id_peca']
            tipo_peca = values['tipo'] # CORRIGIDO
            fornecedor = values['fornecedor']
            custo = values['custo'] # CORRIGIDO
    
            if not id_peca:
                sg.popup_error("Digite o ID da Peça para atualizar!")
            else:
                try:
                    with engine.begin() as conn:
                        query = text("UPDATE peca SET tipo_peca = :tipo, fornecedor = :forn, custo_unitario = :custo WHERE id_peca = :id")
                        conn.execute(query, {"tipo": tipo_peca, "forn": fornecedor, "custo": custo, "id": id_peca})
                    sg.popup("Peça atualizada com sucesso!")
                except Exception as e: 
                    sg.popup_error(f"Erro: {e}")

        if event == 'Excluir':
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM peca WHERE id_peca = :id"), {"id": values['id_peca']})
                sg.popup("Peça excluída!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")
    window.close()


# ==========================================
# 6. TELA DE PAGAMENTOS
# ==========================================
def tela_pagamento():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('GERENCIAR PAGAMENTOS', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID Pagamento:'), sg.Input(key='id_pagamento', size=(10, 1))],
        [sg.Text('ID do Orçamento:'), sg.Input(key='id_orcamento', size=(10, 1))],
        [sg.Text('Valor Pago:'), sg.Input(key='valor', size=(15, 1))],
        [sg.Text('Forma de Pagamento (Pix, Cartao...):'), sg.Input(key='forma', size=(20, 1))],
        [sg.Text('Data Pagamento (AAAA-MM-DD):'), sg.Input(key='data', size=(15, 1))],
        [sg.Button('Salvar'), sg.Button('Listar'), sg.Button('Excluir'), sg.Button('Voltar')]
    ]
    window = sg.Window('Nova DPS Informática - Pagamentos', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break
            
        if event == 'Salvar':
            try:
                with engine.begin() as conn:
                    query = text("""INSERT INTO pagamento (id_pagamento, id_orcamento, valor_pago, forma_pagamento, data_pagamento) 
                                    VALUES (:id_p, :id_o, :val, :forma, :dt)""")
                    conn.execute(query, {"id_p": values['id_pagamento'], "id_o": values['id_orcamento'], "val": values['valor'], 
                                         "forma": values['forma'], "dt": values['data']})
                sg.popup("Pagamento salvo!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Listar':
            try:
                with engine.connect() as conn:
                    dados = conn.execute(text("SELECT id_pagamento, valor_pago FROM pagamento")).fetchall()
                    texto = "\n".join([f"ID: {d[0]} | Valor: R$ {d[1]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Vazio.", title="Pagamentos")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        if event == 'Excluir':
            try:
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM pagamento WHERE id_pagamento = :id"), {"id": values['id_pagamento']})
                sg.popup("Pagamento excluído!")
            except Exception as e:
                sg.popup_error(f"Erro: {e}")
    window.close()


# ==========================================
# 7. TELA DE CONSULTAS E RELATÓRIOS (MELHORADA)
# ==========================================
def tela_consultas():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('CONSULTAS E RELATÓRIOS OPERACIONAIS', font=('Helvetica', 14, 'bold'))],
        [sg.Text('Selecione o relatório que deseja emitir:')],
        [sg.Text('')], 
        [sg.Button('Fila de Serviços Pendentes (RF06)', size=(40, 2))], 
        [sg.Button('Balanço Financeiro (Orçamentos vs Pagos)', size=(40, 2))],
        [sg.Button('Rastreabilidade de Peças por Equipamento', size=(40, 2))],
        [sg.Text('')], 
        [sg.Button('Voltar', size=(15, 2))]
    ]
    window = sg.Window('Nova DPS Informática - Relatórios', layout, element_justification='c')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar': break

        # --- CONSULTA 1: SERVIÇOS PENDENTES (Com Status do Serviço) ---
        if event == 'Fila de Serviços Pendentes (RF06)':
            try:
                with engine.connect() as conn:
                    query = text("""
                        SELECT s.id_servico, c.nome, p.modelo_equipamento, s.status_servico, p.data_abertura
                        FROM servico s
                        JOIN pedido p ON s.id_pedido = p.id_pedido
                        JOIN cliente c ON p.id_cliente = c.id_cliente
                        WHERE s.status_servico != 'Concluido'
                        ORDER BY p.data_abertura ASC
                    """)
                    dados = conn.execute(query).fetchall()
                    texto = "\n".join([f"OS: {d[0]} | Cliente: {d[1]} | Equip: {d[2]} | Status: {d[3]} | Aberto em: {d[4]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Nenhum serviço pendente!", title="Fila de Serviços (RF06)", size=(75, 12))
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        # --- CONSULTA 2: BALANÇO FINANCEIRO (Orçamentos vs Pagos com LEFT JOIN) ---
        if event == 'Balanço Financeiro (Orçamentos vs Pagos)':
            try:
                with engine.connect() as conn:
                    query = text("""
                        SELECT o.id_orcamento, o.valor_final, COALESCE(SUM(pg.valor_pago), 0) as total_pago, o.data_orcamento
                        FROM orcamento o
                        LEFT JOIN pagamento pg ON o.id_orcamento = pg.id_orcamento
                        GROUP BY o.id_orcamento, o.valor_final, o.data_orcamento
                        ORDER BY o.data_orcamento DESC
                    """)
                    dados = conn.execute(query).fetchall()
                    texto = "\n".join([f"Orçamento ID: {d[0]} | Valor Final: R${d[1]} | Total Já Pago: R${d[2]} | Data: {d[3]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Nenhum orçamento gerado.", title="Balanço Financeiro", size=(75, 12))
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

        # --- CONSULTA 3: RASTREABILIDADE (Cruzando até chegar ao equipamento) ---
        if event == 'Rastreabilidade de Peças por Equipamento':
            try:
                with engine.connect() as conn:
                    query = text("""
                        SELECT p.id_peca, p.tipo_peca, p.fornecedor, p.custo_unitario, ped.modelo_equipamento
                        FROM peca p
                        JOIN orcamento o ON p.id_orcamento = o.id_orcamento
                        JOIN servico s ON o.id_servico = s.id_servico
                        JOIN pedido ped ON s.id_pedido = ped.id_pedido
                        ORDER BY p.data_compra DESC
                    """)
                    dados = conn.execute(query).fetchall()
                    texto = "\n".join([f"Peça ID: {d[0]} | Nome: {d[1]} | Fornecedor: {d[2]} | Custo: R${d[3]} | Instalada no: {d[4]}" for d in dados])
                    sg.popup_scrolled(texto if texto else "Nenhuma peça utilizada ainda.", title="Rastreabilidade de Peças", size=(75, 12))
            except Exception as e:
                sg.popup_error(f"Erro: {e}")

    window.close()