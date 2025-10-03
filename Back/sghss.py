# Sistema de Gestão Hospitalar e de Serviços de Saúde (Protótipo Simples)

class Paciente:
    def __init__(self, nome, cpf, idade):
        self.nome = nome
        self.cpf = cpf
        self.idade = idade
        self.historico = []
        self.consultas = []

    def adicionar_historico(self, registro):
        self.historico.append(registro)

    def agendar_consulta(self, consulta):
        self.consultas.append(consulta)

class Profissional:
    def __init__(self, nome, crm, especialidade):
        self.nome = nome
        self.crm = crm
        self.especialidade = especialidade
        self.agenda = []

    def adicionar_consulta(self, consulta):
        self.agenda.append(consulta)

class Consulta:
    def __init__(self, paciente, profissional, data):
        self.paciente = paciente
        self.profissional = profissional
        self.data = data

    def __str__(self):
        return f"Consulta: {self.paciente.nome} com Dr(a). {self.profissional.nome} em {self.data}"

# ---------------- MENU SIMPLES ----------------
pacientes = []
profissionais = []
consultas = []

def cadastrar_paciente():
    nome = input("Nome do paciente: ")
    cpf = input("CPF: ")
    idade = int(input("Idade: "))
    p = Paciente(nome, cpf, idade)
    pacientes.append(p)
    print("Paciente cadastrado com sucesso!")

def cadastrar_profissional():
    nome = input("Nome do profissional: ")
    crm = input("CRM: ")
    esp = input("Especialidade: ")
    prof = Profissional(nome, crm, esp)
    profissionais.append(prof)
    print("Profissional cadastrado com sucesso!")

def agendar_consulta():
    if not pacientes or not profissionais:
        print("Cadastre pacientes e profissionais primeiro.")
        return
    print("\nPacientes disponíveis:")
    for i, p in enumerate(pacientes):
        print(i, p.nome)
    idx_p = int(input("Escolha o paciente: "))

    print("\nProfissionais disponíveis:")
    for i, pr in enumerate(profissionais):
        print(i, pr.nome, "-", pr.especialidade)
    idx_pr = int(input("Escolha o profissional: "))

    data = input("Data da consulta (dd/mm/aaaa): ")
    c = Consulta(pacientes[idx_p], profissionais[idx_pr], data)
    consultas.append(c)
    pacientes[idx_p].agendar_consulta(c)
    profissionais[idx_pr].adicionar_consulta(c)
    print("Consulta agendada com sucesso!")

def listar_consultas():
    if not consultas:
        print("Nenhuma consulta agendada.")
    for c in consultas:
        print(c)

# ---------------- LOOP PRINCIPAL ----------------
while True:
    print("\n--- SGHSS (Protótipo) ---")
    print("1. Cadastrar Paciente")
    print("2. Cadastrar Profissional")
    print("3. Agendar Consulta")
    print("4. Listar Consultas")
    print("0. Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_paciente()
    elif opcao == "2":
        cadastrar_profissional()
    elif opcao == "3":
        agendar_consulta()
    elif opcao == "4":
        listar_consultas()
    elif opcao == "0":
        print("Encerrando o sistema...")
        break
    else:
        print("Opção inválida.")
