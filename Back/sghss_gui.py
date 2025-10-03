import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
import re
from datetime import datetime

# Define o tema e a cor da interface
ctk.set_appearance_mode("light")  # Pode ser "System", "Dark" ou "Light"
ctk.set_default_color_theme("blue")  # Pode ser "blue", "green" ou "dark-blue"

# ---------------- Classes ----------------
class Paciente:
    def __init__(self, nome, cpf, rg, nascimento, idade, endereco, telefone, cep):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.nascimento = nascimento
        self.idade = idade
        self.endereco = endereco
        self.telefone = telefone
        self.cep = cep
        self.consultas = []

class Profissional:
    def __init__(self, nome, crm, especialidade):
        self.nome = nome
        self.crm = crm
        self.especialidade = especialidade
        self.agenda = []

class Consulta:
    def __init__(self, paciente, profissional, data):
        self.paciente = paciente
        self.profissional = profissional
        self.data = data

    def __str__(self):
        return f"{self.data} - {self.paciente.nome} com Dr(a). {self.profissional.nome}"

# ---------------- Dados ----------------
pacientes = []
profissionais = []
consultas = []

# ---------------- Funções auxiliares ----------------
def formatar_cpf(cpf_raw: str) -> str:
    digits = re.sub(r"\D", "", cpf_raw)
    if len(digits) != 11:
        return None
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

def pedir_cpf():
    while True:
        cpf_raw = simpledialog.askstring("Cadastro de Paciente", "CPF (somente números):")
        if cpf_raw is None:
            return None
        cpf_formatado = formatar_cpf(cpf_raw)
        if not cpf_formatado:
            messagebox.showerror("CPF inválido", "Digite 11 dígitos para o CPF.")
            continue
        return cpf_formatado

def formatar_rg(rg_raw: str) -> str:
    digits = re.sub(r"\D", "", rg_raw)
    return digits if digits else None

def pedir_rg():
    while True:
        rg_raw = simpledialog.askstring("Cadastro de Paciente", "RG:")
        if rg_raw is None:
            return None
        rg_formatado = formatar_rg(rg_raw)
        if not rg_formatado:
            messagebox.showerror("RG inválido", "O campo RG não pode ser vazio.")
            continue
        return rg_formatado

def formatar_data(data_raw: str) -> str:
    digits = re.sub(r"\D", "", data_raw)
    if len(digits) != 8:
        return None
    try:
        return datetime.strptime(digits, "%d%m%Y").strftime("%d/%m/%Y")
    except ValueError:
        return None

def pedir_data(mensagem="Data (ddmmaaaa ou dd/mm/aaaa):"):
    while True:
        data_raw = simpledialog.askstring("Cadastro", mensagem)
        if data_raw is None:
            return None
        data_formatada = formatar_data(data_raw)
        if not data_formatada:
            messagebox.showerror("Data inválida", "Digite uma data válida (ex.: 01012000 ou 01/01/2000).")
            continue
        return data_formatada

def formatar_telefone(tel_raw: str) -> str:
    digits = re.sub(r"\D", "", tel_raw)
    if len(digits) not in [10, 11]:
        return None
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"

def pedir_telefone():
    while True:
        tel_raw = simpledialog.askstring("Cadastro de Paciente", "Telefone (com DDD):")
        if tel_raw is None:
            return None
        tel_formatado = formatar_telefone(tel_raw)
        if not tel_formatado:
            messagebox.showerror("Telefone inválido", "Digite um telefone válido (10 ou 11 dígitos, com DDD).")
            continue
        return tel_formatado

def formatar_cep(cep_raw: str) -> str:
    digits = re.sub(r"\D", "", cep_raw)
    if len(digits) != 8:
        return None
    return f"{digits[:5]}-{digits[5:]}"

def pedir_cep():
    while True:
        cep_raw = simpledialog.askstring("Cadastro de Paciente", "CEP (somente números):")
        if cep_raw is None:
            return None
        cep_formatado = formatar_cep(cep_raw)
        if not cep_formatado:
            messagebox.showerror("CEP inválido", "Digite 8 dígitos para o CEP.")
            continue
        return cep_formatado

