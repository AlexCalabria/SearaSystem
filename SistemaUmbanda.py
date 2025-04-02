import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from threading import Thread

class SistemaUmbanda:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro - Seara Vertentes")
        self.root.geometry("900x600")
        
        # Configuração do banco de dados
        self.conectar_banco()
        self.criar_tabelas()
        
        # Configuração do estilo
        self.configurar_estilos()
        
        # Tela de login
        self.criar_tela_login()
        
        # Variáveis para controle de usuário
        self.usuario_logado = False
    
    def configurar_estilos(self):
        """Configura estilos visuais para a aplicação"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TEntry', font=('Arial', 10), padding=5)
        style.configure('TCombobox', font=('Arial', 10), padding=5)
        style.configure('Treeview', font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
    def conectar_banco(self):
        """Conecta ao banco de dados SQLite"""
        self.conn = sqlite3.connect('umbanda.db')
        self.cursor = self.conn.cursor()
    
    def criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        # Tabela de membros
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS membros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                endereco TEXT NOT NULL,
                contato TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                sexo TEXT NOT NULL,
                estado_civil TEXT NOT NULL,
                cargo TEXT NOT NULL,
                situacao_profissional TEXT NOT NULL,
                data_entrada TEXT NOT NULL,
                janeiro INTEGER DEFAULT 0,
                fevereiro INTEGER DEFAULT 0,
                marco INTEGER DEFAULT 0,
                abril INTEGER DEFAULT 0,
                maio INTEGER DEFAULT 0,
                junho INTEGER DEFAULT 0,
                julho INTEGER DEFAULT 0,
                agosto INTEGER DEFAULT 0,
                setembro INTEGER DEFAULT 0,
                outubro INTEGER DEFAULT 0,
                novembro INTEGER DEFAULT 0,
                dezembro INTEGER DEFAULT 0
            )
        ''')
        
        # Tabela de usuários (simplificada para login)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        
        # Verifica se existe algum usuário cadastrado
        self.cursor.execute("SELECT COUNT(*) FROM usuarios")
        if self.cursor.fetchone()[0] == 0:
            # Insere um usuário padrão (em produção, isso seria configurado separadamente)
            self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ('admin', 'admin123'))
            self.conn.commit()
    
    def criar_tela_login(self):
        """Cria a tela de login"""
        self.limpar_tela()
        
        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(login_frame, text="Usuário:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.usuario_entry = ttk.Entry(login_frame, font=('Arial', 12))
        self.usuario_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Senha:", font=('Arial', 12)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.senha_entry = ttk.Entry(login_frame, show="*", font=('Arial', 12))
        self.senha_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(login_frame, text="Entrar", command=self.validar_login).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configuração para pressionar Enter
        self.usuario_entry.bind('<Return>', lambda event: self.senha_entry.focus())
        self.senha_entry.bind('<Return>', lambda event: self.validar_login())
    
    def validar_login(self):
        """Valida as credenciais do usuário"""
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        
        self.cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = self.cursor.fetchone()
        
        if resultado:
            self.usuario_logado = True
            self.criar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")
    
    def limpar_tela(self):
        """Remove todos os widgets da tela"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def criar_tela_principal(self):
        """Cria a tela principal com abas de navegação"""
        self.limpar_tela()
        
        # Cria o notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba de cadastro
        self.criar_aba_cadastro()
        
        # Aba de pesquisa
        self.criar_aba_pesquisa()
        
        # Botão de logout
        ttk.Button(self.root, text="Sair", command=self.fazer_logout).pack(side='bottom', pady=10)
    
    def criar_aba_cadastro(self):
        """Cria a aba de cadastro de novos membros"""
        frame_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(frame_cadastro, text="Novo Cadastro")
        
        # Variáveis para os campos
        self.nome_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.endereco_var = tk.StringVar()
        self.contato_var = tk.StringVar()
        self.data_nascimento_var = tk.StringVar()
        self.sexo_var = tk.StringVar()
        self.estado_civil_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.situacao_profissional_var = tk.StringVar()
        self.data_entrada_var = tk.StringVar()
        
        # Dicionário de opções para combobox
        self.opcoes = {
            'sexo': ['Masculino', 'Feminino'],
            'estado_civil': ['Solteiro', 'Casado'],
            'situacao_profissional': ['Empregado', 'Desempregado'],
            'cargo': ['Médium', 'Cambono', 'Ogã', 'Chefia']
        }
        
        # Layout dos campos
        campos = [
            ("Nome:", self.nome_var, None),
            ("Email:", self.email_var, None),
            ("Endereço:", self.endereco_var, None),
            ("Contato:", self.contato_var, None),
            ("Data de Nascimento:", self.data_nascimento_var, None),
            ("Sexo:", self.sexo_var, self.opcoes['sexo']),
            ("Estado Civil:", self.estado_civil_var, self.opcoes['estado_civil']),
            ("Cargo:", self.cargo_var, self.opcoes['cargo']),
            ("Situação Profissional:", self.situacao_profissional_var, self.opcoes['situacao_profissional']),
            ("Data de Entrada:", self.data_entrada_var, None)
        ]
        
        for i, (label, var, opcoes) in enumerate(campos):
            ttk.Label(frame_cadastro, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if opcoes:
                # Combobox para campos com opções pré-definidas
                combobox = ttk.Combobox(frame_cadastro, textvariable=var, values=opcoes, state='readonly')
                combobox.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                var.set(opcoes[0])  # Define o valor padrão
            else:
                # Entry para campos de texto livre
                entry = ttk.Entry(frame_cadastro, textvariable=var)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        
        # Botão de salvar
        ttk.Button(frame_cadastro, text="Salvar", command=self.salvar_cadastro).grid(row=len(campos), column=0, columnspan=2, pady=10)
        
        # Configurar colunas para expansão
        frame_cadastro.columnconfigure(1, weight=1)
    
    def salvar_cadastro(self):
        """Salva um novo cadastro no banco de dados"""
        # Verifica se todos os campos estão preenchidos
        campos_obrigatorios = [
            (self.nome_var, "Nome"),
            (self.email_var, "Email"),
            (self.endereco_var, "Endereço"),
            (self.contato_var, "Contato"),
            (self.data_nascimento_var, "Data de Nascimento"),
            (self.sexo_var, "Sexo"),
            (self.estado_civil_var, "Estado Civil"),
            (self.cargo_var, "Cargo"),
            (self.situacao_profissional_var, "Situação Profissional"),
            (self.data_entrada_var, "Data de Entrada")
        ]
        
        for var, nome_campo in campos_obrigatorios:
            if not var.get().strip():
                messagebox.showerror("Erro", f"O campo {nome_campo} é obrigatório!")
                return
        
        try:
            # Insere no banco de dados
            self.cursor.execute('''
                INSERT INTO membros (
                    nome, email, endereco, contato, data_nascimento, sexo, 
                    estado_civil, cargo, situacao_profissional, data_entrada
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.nome_var.get(),
                self.email_var.get(),
                self.endereco_var.get(),
                self.contato_var.get(),
                self.data_nascimento_var.get(),
                self.sexo_var.get(),
                self.estado_civil_var.get(),
                self.cargo_var.get(),
                self.situacao_profissional_var.get(),
                self.data_entrada_var.get()
            ))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro salvo com sucesso!")
            self.limpar_campos_cadastro()
            self.atualizar_treeview()  # Atualiza a lista na aba de pesquisa
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados: {e}")
    
    def limpar_campos_cadastro(self):
        """Limpa todos os campos do formulário de cadastro"""
        self.nome_var.set("")
        self.email_var.set("")
        self.endereco_var.set("")
        self.contato_var.set("")
        self.data_nascimento_var.set("")
        self.sexo_var.set(self.opcoes['sexo'][0])
        self.estado_civil_var.set(self.opcoes['estado_civil'][0])
        self.cargo_var.set(self.opcoes['cargo'][0])
        self.situacao_profissional_var.set(self.opcoes['situacao_profissional'][0])
        self.data_entrada_var.set("")
    
    def criar_aba_pesquisa(self):
        """Cria a aba de pesquisa e visualização de membros"""
        frame_pesquisa = ttk.Frame(self.notebook)
        self.notebook.add(frame_pesquisa, text="Pesquisa")
        
        # Frame de pesquisa
        frame_filtros = ttk.Frame(frame_pesquisa)
        frame_filtros.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_filtros, text="Pesquisar por nome:").pack(side='left', padx=5)
        self.pesquisa_var = tk.StringVar()
        pesquisa_entry = ttk.Entry(frame_filtros, textvariable=self.pesquisa_var)
        pesquisa_entry.pack(side='left', padx=5, fill='x', expand=True)
        pesquisa_entry.bind('<KeyRelease>', lambda event: self.atualizar_treeview())
        
        # Treeview para exibir os membros
        frame_treeview = ttk.Frame(frame_pesquisa)
        frame_treeview.pack(fill='both', expand=True, padx=5, pady=5)
        
        colunas = ('nome', 'email', 'cargo', 'situacao', 'pagamentos')
        self.treeview = ttk.Treeview(frame_treeview, columns=colunas, show='headings')
        
        # Configuração das colunas
        self.treeview.heading('nome', text='Nome')
        self.treeview.heading('email', text='Email')
        self.treeview.heading('cargo', text='Cargo')
        self.treeview.heading('situacao', text='Situação Profissional')
        self.treeview.heading('pagamentos', text='Pagamentos')
        
        self.treeview.column('nome', width=150)
        self.treeview.column('email', width=150)
        self.treeview.column('cargo', width=100)
        self.treeview.column('situacao', width=100)
        self.treeview.column('pagamentos', width=150)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame_treeview, orient='vertical', command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.treeview.pack(side='left', fill='both', expand=True)
        
        # Botões de ação
        frame_botoes = ttk.Frame(frame_pesquisa)
        frame_botoes.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(frame_botoes, text="Editar", command=self.editar_membro).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Remover", command=self.remover_membro).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Visualizar", command=self.visualizar_membro).pack(side='left', padx=5)
        
        # Preenche a treeview
        self.atualizar_treeview()
    
    def atualizar_treeview(self):
        """Atualiza a treeview com os membros cadastrados"""
        # Limpa a treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Obtém o termo de pesquisa
        termo_pesquisa = self.pesquisa_var.get().strip()
        
        # Consulta o banco de dados
        if termo_pesquisa:
            self.cursor.execute("SELECT id, nome, email, cargo, situacao_profissional FROM membros WHERE nome LIKE ?", 
                               (f"%{termo_pesquisa}%",))
        else:
            self.cursor.execute("SELECT id, nome, email, cargo, situacao_profissional FROM membros")
        
        membros = self.cursor.fetchall()
        
        # Adiciona os membros à treeview
        for membro in membros:
            id_membro, nome, email, cargo, situacao = membro
            
            # Obtém o status de pagamento (simplificado para exemplo)
            self.cursor.execute("SELECT janeiro, fevereiro, marco, abril, maio, junho, julho, agosto, setembro, outubro, novembro, dezembro FROM membros WHERE id = ?", (id_membro,))
            pagamentos = self.cursor.fetchone()
            meses_pagos = sum(pagamentos)
            status_pagamento = f"{meses_pagos}/12 meses pagos"
            
            self.treeview.insert('', 'end', values=(nome, email, cargo, situacao, status_pagamento), iid=id_membro)
    
    def editar_membro(self):
        """Abre a janela de edição para o membro selecionado"""
        selecionado = self.treeview.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para editar")
            return
        
        id_membro = selecionado
        self.abrir_janela_edicao(id_membro)
    
    def abrir_janela_edicao(self, id_membro):
        """Abre uma janela para edição dos dados do membro"""
        # Obtém os dados do membro
        self.cursor.execute("SELECT * FROM membros WHERE id = ?", (id_membro,))
        membro = self.cursor.fetchone()
        
        if not membro:
            messagebox.showerror("Erro", "Membro não encontrado")
            return
        
        # Cria a janela de edição
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Membro")
        janela_edicao.geometry("500x600")
        
        # Variáveis para os campos
        nome_var = tk.StringVar(value=membro[1])
        email_var = tk.StringVar(value=membro[2])
        endereco_var = tk.StringVar(value=membro[3])
        contato_var = tk.StringVar(value=membro[4])
        data_nascimento_var = tk.StringVar(value=membro[5])
        sexo_var = tk.StringVar(value=membro[6])
        estado_civil_var = tk.StringVar(value=membro[7])
        cargo_var = tk.StringVar(value=membro[8])
        situacao_profissional_var = tk.StringVar(value=membro[9])
        data_entrada_var = tk.StringVar(value=membro[10])
        
        # Layout dos campos
        campos = [
            ("Nome:", nome_var, None),
            ("Email:", email_var, None),
            ("Endereço:", endereco_var, None),
            ("Contato:", contato_var, None),
            ("Data de Nascimento:", data_nascimento_var, None),
            ("Sexo:", sexo_var, self.opcoes['sexo']),
            ("Estado Civil:", estado_civil_var, self.opcoes['estado_civil']),
            ("Cargo:", cargo_var, self.opcoes['cargo']),
            ("Situação Profissional:", situacao_profissional_var, self.opcoes['situacao_profissional']),
            ("Data de Entrada:", data_entrada_var, None)
        ]
        
        for i, (label, var, opcoes) in enumerate(campos):
            ttk.Label(janela_edicao, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if opcoes:
                combobox = ttk.Combobox(janela_edicao, textvariable=var, values=opcoes, state='readonly')
                combobox.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            else:
                entry = ttk.Entry(janela_edicao, textvariable=var)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        
        # Frame para os checkboxes de pagamento
        frame_pagamentos = ttk.LabelFrame(janela_edicao, text="Pagamentos Mensais")
        frame_pagamentos.grid(row=len(campos), column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
        meses = [
            ("Janeiro", 11), ("Fevereiro", 12), ("Março", 13), ("Abril", 14),
            ("Maio", 15), ("Junho", 16), ("Julho", 17), ("Agosto", 18),
            ("Setembro", 19), ("Outubro", 20), ("Novembro", 21), ("Dezembro", 22)
        ]
        
        # Variáveis para os checkboxes
        check_vars = []
        
        for i, (mes, idx) in enumerate(meses):
            var = tk.IntVar(value=membro[idx])
            check_vars.append(var)
            ttk.Checkbutton(frame_pagamentos, text=mes, variable=var).grid(row=i//3, column=i%3, sticky='w', padx=5, pady=2)
        
        # Botões de ação
        frame_botoes = ttk.Frame(janela_edicao)
        frame_botoes.grid(row=len(campos)+1, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botoes, text="Salvar", command=lambda: self.salvar_edicao(
            id_membro, nome_var, email_var, endereco_var, contato_var, 
            data_nascimento_var, sexo_var, estado_civil_var, cargo_var, 
            situacao_profissional_var, data_entrada_var, check_vars, janela_edicao
        )).pack(side='left', padx=5)
        
        ttk.Button(frame_botoes, text="Cancelar", command=janela_edicao.destroy).pack(side='left', padx=5)
        
        # Configurar colunas para expansão
        janela_edicao.columnconfigure(1, weight=1)
    
    def salvar_edicao(self, id_membro, nome_var, email_var, endereco_var, contato_var, 
                     data_nascimento_var, sexo_var, estado_civil_var, cargo_var, 
                     situacao_profissional_var, data_entrada_var, check_vars, janela):
        """Salva as alterações feitas no membro"""
        # Verifica campos obrigatórios
        campos_obrigatorios = [
            (nome_var, "Nome"),
            (email_var, "Email"),
            (endereco_var, "Endereço"),
            (contato_var, "Contato"),
            (data_nascimento_var, "Data de Nascimento"),
            (sexo_var, "Sexo"),
            (estado_civil_var, "Estado Civil"),
            (cargo_var, "Cargo"),
            (situacao_profissional_var, "Situação Profissional"),
            (data_entrada_var, "Data de Entrada")
        ]
        
        for var, nome_campo in campos_obrigatorios:
            if not var.get().strip():
                messagebox.showerror("Erro", f"O campo {nome_campo} é obrigatório!")
                return
        
        try:
            # Atualiza os dados básicos
            self.cursor.execute('''
                UPDATE membros SET
                    nome = ?, email = ?, endereco = ?, contato = ?, 
                    data_nascimento = ?, sexo = ?, estado_civil = ?, 
                    cargo = ?, situacao_profissional = ?, data_entrada = ?
                WHERE id = ?
            ''', (
                nome_var.get(),
                email_var.get(),
                endereco_var.get(),
                contato_var.get(),
                data_nascimento_var.get(),
                sexo_var.get(),
                estado_civil_var.get(),
                cargo_var.get(),
                situacao_profissional_var.get(),
                data_entrada_var.get(),
                id_membro
            ))
            
            # Atualiza os pagamentos
            meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 
                    'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
            
            for i, var in enumerate(check_vars):
                self.cursor.execute(f"UPDATE membros SET {meses[i]} = ? WHERE id = ?", (var.get(), id_membro))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            janela.destroy()
            self.atualizar_treeview()
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar no banco de dados: {e}")
    
    def remover_membro(self):
        """Remove o membro selecionado"""
        selecionado = self.treeview.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para remover")
            return
        
        id_membro = selecionado
        
        # Confirmação
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este membro?"):
            return
        
        try:
            self.cursor.execute("DELETE FROM membros WHERE id = ?", (id_membro,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Membro removido com sucesso!")
            self.atualizar_treeview()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao remover do banco de dados: {e}")
    
    def visualizar_membro(self):
        """Abre uma janela com os detalhes completos do membro"""
        selecionado = self.treeview.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para visualizar")
            return
        
        id_membro = selecionado
        
        # Obtém os dados do membro
        self.cursor.execute("SELECT * FROM membros WHERE id = ?", (id_membro,))
        membro = self.cursor.fetchone()
        
        if not membro:
            messagebox.showerror("Erro", "Membro não encontrado")
            return
        
        # Cria a janela de visualização
        janela_visualizacao = tk.Toplevel(self.root)
        janela_visualizacao.title(f"Detalhes - {membro[1]}")
        janela_visualizacao.geometry("500x600")
        
        # Dados básicos
        frame_dados = ttk.LabelFrame(janela_visualizacao, text="Dados Pessoais")
        frame_dados.pack(fill='x', padx=5, pady=5)
        
        campos = [
            ("Nome:", membro[1]),
            ("Email:", membro[2]),
            ("Endereço:", membro[3]),
            ("Contato:", membro[4]),
            ("Data de Nascimento:", membro[5]),
            ("Sexo:", membro[6]),
            ("Estado Civil:", membro[7]),
            ("Cargo:", membro[8]),
            ("Situação Profissional:", membro[9]),
            ("Data de Entrada:", membro[10])
        ]
        
        for i, (label, valor) in enumerate(campos):
            ttk.Label(frame_dados, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            ttk.Label(frame_dados, text=valor).grid(row=i, column=1, padx=5, pady=2, sticky='w')
        
        # Pagamentos
        frame_pagamentos = ttk.LabelFrame(janela_visualizacao, text="Pagamentos")
        frame_pagamentos.pack(fill='x', padx=5, pady=5)
        
        meses = [
            ("Janeiro", 11), ("Fevereiro", 12), ("Março", 13), ("Abril", 14),
            ("Maio", 15), ("Junho", 16), ("Julho", 17), ("Agosto", 18),
            ("Setembro", 19), ("Outubro", 20), ("Novembro", 21), ("Dezembro", 22)
        ]
        
        for i, (mes, idx) in enumerate(meses):
            status = "Pago" if membro[idx] else "Não pago"
            ttk.Label(frame_pagamentos, text=mes).grid(row=i//3, column=(i%3)*2, padx=5, pady=2, sticky='e')
            ttk.Label(frame_pagamentos, text=status).grid(row=i//3, column=(i%3)*2+1, padx=5, pady=2, sticky='w')
        
        # Botão de fechar
        ttk.Button(janela_visualizacao, text="Fechar", command=janela_visualizacao.destroy).pack(pady=10)
    
    def fazer_logout(self):
        """Realiza o logout do sistema"""
        self.usuario_logado = False
        self.criar_tela_login()
    
    def enviar_email_cobranca(self):
        """Envia emails de cobrança (simulação)"""
        # Esta função seria chamada por um agendador externo
        hoje = datetime.now()
        
        if hoje.day == 3:
            # Lembretes no dia 3
            self.cursor.execute("SELECT email FROM membros")
            emails = [email[0] for email in self.cursor.fetchall()]
            
            for email in emails:
                self.enviar_email(email, "Lembrete de Pagamento", "Por favor, realize o pagamento da mensalidade até o dia 10 deste mês.")
        
        elif hoje.day == 11:
            # Cobrança no dia 11 para inadimplentes do mês atual
            mes_atual = hoje.month
            campo_mes = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 
                        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'][mes_atual - 1]
            
            self.cursor.execute(f"SELECT nome, email FROM membros WHERE {campo_mes} = 0")
            inadimplentes = self.cursor.fetchall()
            
            for nome, email in inadimplentes:
                self.enviar_email(email, "Pagamento Pendente", f"Prezado(a) {nome}, identificamos que o pagamento deste mês ainda não foi realizado. Por favor, regularize sua situação.")
        
        elif hoje.day == 1:
            # Verificação de inadimplência prolongada
            mes_atual = hoje.month
            meses_verificar = [(mes_atual - i - 1) % 12 + 1 for i in range(3)]  # Últimos 3 meses
            
            for membro_id, nome, email in self.cursor.execute("SELECT id, nome, email FROM membros"):
                meses_nao_pagos = 0
                
                for mes in meses_verificar:
                    campo_mes = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 
                                'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'][mes - 1]
                    self.cursor.execute(f"SELECT {campo_mes} FROM membros WHERE id = ?", (membro_id,))
                    if self.cursor.fetchone()[0] == 0:
                        meses_nao_pagos += 1
                
                if meses_nao_pagos == 2:
                    self.enviar_email(email, "Aviso Importante", f"Prezado(a) {nome}, você possui 2 meses de inadimplência. Caso complete 3 meses, será afastado das atividades.")
                elif meses_nao_pagos >= 3:
                    self.enviar_email(email, "Afastamento", f"Prezado(a) {nome}, devido a 3 meses de inadimplência, você está afastado das atividades até regularizar sua situação.")
    
    def enviar_email(self, destinatario, assunto, mensagem):
        """Simula o envio de email (em produção, configurar servidor SMTP real)"""
        print(f"Simulando envio de email para {destinatario}")
        print(f"Assunto: {assunto}")
        print(f"Mensagem: {mensagem}")
        print("-" * 50)
        
        # Em produção, usar algo como:
        # msg = MIMEText(mensagem)
        # msg['Subject'] = assunto
        # msg['From'] = 'seara_vertentes@example.com'
        # msg['To'] = destinatario
        
        # with smtplib.SMTP('smtp.example.com', 587) as server:
        #     server.starttls()
        #     server.login('usuario', 'senha')
        #     server.send_message(msg)
    
    def iniciar_agendador(self):
        """Inicia o agendador de tarefas em segundo plano"""
        # Em produção, usar um agendador real como APScheduler
        print("Agendador iniciado - verificações diárias serão feitas")
        # Esta função verificaria a data e chamaria enviar_email_cobranca quando necessário

def main():
    root = tk.Tk()
    app = SistemaUmbanda(root)
    root.mainloop()

if __name__ == "__main__":
    main()