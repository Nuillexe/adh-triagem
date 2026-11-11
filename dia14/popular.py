import os
import random
import django

# Configura o ambiente do Django para o script rodar avulso
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dia14.settings')  # Substitua 'seu_projeto' pelo nome da pasta principal do seu projeto
django.setup()

from formulario.models import Participate

nomes_base = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", 
    "Igor", "Juliana", "Kleber", "Larissa", "Marcos", "Natália", "Otávio", "Patrícia", 
    "Rafael", "Sabrina", "Thiago", "Vanessa", "Wagner", "Tatiane", "Rodrigo", "Camila",
    "Lucas", "Beatriz", "Matheus", "Mariana", "Felipe", "Amanda", "Diego", "Larissa"
]

sobrenomes_base = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira",
    "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes",
    "Barbosa", "Cardoso", "Rocha", "Dias", "Monteiro", "Teixeira", "Vieira"
]

condicoes_possiveis = ['DM1', 'DM2', 'DM1&HT', 'DM2&HT', 'HT', 'Nenhum']

print("Iniciando a criação de participantes de teste...")

criados = 0
for i in range(35):
    nome = f"{random.choice(nomes_base)} {random.choice(sobrenomes_base)} {i+1}"
    idade = random.randint(20, 85)
    condicao = random.choice(condicoes_possiveis)
    glicemia = random.randint(70, 260)
    
    pressao_alta = random.randint(100, 190)
    pressao_baixa = random.randint(60, 115)
    
    observacao = random.choice([
        "Paciente relata uso regular de medicação.",
        "Sem queixas no momento do atendimento.",
        "Orientado sobre dieta restritiva de açúcar.",
        "Retorno agendado para o próximo mutirão.",
        ""
    ])

    try:
        Participate.objects.create(
            nome=nome,
            idade=idade,
            condicao_saude=condicao,
            glicemia=glicemia,
            pressaoAlta=pressao_alta,
            pressaoBaixa=pressao_baixa,
            observacao=observacao
        )
        criados += 1
    except Exception as e:
        continue

print(f"Sucesso! {criados} participantes de teste foram adicionados ao banco de dados.")