# ---------------- Funções principais ----------------
def cadastrar_paciente():
    nome = simpledialog.askstring("Cadastro de Paciente", "Nome:")
    if nome is None:
        return
    cpf = pedir_cpf()
    if cpf is None:
        return
    rg = pedir_rg()
    if rg is None:
        return
    nascimento = pedir_data("Data de Nascimento (ddmmaaaa ou dd/mm/aaaa):")
    if nascimento is None:
        return
    idade = simpledialog.askinteger("Cadastro de Paciente", "Idade:")
    if idade is None:
        return
    telefone = pedir_telefone()
    if telefone is None:
        return
    cep = pedir_cep()
    if cep is None:
        return
    endereco = simpledialog.askstring("Cadastro de Paciente", "Endereço completo:")
    if endereco is None:
        return

    p = Paciente(nome, cpf, rg, nascimento, idade, endereco, telefone, cep)
    pacientes.append(p)

    messagebox.showinfo(
        "Sucesso",
        f"Paciente cadastrado!\n\n"
        f"Nome: {nome}\nCPF: {cpf}\nRG: {rg}\nNascimento: {nascimento}\n"
        f"Idade: {idade}\nEndereço: {endereco}\nTelefone: {telefone}\nCEP: {cep}"
    )

def cadastrar_profissional():
    nome = simpledialog.askstring("Cadastro de Profissional", "Nome:")
    crm = simpledialog.askstring("Cadastro de Profissional", "CRM:")
    esp = simpledialog.askstring("Cadastro de Profissional", "Especialidade:")
    if nome and crm and esp:
        pr = Profissional(nome, crm, esp)
        profissionais.append(pr)
        messagebox.showinfo("Sucesso", "Profissional cadastrado com sucesso!")

def agendar_consulta():
    if not pacientes or not profissionais:
        messagebox.showwarning("Atenção", "Cadastre pacientes e profissionais primeiro.")
        return
    
    paciente_nomes = [p.nome for p in pacientes]
    profissional_nomes = [f"{pr.nome} - {pr.especialidade}" for pr in profissionais]

    paciente_idx = simpledialog.askinteger(
        "Agendamento",
        f"Escolha o paciente (0 a {len(pacientes)-1}):\n" + "\n".join(f"{i} - {p}" for i,p in enumerate(paciente_nomes))
    )
    profissional_idx = simpledialog.askinteger(
        "Agendamento",
        f"Escolha o profissional (0 a {len(profissionais)-1}):\n" + "\n".join(f"{i} - {pr}" for i,pr in enumerate(profissional_nomes))
    )
    data = pedir_data("Data da consulta (ddmmaaaa ou dd/mm/aaaa):")

    if paciente_idx is not None and profissional_idx is not None and data:
        c = Consulta(pacientes[paciente_idx], profissionais[profissional_idx], data)
        consultas.append(c)
        pacientes[paciente_idx].consultas.append(c)
        profissionais[profissional_idx].agenda.append(c)
        messagebox.showinfo("Sucesso", f"Consulta agendada para {data}!")

def listar_consultas():
    if not consultas:
        messagebox.showinfo("Consultas", "Nenhuma consulta agendada.")
    else:
        texto = "\n".join(str(c) for c in consultas)
        messagebox.showinfo("Consultas Agendadas", texto)

