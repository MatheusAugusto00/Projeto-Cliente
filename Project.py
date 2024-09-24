from tkinter import *
from tkinter import ttk
from tkinter import tix
import sqlite3
from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter, A4
#from reportlab.pdfbase import pdfmetrics
import webbrowser

root = tix.Tk()


class Relatorios():
    def printCliente(self):
        webbrowser.open('cliente.pdf')

    def geraRelatCli(self):
        self.c = canvas.Canvas('cliente.pdf')

        self.codRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telRel = self.telefone_entry.get()
        self.cidRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 640, 'Telefone: ')
        self.c.drawString(50, 610, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(125, 700, self.codRel)
        self.c.drawString(115, 670, self.nomeRel)
        self.c.drawString(140, 640, self.telRel)
        self.c.drawString(125, 610, self.cidRel)

        self.c.rect(20, 600, 550, 125, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()


class Func():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("Clientes.bd");
        print("Conectando ao banco de dados")
        self.cursor = self.conn.cursor()

    def desconcta_bd(self):
        self.conn.close();
        print("Desconectando ao banco de dados")

    def monta_tabela(self):

        self.conecta_bd()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );  
        """)

        self.conn.commit();
        print("Banco de dados criado")
        self.desconcta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(f""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                           VALUES(?, ?, ?)""", (self.nome, self.fone, self.cidade))

        self.conn.commit()
        self.desconcta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()

        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
                            ORDER BY nome_cliente ASC; """)

        for i in lista:
            self.listaCli.insert("", END, values=i)

        self.desconcta_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.conn.execute(f""" DELETE FROM clientes WHERE cod = {self.codigo} """)
        self.conn.commit()
        self.desconcta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(f""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
                            WHERE cod = {self.codigo} """, (self.nome, self.fone, self.cidade))
        self.conn.commit()
        self.desconcta_bd()
        self.select_lista()
        self.limpa_tela()

    def buscar_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes 
                            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC """ % nome)
        buscaNomeCli = self.cursor.fetchall()
        for i in buscaNomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconcta_bd()


class App(Func, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.bts_frame1()
        self.list_frame2()
        self.monta_tabela()
        self.select_lista()
        self.menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro dos clientes")
        self.root.configure(background="palegreen4")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=1000, height=800)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame1 = Frame(self.root, bd=4, bg="lightgray", highlightbackground="palegreen", highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = Frame(self.root, bd=4, bg="lightgray", highlightbackground="palegreen", highlightthickness=3)
        self.frame2.place(relx=0.02, rely=0.51, relwidth=0.96, relheight=0.46)

    def bts_frame1(self):
        self.canvas_bt = Canvas(self.frame1, bd=0, bg='black', highlightbackground='gray', highlightthickness=3)
        self.canvas_bt.place(relx=0.19, rely=0.08, relwidth=0.228, relheight=0.16)

        self.bt_limpar = Button(self.frame1, text='Limpar', bg='seagreen4', bd=3, fg='white', command=self.limpa_tela,
                                activebackground='seagreen1', activeforeground='black')
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.12)

        self.bt_buscar = Button(self.frame1, text='Buscar', bg='seagreen4', bd=3, fg='white',
                                command=self.buscar_cliente,
                                activebackground='seagreen1', activeforeground='black')
        self.bt_buscar.place(relx=0.31, rely=0.1, relwidth=0.1, relheight=0.12)

        self.balao_buscar = tix.Balloon(self.frame1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg='Digite no campo o nome do cliente que deseja pesquisar.')

        self.bt_novo = Button(self.frame1, text='Novo', bg='seagreen4', bd=3, fg='white', command=self.add_cliente,
                              activebackground='seagreen1', activeforeground='black')
        self.bt_novo.place(relx=0.61, rely=0.1, relwidth=0.1, relheight=0.12)

        self.bt_alterar = Button(self.frame1, text='Alterar', bg='seagreen4', bd=3, fg='white',
                                 command=self.altera_cliente,
                                 activebackground='seagreen1', activeforeground='black')
        self.bt_alterar.place(relx=0.72, rely=0.1, relwidth=0.1, relheight=0.12)

        self.bt_apagar = Button(self.frame1, text='Apagar', bg='seagreen4', bd=3, fg='white',
                                command=self.deleta_cliente,
                                activebackground='seagreen1', activeforeground='black')
        self.bt_apagar.place(relx=0.83, rely=0.1, relwidth=0.1, relheight=0.12)

        self.lb_codigo = Label(self.frame1, text='Codigo', bg='lightgray')
        self.lb_codigo.place(relx=0.008, rely=0.01)

        self.codigo_entry = Entry(self.frame1)
        self.codigo_entry.place(relx=0.008, rely=0.1, relwidth=0.1)

        self.lb_nome = Label(self.frame1, text='Nome', bg='lightgray')
        self.lb_nome.place(relx=0.008, rely=0.31)

        self.nome_entry = Entry(self.frame1)
        self.nome_entry.place(relx=0.008, rely=0.4, relwidth=0.8)

        self.lb_telefone = Label(self.frame1, text='Telefone', bg='lightgray')
        self.lb_telefone.place(relx=0.008, rely=0.61)

        self.telefone_entry = Entry(self.frame1)
        self.telefone_entry.place(relx=0.008, rely=0.7, relwidth=0.3)

        self.lb_cidade = Label(self.frame1, text='Cidade', bg='lightgray')
        self.lb_cidade.place(relx=0.5, rely=0.61)

        self.cidade_entry = Entry(self.frame1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.308)

    def list_frame2(self):
        self.listaCli = ttk.Treeview(self.frame2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Codigo')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')

        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=125)
        self.listaCli.column('#4', width=125)

        self.listaCli.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.85)

        self.scroolista = Scrollbar(self.frame2, orient='vertical')
        self.listaCli.configure(yscrollcommand=self.scroolista.set)
        self.scroolista.place(relx=0.96, rely=0.05, relwidth=0.03, relheight=0.85)

        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def quit():
            self.root.destroy()

        menubar.add_cascade(label='Opções', menu=filemenu)
        menubar.add_cascade(label='Relatorios', menu=filemenu2)

        filemenu.add_command(label='sair', command=quit)
        filemenu.add_command(label='Limpar texto', command=self.limpa_tela)

        filemenu2.add_command(label='Ficha do cliente', command=self.geraRelatCli)


App()
