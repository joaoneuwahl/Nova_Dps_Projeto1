#  Sistema de Gestão Automatizada - Nova DPS Informática

Este projeto é um Sistema de Gestão de Ordens de Serviço desenvolvido como requisito para a disciplina de **Projeto Integrador I**. O objetivo é automatizar e gerenciar o fluxo de trabalho da assistência técnica **Nova DPS Informática**, desde a entrada do equipamento até o faturamento e entrega.

##  Funcionalidades Implementadas
O sistema conta com uma interface gráfica intuitiva e realiza o controle completo (CRUD) e cruzamento de dados das seguintes áreas:
* **Clientes:** Cadastro e gestão de dados de contato.
* **Pedidos:** Abertura de chamados com modelo do equipamento e relato de falhas.
* **Serviços:** Fila de trabalho técnica e controle de status de reparo.
* **Orçamentos:** Precificação estimada vs. final.
* **Peças:** Rastreabilidade de componentes utilizados por serviço e fornecedor.
* **Pagamentos:** Controle financeiro e formas de pagamento.

**Consultas e Relatórios Operacionais:**
* Fila de Serviços Pendentes (Ordenada por tempo de espera).
* Balanço Financeiro (Valor cobrado vs. Valor pago).
* Rastreabilidade de Peças por Equipamento.

##  Tecnologias Utilizadas
* **Back-end & Lógica:** Python 3
* **Interface Gráfica:** PySimpleGUI
* **Banco de Dados:** PostgreSQL (Relacional)
* **Integração BD:** SQLAlchemy
* **Análise de Dados:** Power BI (Para o Dashboard Gerencial)

##  Equipe Desenvolvedora
* Matheus Ferrari Farias
* Jonny Araujo
* Wellingtton Bezerra de Lima
* João Vitor Carvalho Neuwahl
* Luiz Enrique Silva Souza

##  Como rodar o projeto localmente
1. Clone este repositório.
2. Crie um arquivo `.env` na raiz do projeto com a sua string de conexão: `DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco`
3. Instale as dependências: `pip install PySimpleGUI SQLAlchemy psycopg2-binary python-dotenv`
4. Execute o script SQL no pgAdmin para criar e popular o banco de dados.
5. Rode o arquivo `main.py`.