# --- Funções para exclusão ---
def excluir_paciente():
    if not pacientes:
        messagebox.showinfo("Atenção", "Não há pacientes cadastrados para excluir.")
        return
    
    paciente_nomes = [p.nome for p in pacientes]
    msg = "Escolha o paciente para excluir (0 a {}):\n".format(len(pacientes) - 1)
    msg += "\n".join(f"{i} - {nome}" for i, nome in enumerate(paciente_nomes))
    
    try:
        idx = simpledialog.askinteger("Excluir Paciente", msg)
        if idx is not None and 0 <= idx < len(pacientes):
            paciente_removido = pacientes.pop(idx)
            messagebox.showinfo("Sucesso", f"Paciente '{paciente_removido.nome}' excluído com sucesso.")
        elif idx is not None:
            messagebox.showerror("Erro", "Índice inválido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def excluir_profissional():
    if not profissionais:
        messagebox.showinfo("Atenção", "Não há profissionais cadastrados para excluir.")
        return

    profissional_nomes = [f"{pr.nome} - {pr.especialidade}" for pr in profissionais]
    msg = "Escolha o profissional para excluir (0 a {}):\n".format(len(profissionais) - 1)
    msg += "\n".join(f"{i} - {nome}" for i, nome in enumerate(profissional_nomes))

    try:
        idx = simpledialog.askinteger("Excluir Profissional", msg)
        if idx is not None and 0 <= idx < len(profissionais):
            profissional_removido = profissionais.pop(idx)
            messagebox.showinfo("Sucesso", f"Profissional '{profissional_removido.nome}' excluído com sucesso.")
        elif idx is not None:
            messagebox.showerror("Erro", "Índice inválido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def excluir_consulta():
    if not consultas:
        messagebox.showinfo("Atenção", "Não há consultas agendadas para excluir.")
        return

    consulta_info = [str(c) for c in consultas]
    msg = "Escolha a consulta para excluir (0 a {}):\n".format(len(consultas) - 1)
    msg += "\n".join(f"{i} - {info}" for i, info in enumerate(consulta_info))

    try:
        idx = simpledialog.askinteger("Excluir Consulta", msg)
        if idx is not None and 0 <= idx < len(consultas):
            consulta_removida = consultas.pop(idx)
            messagebox.showinfo("Sucesso", f"Consulta '{consulta_removida}' excluída com sucesso.")
        elif idx is not None:
            messagebox.showerror("Erro", "Índice inválido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# ---------------- Interface CustomTkinter com Gradiente Suave ----------------
# Lista de cores para o efeito (em RGB) para um tema de hospital
hospital_colors_rgb = [
    (173, 216, 230),  # Azul claro
    (240, 248, 255),  # Branco-fantasma
    (240, 240, 240),  # Cinza claro
    (191, 239, 255)   # Azul-celeste
]

color_index = 0
step_count = 0
total_steps = 200  # Quantidade de passos para cada transição

def rgb_to_hex(rgb):
    return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"

def animate_background():
    global color_index, step_count

    step_count += 1
    if step_count > total_steps:
        step_count = 0
        color_index = (color_index + 1) % len(hospital_colors_rgb)

    start_color = hospital_colors_rgb[color_index]
    end_color = hospital_colors_rgb[(color_index + 1) % len(hospital_colors_rgb)]

    # Interpolação de cores
    r = start_color[0] + (end_color[0] - start_color[0]) * (step_count / total_steps)
    g = start_color[1] + (end_color[1] - start_color[1]) * (step_count / total_steps)
    b = start_color[2] + (end_color[2] - start_color[2]) * (step_count / total_steps)

    new_color_hex = rgb_to_hex((r, g, b))
    root.configure(fg_color=new_color_hex)
    
    # Chama a função novamente após 20ms para uma animação fluida
    root.after(20, animate_background)

root = ctk.CTk()
root.title("🏥 SGHSS - Sistema de Gestão Hospitalar")
root.geometry("440x550")

# Inicia a animação de fundo
animate_background()

titulo = ctk.CTkLabel(root, text="SGHSS", font=("Arial", 16, "bold"), text_color="#2196F3")
titulo.pack(pady=10)

# Frame de botões principais
main_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#ffffff")
main_frame.pack(pady=10, padx=20, fill="both", expand=True)

btn1 = ctk.CTkButton(main_frame, text="Cadastrar Paciente", command=cadastrar_paciente)
btn1.pack(pady=6, padx=10, fill="x")

btn2 = ctk.CTkButton(main_frame, text="Cadastrar Profissional", command=cadastrar_profissional)
btn2.pack(pady=6, padx=10, fill="x")

btn3 = ctk.CTkButton(main_frame, text="Agendar Consulta", command=agendar_consulta)
btn3.pack(pady=6, padx=10, fill="x")

btn4 = ctk.CTkButton(main_frame, text="Listar Consultas", command=listar_consultas)
btn4.pack(pady=6, padx=10, fill="x")

# Frame de exclusão
excluir_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#ffffff")
excluir_frame.pack(pady=10, padx=20, fill="both", expand=True)

excluir_titulo = ctk.CTkLabel(excluir_frame, text="Excluir Registros", font=("Arial", 12, "bold"), text_color="#f44336")
excluir_titulo.pack(pady=5)

btn_excluir_paciente = ctk.CTkButton(excluir_frame, text="Excluir Paciente", command=excluir_paciente, fg_color="#f44336", hover_color="#d32f2f")
btn_excluir_paciente.pack(pady=5, padx=10, fill="x")

btn_excluir_profissional = ctk.CTkButton(excluir_frame, text="Excluir Profissional", command=excluir_profissional, fg_color="#f44336", hover_color="#d32f2f")
btn_excluir_profissional.pack(pady=5, padx=10, fill="x")

btn_excluir_consulta = ctk.CTkButton(excluir_frame, text="Excluir Consulta", command=excluir_consulta, fg_color="#f44336", hover_color="#d32f2f")
btn_excluir_consulta.pack(pady=5, padx=10, fill="x")

# Botão de Sair
btn_sair = ctk.CTkButton(root, text="Sair", command=root.quit, fg_color="#555555", hover_color="#333333")
btn_sair.pack(pady=10, padx=20, fill="x")

root.mainloop()