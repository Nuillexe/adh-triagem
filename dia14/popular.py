import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dia14.settings')
django.setup()

from formulario.models import Paciente, Evento, Medical_measurement

nomes_base = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda",
    "Gabriel", "Helena", "Igor", "Juliana", "Kleber", "Larissa",
    "Marcos", "Natália", "Otávio", "Patrícia", "Rafael", "Sabrina",
    "Thiago", "Vanessa", "Wagner", "Tatiane", "Rodrigo", "Camila",
    "Lucas", "Beatriz", "Matheus", "Mariana", "Felipe", "Amanda"
]

sobrenomes_base = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues",
    "Ferreira", "Alves", "Pereira", "Lima", "Gomes",
    "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida",
    "Lopes", "Barbosa", "Cardoso", "Rocha", "Dias"
]

condicoes = [
    'DM1',
    'DM2',
    'DM1&HT',
    'DM2&HT',
    'HT',
    'Nenhum'
]

bairros = [
    'alto_maron',
    'ayrton_senna',
    'bateias',
    'boa_vista',
    'brasil',
    'campinhos',
    'candeias',
    'centro',
    'cruzeiro',
    'felicia',
    'guarani',
    'ibirapuera',
    'jatoba',
    'jurema',
    'patagonia',
    'primavera',
    'recreio',
    'sao_pedro',
    'universidade',
    'zabele'
]

print('Obtendo evento principal...')

evento, criado = Evento.objects.get_or_create(
    nome='dia14-Ação social de Educação em diabetes',
    defaults={
        'descricao': 'Ocorreu no Projeto Social Vila América.',
        'data': '2026-11-14'
    }
)

if criado:
    print('Evento criado.')
else:
    print('Evento já existia.')

criados = 0

for i in range(35):

    nome = f"{random.choice(nomes_base)} {random.choice(sobrenomes_base)} {i+1}"

    try:

        paciente = Paciente.objects.create(
            nome=nome,
            idade=random.randint(20, 85),
            condicao_saude=random.choice(condicoes),
            telefone=f"7799{random.randint(10000000,99999999)}",
            sexo=random.choice(['M', 'F']),
            bairro=random.choice(bairros),
            rua=f"Rua {random.randint(1, 200)}",
            numero_da_residencia=str(random.randint(1, 999)),
            cidade='vitoria_da_conquista'
        )

        Medical_measurement.objects.create(
            paciente=paciente,
            evento=evento,
            glicemia=random.randint(70, 260),
            pressaoAlta=random.randint(100, 190),
            pressaoBaixa=random.randint(60, 115),
            observacao=random.choice([
                'Paciente relata uso regular de medicação.',
                'Sem queixas no momento do atendimento.',
                'Orientado sobre dieta restritiva de açúcar.',
                'Retorno agendado para acompanhamento.',
                ''
            ])
        )

        criados += 1

    except Exception as e:
        print(f'Erro ao criar {nome}: {e}')

print(f'\n{criados} pacientes criados com sucesso.')
print(f'Todas as medições vinculadas ao evento: {evento.nome}')