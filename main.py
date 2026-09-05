import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import calendar

ARQUIVO = "contas.txt"
ARQUIVO_SALDO = "saldo.txt"

saldo_disponivel = 0.0


# ==========================================================
# FORMATAÇÃO DE VALORES
# ==========================================================

def formatar_valor(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_valor_campo(valor):
    return (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def converter_valor(texto):
    try:
        return float(
            str(texto)
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
    except ValueError:
        return None


def formatar_campo_moeda(event):
    campo = event.widget

    texto = campo.get()

    numeros = ""

    for caractere in texto:
        if caractere.isdigit():
            numeros += caractere

    if not numeros:
        campo.delete(0, tk.END)
        return

    numeros = numeros[:15]

    valor = int(numeros) / 100

    texto_formatado = (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    campo.delete(0, tk.END)
    campo.insert(0, texto_formatado)


# ==========================================================
# DICAS
# ==========================================================

def criar_dica(campo, texto):

    dica = tk.Toplevel(janela)

    dica.withdraw()
    dica.overrideredirect(True)

    tk.Label(
        dica,
        text=texto,
        bg="#ffffcc",
        fg="#333333",
        relief="solid",
        borderwidth=1,
        padx=6,
        pady=3,
        font=("Arial", 9)
    ).pack()

    def mostrar(event):

        x = event.x_root + 10
        y = event.y_root + 10

        dica.geometry(f"+{x}+{y}")

        dica.deiconify()

    def esconder(event):

        dica.withdraw()

    campo.bind("<Enter>", mostrar)
    campo.bind("<Leave>", esconder)


# ==========================================================
# FORMATAÇÃO DE TEXTO
# ==========================================================

def formatar_texto(event):

    campo = event.widget

    texto = campo.get()

    texto_formatado = ""

    for caractere in texto:

        if caractere.isalpha() or caractere.isspace():

            texto_formatado += caractere.upper()

    if texto != texto_formatado:

        posicao = campo.index(tk.INSERT)

        campo.delete(0, tk.END)

        campo.insert(0, texto_formatado)

        try:
            campo.icursor(posicao)
        except:
            pass


# ==========================================================
# SALDO
# ==========================================================

def salvar_saldo():

    with open(
        ARQUIVO_SALDO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            str(saldo_disponivel)
        )


def carregar_saldo():

    global saldo_disponivel

    try:

        with open(
            ARQUIVO_SALDO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            conteudo = arquivo.read().strip()

            if conteudo:

                saldo_disponivel = float(
                    conteudo
                )

            else:

                saldo_disponivel = 0.0

    except (
        FileNotFoundError,
        ValueError
    ):

        saldo_disponivel = 0.0

    atualizar_saldo()


def atualizar_saldo():

    label_saldo.config(
        text="Disponível para pagar: "
        + formatar_valor(saldo_disponivel)
    )


# ==========================================================
# ALTERAR SALDO
# ==========================================================

def alterar_saldo():

    janela_saldo = tk.Toplevel(janela)

    janela_saldo.title(
        "Alterar Valor Disponível"
    )

    janela_saldo.resizable(
        False,
        False
    )

    janela_saldo.transient(janela)

    janela_saldo.grab_set()


    tk.Label(
        janela_saldo,
        text="Novo valor disponível:",
        font=("Arial", 11, "bold")
    ).pack(
        padx=20,
        pady=(20, 10)
    )


    entrada_saldo = tk.Entry(
        janela_saldo,
        width=25,
        justify="center",
        font=("Arial", 12)
    )

    entrada_saldo.pack(
        padx=20,
        pady=5
    )


    entrada_saldo.insert(
        0,
        formatar_valor_campo(
            saldo_disponivel
        )
    )


    entrada_saldo.bind(
        "<KeyRelease>",
        formatar_campo_moeda
    )


    def salvar_novo_saldo():

        global saldo_disponivel

        valor = converter_valor(
            entrada_saldo.get()
        )

        if valor is None:

            messagebox.showerror(
                "Erro",
                "Digite um valor válido."
            )

            return

        if valor < 0:

            messagebox.showerror(
                "Erro",
                "O valor não pode ser negativo."
            )

            return

        saldo_disponivel = valor

        salvar_saldo()

        atualizar_saldo()

        janela_saldo.destroy()


    tk.Button(
        janela_saldo,
        text="💾 Salvar",
        width=15,
        command=salvar_novo_saldo,
        cursor="hand2"
    ).pack(
        pady=15
    )


# ==========================================================
# ADICIONAR VALOR
# ==========================================================

def adicionar_valor():

    janela_adicionar = tk.Toplevel(janela)

    janela_adicionar.title(
        "Adicionar Valor"
    )

    janela_adicionar.resizable(
        False,
        False
    )

    janela_adicionar.transient(janela)

    janela_adicionar.grab_set()


    tk.Label(
        janela_adicionar,
        text="Valor a adicionar:",
        font=("Arial", 11, "bold")
    ).pack(
        padx=20,
        pady=(20, 10)
    )


    entrada_adicionar = tk.Entry(
        janela_adicionar,
        width=25,
        justify="center",
        font=("Arial", 12)
    )

    entrada_adicionar.pack(
        padx=20,
        pady=5
    )

    entrada_adicionar.focus()


    entrada_adicionar.bind(
        "<KeyRelease>",
        formatar_campo_moeda
    )


    def confirmar_adicao():

        global saldo_disponivel

        valor = converter_valor(
            entrada_adicionar.get()
        )

        if valor is None:

            messagebox.showerror(
                "Erro",
                "Digite um valor válido."
            )

            return

        if valor <= 0:

            messagebox.showerror(
                "Erro",
                "O valor deve ser maior que zero."
            )

            return

        saldo_disponivel += valor

        salvar_saldo()

        atualizar_saldo()

        janela_adicionar.destroy()

        messagebox.showinfo(
            "Sucesso",
            f"{formatar_valor(valor)} "
            "foi adicionado ao saldo."
        )


    tk.Button(
        janela_adicionar,
        text="➕ Adicionar",
        width=15,
        command=confirmar_adicao,
        cursor="hand2"
    ).pack(
        pady=15
    )


# ==========================================================
# CALENDÁRIO
# ==========================================================

def abrir_calendario(campo_data):

    calendario_janela = tk.Toplevel(janela)

    calendario_janela.title(
        "Selecionar Data"
    )

    calendario_janela.resizable(
        False,
        False
    )

    calendario_janela.transient(janela)

    calendario_janela.grab_set()


    hoje = date.today()


    try:

        data_atual = datetime.strptime(
            campo_data.get(),
            "%d/%m/%Y"
        ).date()

    except ValueError:

        data_atual = hoje


    ano_atual = data_atual.year
    mes_atual = data_atual.month


    def selecionar_data(dia):

        data_selecionada = date(
            ano_atual,
            mes_atual,
            dia
        )

        campo_data.delete(
            0,
            tk.END
        )

        campo_data.insert(
            0,
            data_selecionada.strftime(
                "%d/%m/%Y"
            )
        )

        calendario_janela.destroy()


    def mes_anterior():

        nonlocal mes_atual, ano_atual

        mes_atual -= 1

        if mes_atual == 0:

            mes_atual = 12
            ano_atual -= 1

        atualizar_calendario()


    def proximo_mes():

        nonlocal mes_atual, ano_atual

        mes_atual += 1

        if mes_atual == 13:

            mes_atual = 1
            ano_atual += 1

        atualizar_calendario()


    def ir_para_hoje():

        nonlocal mes_atual, ano_atual

        mes_atual = hoje.month
        ano_atual = hoje.year

        atualizar_calendario()


    def atualizar_calendario():

        for widget in frame_dias.winfo_children():

            widget.destroy()


        meses = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro"
        ]


        label_mes.config(
            text=f"{meses[mes_atual]} {ano_atual}"
        )


        dias_semana = [
            "Seg",
            "Ter",
            "Qua",
            "Qui",
            "Sex",
            "Sáb",
            "Dom"
        ]


        for coluna, dia_semana in enumerate(
            dias_semana
        ):

            tk.Label(
                frame_dias,
                text=dia_semana,
                width=5,
                font=("Arial", 9, "bold")
            ).grid(
                row=0,
                column=coluna,
                padx=2,
                pady=5
            )


        semanas = calendar.monthcalendar(
            ano_atual,
            mes_atual
        )


        for linha, semana in enumerate(
            semanas,
            start=1
        ):

            for coluna, dia in enumerate(
                semana
            ):

                if dia == 0:
                    continue

                tk.Button(
                    frame_dias,
                    text=str(dia),
                    width=5,
                    command=lambda d=dia:
                        selecionar_data(d),
                    cursor="hand2"
                ).grid(
                    row=linha,
                    column=coluna,
                    padx=2,
                    pady=2
                )


    frame_cabecalho = tk.Frame(
        calendario_janela
    )

    frame_cabecalho.pack(
        pady=10
    )


    tk.Button(
        frame_cabecalho,
        text="◀",
        width=3,
        command=mes_anterior,
        cursor="hand2"
    ).pack(
        side="left",
        padx=3
    )


    label_mes = tk.Label(
        frame_cabecalho,
        text="",
        font=("Arial", 11, "bold"),
        width=18
    )

    label_mes.pack(
        side="left"
    )


    tk.Button(
        frame_cabecalho,
        text="▶",
        width=3,
        command=proximo_mes,
        cursor="hand2"
    ).pack(
        side="left",
        padx=3
    )


    tk.Button(
        calendario_janela,
        text="Hoje",
        command=ir_para_hoje,
        cursor="hand2"
    ).pack(
        pady=5
    )


    frame_dias = tk.Frame(
        calendario_janela
    )

    frame_dias.pack(
        padx=10,
        pady=5
    )


    atualizar_calendario()


# ==========================================================
# CONTAS
# ==========================================================

def carregar_contas():

    tabela.delete(
        *tabela.get_children()
    )

    try:

        with open(
            ARQUIVO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            for linha in arquivo:

                linha = linha.strip()

                if not linha:
                    continue

                dados = linha.split("|")

                if len(dados) != 5:
                    continue

                descricao = dados[0].upper()
                categoria = dados[1].upper()
                valor = dados[2]
                vencimento = dados[3]
                status = dados[4]

                try:

                    valor_numerico = float(
                        valor
                    )

                except ValueError:

                    continue

                tabela.insert(
                    "",
                    "end",
                    values=(
                        descricao,
                        categoria,
                        formatar_valor(
                            valor_numerico
                        ),
                        vencimento,
                        status
                    )
                )

    except FileNotFoundError:

        with open(
            ARQUIVO,
            "w",
            encoding="utf-8"
        ):
            pass

    atualizar_resumo()


def salvar_contas():

    with open(
        ARQUIVO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        for item in tabela.get_children():

            dados = tabela.item(
                item,
                "values"
            )

            descricao = dados[0].upper()

            categoria = dados[1].upper()

            valor = (
                str(dados[2])
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

            vencimento = dados[3]

            status = dados[4]

            arquivo.write(
                f"{descricao}|"
                f"{categoria}|"
                f"{valor}|"
                f"{vencimento}|"
                f"{status}\n"
            )


# ==========================================================
# LIMPAR CAMPOS
# ==========================================================

def limpar_campos():

    entrada_descricao.delete(
        0,
        tk.END
    )

    entrada_categoria.delete(
        0,
        tk.END
    )

    entrada_valor.delete(
        0,
        tk.END
    )

    entrada_vencimento.delete(
        0,
        tk.END
    )

    entrada_vencimento.insert(
        0,
        date.today().strftime(
            "%d/%m/%Y"
        )
    )

    tabela.selection_remove(
        tabela.selection()
    )


# ==========================================================
# CADASTRAR
# ==========================================================

def cadastrar():

    descricao = (
        entrada_descricao
        .get()
        .strip()
        .upper()
    )

    categoria = (
        entrada_categoria
        .get()
        .strip()
        .upper()
    )

    valor = converter_valor(
        entrada_valor.get()
    )

    vencimento = (
        entrada_vencimento
        .get()
        .strip()
    )


    if not descricao:

        messagebox.showwarning(
            "Atenção",
            "Informe a descrição da conta."
        )

        return


    if not categoria:

        messagebox.showwarning(
            "Atenção",
            "Informe a categoria."
        )

        return


    if valor is None or valor <= 0:

        messagebox.showwarning(
            "Atenção",
            "Informe um valor válido."
        )

        return


    try:

        datetime.strptime(
            vencimento,
            "%d/%m/%Y"
        )

    except ValueError:

        messagebox.showerror(
            "Erro",
            "Digite uma data válida no formato DD/MM/AAAA."
        )

        return


    tabela.insert(
        "",
        "end",
        values=(
            descricao,
            categoria,
            formatar_valor(valor),
            vencimento,
            "Pendente"
        )
    )


    salvar_contas()

    limpar_campos()

    atualizar_resumo()


    messagebox.showinfo(
        "Sucesso",
        "Conta cadastrada com sucesso!"
    )


# ==========================================================
# EDITAR
# ==========================================================

def editar():

    selecionado = tabela.selection()

    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma conta para editar."
        )

        return


    item = selecionado[0]

    dados = tabela.item(
        item,
        "values"
    )


    janela_editar = tk.Toplevel(
        janela
    )

    janela_editar.title(
        "Editar Conta"
    )

    janela_editar.resizable(
        False,
        False
    )

    janela_editar.transient(
        janela
    )

    janela_editar.grab_set()


    tk.Label(
        janela_editar,
        text="Descrição:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )


    entrada_edit_descricao = tk.Entry(
        janela_editar,
        width=35
    )

    entrada_edit_descricao.grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    entrada_edit_descricao.insert(
        0,
        dados[0]
    )

    entrada_edit_descricao.bind(
        "<KeyRelease>",
        formatar_texto
    )


    tk.Label(
        janela_editar,
        text="Categoria:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )


    entrada_edit_categoria = tk.Entry(
        janela_editar,
        width=35
    )

    entrada_edit_categoria.grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

    entrada_edit_categoria.insert(
        0,
        dados[1]
    )

    entrada_edit_categoria.bind(
        "<KeyRelease>",
        formatar_texto
    )


    tk.Label(
        janela_editar,
        text="Valor:"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )


    entrada_edit_valor = tk.Entry(
        janela_editar,
        width=35
    )

    entrada_edit_valor.grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )


    valor_original = converter_valor(
        dados[2]
    )


    entrada_edit_valor.insert(
        0,
        formatar_valor_campo(
            valor_original
        )
    )


    entrada_edit_valor.bind(
        "<KeyRelease>",
        formatar_campo_moeda
    )


    tk.Label(
        janela_editar,
        text="Vencimento:"
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )


    frame_edit_data = tk.Frame(
        janela_editar
    )

    frame_edit_data.grid(
        row=3,
        column=1,
        padx=10,
        pady=8,
        sticky="w"
    )


    entrada_edit_vencimento = tk.Entry(
        frame_edit_data,
        width=28
    )

    entrada_edit_vencimento.pack(
        side="left"
    )

    entrada_edit_vencimento.insert(
        0,
        dados[3]
    )


    tk.Button(
        frame_edit_data,
        text="📅",
        font=("Segoe UI Emoji", 8),
        width=2,
        height=1,
        padx=0,
        pady=0,
        command=lambda:
            abrir_calendario(
                entrada_edit_vencimento
            ),
        cursor="hand2"
    ).pack(
        side="left",
        padx=(3, 0)
    )


    tk.Label(
        janela_editar,
        text="Status:"
    ).grid(
        row=4,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )


    tk.Label(
        janela_editar,
        text=dados[4],
        font=("Arial", 10, "bold")
    ).grid(
        row=4,
        column=1,
        padx=10,
        pady=8,
        sticky="w"
    )


    def salvar_edicao():

        global saldo_disponivel

        nova_descricao = (
            entrada_edit_descricao
            .get()
            .strip()
            .upper()
        )

        nova_categoria = (
            entrada_edit_categoria
            .get()
            .strip()
            .upper()
        )

        novo_valor = converter_valor(
            entrada_edit_valor.get()
        )

        novo_vencimento = (
            entrada_edit_vencimento
            .get()
            .strip()
        )


        if not nova_descricao:

            messagebox.showwarning(
                "Atenção",
                "Informe a descrição."
            )

            return


        if not nova_categoria:

            messagebox.showwarning(
                "Atenção",
                "Informe a categoria."
            )

            return


        if novo_valor is None or novo_valor <= 0:

            messagebox.showwarning(
                "Atenção",
                "Informe um valor válido."
            )

            return


        try:

            datetime.strptime(
                novo_vencimento,
                "%d/%m/%Y"
            )

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite uma data válida."
            )

            return


        status = dados[4]


        if status == "Paga":

            diferenca = (
                novo_valor -
                valor_original
            )

            saldo_disponivel -= diferenca


            if saldo_disponivel < 0:

                confirmar = messagebox.askyesno(
                    "Atenção",
                    "Essa alteração deixará "
                    "o valor disponível negativo.\n\n"
                    "Deseja continuar?"
                )


                if not confirmar:

                    saldo_disponivel += diferenca

                    return


            salvar_saldo()

            atualizar_saldo()


        tabela.item(
            item,
            values=(
                nova_descricao,
                nova_categoria,
                formatar_valor(
                    novo_valor
                ),
                novo_vencimento,
                status
            )
        )


        salvar_contas()

        atualizar_resumo()

        janela_editar.destroy()


        messagebox.showinfo(
            "Sucesso",
            "Conta alterada com sucesso!"
        )


    tk.Button(
        janela_editar,
        text="💾 Salvar Alterações",
        width=20,
        command=salvar_edicao,
        cursor="hand2"
    ).grid(
        row=5,
        column=0,
        columnspan=2,
        pady=20
    )


# ==========================================================
# EXCLUIR
# ==========================================================

def excluir():

    selecionado = tabela.selection()

    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma conta."
        )

        return


    item = selecionado[0]


    confirmar = messagebox.askyesno(
        "Confirmar exclusão",
        "Deseja realmente excluir esta conta?"
    )


    if confirmar:

        tabela.delete(item)

        salvar_contas()

        atualizar_resumo()


# ==========================================================
# MARCAR COMO PAGA
# ==========================================================

def marcar_paga():

    global saldo_disponivel


    selecionado = tabela.selection()


    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma conta."
        )

        return


    item = selecionado[0]

    dados = tabela.item(
        item,
        "values"
    )


    if dados[4] == "Paga":

        messagebox.showinfo(
            "Informação",
            "Esta conta já está marcada como paga."
        )

        return


    valor = converter_valor(
        dados[2]
    )


    if valor is None:
        return


    if saldo_disponivel < valor:

        confirmar = messagebox.askyesno(
            "Saldo insuficiente",
            "O valor disponível é menor "
            "que o valor da conta.\n\n"
            f"Disponível: "
            f"{formatar_valor(saldo_disponivel)}\n"
            f"Conta: "
            f"{formatar_valor(valor)}\n\n"
            "Deseja marcar a conta como paga mesmo assim?"
        )


        if not confirmar:
            return


    saldo_disponivel -= valor

    salvar_saldo()

    atualizar_saldo()


    tabela.item(
        item,
        values=(
            dados[0],
            dados[1],
            dados[2],
            dados[3],
            "Paga"
        )
    )


    salvar_contas()

    atualizar_resumo()


# ==========================================================
# DESMARCAR COMO PAGA
# ==========================================================

def desmarcar_paga():

    global saldo_disponivel


    selecionado = tabela.selection()


    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma conta para desmarcar."
        )

        return


    item = selecionado[0]


    dados = tabela.item(
        item,
        "values"
    )


    if dados[4] != "Paga":

        messagebox.showinfo(
            "Informação",
            "Esta conta não está marcada como paga."
        )

        return


    valor = converter_valor(
        dados[2]
    )


    if valor is None:

        messagebox.showerror(
            "Erro",
            "Não foi possível identificar o valor da conta."
        )

        return


    confirmar = messagebox.askyesno(
        "Desmarcar conta",
        "Deseja realmente desmarcar esta conta como paga?\n\n"
        f"Valor devolvido ao disponível: "
        f"{formatar_valor(valor)}"
    )


    if not confirmar:
        return


    saldo_disponivel += valor

    salvar_saldo()

    atualizar_saldo()


    tabela.item(
        item,
        values=(
            dados[0],
            dados[1],
            dados[2],
            dados[3],
            "Pendente"
        )
    )


    salvar_contas()

    atualizar_resumo()


    messagebox.showinfo(
        "Sucesso",
        "A conta voltou para Pendente.\n\n"
        f"Saldo disponível: "
        f"{formatar_valor(saldo_disponivel)}"
    )


# ==========================================================
# SELEÇÃO
# ==========================================================

def selecionar_conta(event):

    # Selecionar uma conta não preenche os campos.

    return


# ==========================================================
# PESQUISA
# ==========================================================

def pesquisar():

    termo = (
        entrada_pesquisa
        .get()
        .strip()
        .upper()
        .lower()
    )


    tabela.delete(
        *tabela.get_children()
    )


    try:

        with open(
            ARQUIVO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            for linha in arquivo:

                linha = linha.strip()


                if not linha:
                    continue


                dados = linha.split("|")


                if len(dados) != 5:
                    continue


                descricao = dados[0].upper()

                categoria = dados[1].upper()

                valor = dados[2]

                vencimento = dados[3]

                status = dados[4]


                texto = (
                    descricao + " " +
                    categoria + " " +
                    vencimento + " " +
                    status
                ).lower()


                if termo in texto:

                    try:

                        valor_numerico = float(
                            valor
                        )

                    except ValueError:

                        continue


                    tabela.insert(
                        "",
                        "end",
                        values=(
                            descricao,
                            categoria,
                            formatar_valor(
                                valor_numerico
                            ),
                            vencimento,
                            status
                        )
                    )


    except FileNotFoundError:

        pass


    atualizar_resumo()


def mostrar_todas():

    entrada_pesquisa.delete(
        0,
        tk.END
    )

    carregar_contas()


# ==========================================================
# RESUMO
# ==========================================================

def atualizar_resumo():

    total = 0

    pago = 0

    pendente = 0


    for item in tabela.get_children():

        dados = tabela.item(
            item,
            "values"
        )


        valor = converter_valor(
            dados[2]
        )


        if valor is None:
            continue


        total += valor


        if dados[4] == "Paga":

            pago += valor

        else:

            pendente += valor


    label_total.config(
        text=f"Total: {formatar_valor(total)}"
    )


    label_pago.config(
        text=f"Pago: {formatar_valor(pago)}"
    )


    label_pendente.config(
        text=f"Pendente: {formatar_valor(pendente)}"
    )


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

janela = tk.Tk()

janela.title(
    "Sistema de Cadastro de Contas"
)

janela.geometry(
    "950x750"
)

janela.minsize(
    850,
    650
)


# ==========================================================
# TÍTULO
# ==========================================================

titulo = tk.Label(
    janela,
    text="💰 CONTROLE DE CONTAS",
    font=(
        "Arial",
        20,
        "bold"
    )
)

titulo.pack(
    pady=15
)


# ==========================================================
# SALDO DISPONÍVEL
# ==========================================================

frame_saldo = tk.Frame(
    janela
)

frame_saldo.pack(
    fill="x",
    padx=20,
    pady=5
)


label_saldo = tk.Label(
    frame_saldo,
    text="Disponível para pagar: R$ 0,00",
    font=(
        "Arial",
        14,
        "bold"
    )
)

label_saldo.pack(
    side="left"
)


# ==========================================================
# BOTÕES DO SALDO
# ==========================================================

frame_botoes_saldo = tk.Frame(
    frame_saldo
)

frame_botoes_saldo.pack(
    side="right",
    padx=30
)


tk.Button(
    frame_botoes_saldo,
    text="➕ Adicionar",
    command=adicionar_valor,
    cursor="hand2",
    width=18
).pack(
    side="left",
    padx=2
)


tk.Button(
    frame_botoes_saldo,
    text="💰 Alterar",
    command=alterar_saldo,
    cursor="hand2",
    width=18
).pack(
    side="left",
    padx=2
)


# ==========================================================
# FORMULÁRIO
# ==========================================================

frame_formulario = tk.Frame(
    janela
)

frame_formulario.pack(
    padx=20,
    pady=10,
    fill="x"
)


# ==========================================================
# CAMPOS
# ==========================================================

frame_campos = tk.Frame(
    frame_formulario
)

frame_campos.pack(
    side="left",
    anchor="nw"
)


# ==========================================================
# DESCRIÇÃO
# ==========================================================

tk.Label(
    frame_campos,
    text="Descrição:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=6,
    sticky="w"
)


entrada_descricao = tk.Entry(
    frame_campos,
    width=40
)

entrada_descricao.grid(
    row=0,
    column=1,
    padx=5,
    pady=6
)

entrada_descricao.bind(
    "<KeyRelease>",
    formatar_texto
)

criar_dica(
    entrada_descricao,
    "Ex.: Conta de energia"
)


# ==========================================================
# CATEGORIA
# ==========================================================

tk.Label(
    frame_campos,
    text="Categoria:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=6,
    sticky="w"
)


entrada_categoria = tk.Entry(
    frame_campos,
    width=40
)

entrada_categoria.grid(
    row=1,
    column=1,
    padx=5,
    pady=6
)

entrada_categoria.bind(
    "<KeyRelease>",
    formatar_texto
)

criar_dica(
    entrada_categoria,
    "Ex.: Casa"
)


# ==========================================================
# VALOR
# ==========================================================

tk.Label(
    frame_campos,
    text="Valor:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=6,
    sticky="w"
)


entrada_valor = tk.Entry(
    frame_campos,
    width=40
)

entrada_valor.grid(
    row=2,
    column=1,
    padx=5,
    pady=6
)

entrada_valor.bind(
    "<KeyRelease>",
    formatar_campo_moeda
)

criar_dica(
    entrada_valor,
    "Ex.: 150,50"
)


# ==========================================================
# VENCIMENTO
# ==========================================================

tk.Label(
    frame_campos,
    text="Vencimento:"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=6,
    sticky="w"
)


frame_data = tk.Frame(
    frame_campos
)

frame_data.grid(
    row=3,
    column=1,
    padx=5,
    pady=6,
    sticky="w"
)


entrada_vencimento = tk.Entry(
    frame_data,
    width=33
)

entrada_vencimento.pack(
    side="left"
)

entrada_vencimento.insert(
    0,
    date.today().strftime(
        "%d/%m/%Y"
    )
)


criar_dica(
    entrada_vencimento,
    "Formato: DD/MM/AAAA"
)


tk.Button(
    frame_data,
    text="📅",
    font=("Segoe UI Emoji", 8),
    width=2,
    height=1,
    padx=0,
    pady=0,
    command=lambda:
        abrir_calendario(
            entrada_vencimento
        ),
    cursor="hand2"
).pack(
    side="left",
    padx=(3, 0)
)


# ==========================================================
# BOTÕES DO CADASTRO
# ==========================================================

frame_botoes = tk.Frame(
    frame_formulario
)

frame_botoes.pack(
    side="right",
    padx=30,
    anchor="ne"
)


tk.Button(
    frame_botoes,
    text="➕ Cadastrar",
    width=18,
    command=cadastrar,
    cursor="hand2"
).pack(
    pady=4
)


tk.Button(
    frame_botoes,
    text="✏️ Editar",
    width=18,
    command=editar,
    cursor="hand2"
).pack(
    pady=4
)


tk.Button(
    frame_botoes,
    text="🗑️ Excluir",
    width=18,
    command=excluir,
    cursor="hand2"
).pack(
    pady=4
)


# ==========================================================
# BOTÕES MARCAR / DESMARCAR PAGA
# ==========================================================

frame_botoes_pagamento = tk.Frame(
    frame_botoes
)

frame_botoes_pagamento.pack(
    pady=4
)


tk.Button(
    frame_botoes_pagamento,
    text="✅ Marcar Paga",
    width=18,
    command=marcar_paga,
    cursor="hand2"
).pack(
    side="left",
    padx=2
)


tk.Button(
    frame_botoes_pagamento,
    text="↩️ Desmarcar Paga",
    width=18,
    command=desmarcar_paga,
    cursor="hand2"
).pack(
    side="left",
    padx=2
)


# ==========================================================
# TABELA
# ==========================================================

frame_tabela = tk.Frame(
    janela
)

frame_tabela.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


colunas = (
    "descricao",
    "categoria",
    "valor",
    "vencimento",
    "status"
)


tabela = ttk.Treeview(
    frame_tabela,
    columns=colunas,
    show="headings"
)


tabela.heading(
    "descricao",
    text="Descrição"
)

tabela.heading(
    "categoria",
    text="Categoria"
)

tabela.heading(
    "valor",
    text="Valor"
)

tabela.heading(
    "vencimento",
    text="Vencimento"
)

tabela.heading(
    "status",
    text="Status"
)


tabela.column(
    "descricao",
    width=250
)

tabela.column(
    "categoria",
    width=150
)

tabela.column(
    "valor",
    width=120
)

tabela.column(
    "vencimento",
    width=130
)

tabela.column(
    "status",
    width=120
)


tabela.pack(
    fill="both",
    expand=True
)


tabela.bind(
    "<ButtonRelease-1>",
    selecionar_conta
)


# ==========================================================
# PESQUISA
# ==========================================================

frame_pesquisa = tk.Frame(
    janela
)

frame_pesquisa.pack(
    fill="x",
    padx=20,
    pady=8
)


frame_pesquisa_direita = tk.Frame(
    frame_pesquisa
)

frame_pesquisa_direita.pack(
    side="right"
)


tk.Label(
    frame_pesquisa_direita,
    text="Pesquisar:"
).pack(
    side="left",
    padx=5
)


entrada_pesquisa = tk.Entry(
    frame_pesquisa_direita,
    width=30
)

entrada_pesquisa.pack(
    side="left",
    padx=5
)

entrada_pesquisa.bind(
    "<KeyRelease>",
    formatar_texto
)


criar_dica(
    entrada_pesquisa,
    "Ex.: energia"
)


tk.Button(
    frame_pesquisa_direita,
    text="🔎 Pesquisar",
    command=pesquisar,
    cursor="hand2"
).pack(
    side="left",
    padx=5
)


tk.Button(
    frame_pesquisa_direita,
    text="Mostrar Todas",
    command=mostrar_todas,
    cursor="hand2"
).pack(
    side="left",
    padx=5
)


# ==========================================================
# RESUMO
# ==========================================================

frame_resumo = tk.Frame(
    janela
)

frame_resumo.pack(
    pady=10
)


label_total = tk.Label(
    frame_resumo,
    text="Total: R$ 0,00",
    font=(
        "Arial",
        12,
        "bold"
    )
)

label_total.pack(
    side="left",
    padx=20
)


label_pago = tk.Label(
    frame_resumo,
    text="Pago: R$ 0,00",
    font=(
        "Arial",
        12,
        "bold"
    )
)

label_pago.pack(
    side="left",
    padx=20
)


label_pendente = tk.Label(
    frame_resumo,
    text="Pendente: R$ 0,00",
    font=(
        "Arial",
        12,
        "bold"
    )
)

label_pendente.pack(
    side="left",
    padx=20
)


# ==========================================================
# INICIAR
# ==========================================================

carregar_saldo()

carregar_contas()

janela.mainloop()