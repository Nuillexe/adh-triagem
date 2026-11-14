
from django.db.models import Q

from formulario.models import Paciente, Medical_measurement


def percentual(valor, total):
    if total == 0:
        return 0

    return round(valor / total * 100, 1)


def gerar_estatisticas(evento):

    # Todas as medições do evento selecionado
    medicoes = Medical_measurement.objects.filter(
        evento=evento
    ).select_related('paciente', 'evento')

    # Pacientes que participaram desse evento
    participantes = Paciente.objects.filter(
        medicoes__evento=evento
    ).distinct()

    total_participantes = participantes.count()

    # Função auxiliar para contar pacientes sem duplicidade
    def contar_pacientes(queryset):
        return queryset.values('paciente_id').distinct().count()

    # Quantidade por condição de saúde
    qtd_dm1_puro = contar_pacientes(
        medicoes.filter(paciente__condicao_saude='DM1')
    )

    qtd_dm1_ht = contar_pacientes(
        medicoes.filter(paciente__condicao_saude='DM1&HT')
    )

    qtd_dm2_puro = contar_pacientes(
        medicoes.filter(paciente__condicao_saude='DM2')
    )

    qtd_dm2_ht = contar_pacientes(
        medicoes.filter(paciente__condicao_saude='DM2&HT')
    )

    qtd_ht = contar_pacientes(
        medicoes.filter(
            paciente__condicao_saude__in=['HT', 'DM1&HT', 'DM2&HT']
        )
    )

    qtd_nenhum = contar_pacientes(
        medicoes.filter(paciente__condicao_saude='Nenhum')
    )

    # Glicemia elevada
    glicemia_alta = medicoes.filter(glicemia__gte=180)

    qtd_glicemia_alta = contar_pacientes(glicemia_alta)

    qtd_glicemia_alta_dm1 = contar_pacientes(
        glicemia_alta.filter(
            paciente__condicao_saude__in=['DM1', 'DM1&HT']
        )
    )

    qtd_glicemia_alta_dm2 = contar_pacientes(
        glicemia_alta.filter(
            paciente__condicao_saude__in=['DM2', 'DM2&HT']
        )
    )

    qtd_glicemia_alta_nao_dm = contar_pacientes(
        glicemia_alta.filter(
            paciente__condicao_saude__in=['Nenhum', 'HT']
        )
    )

    # Pressão arterial elevada
    pressao_alta = medicoes.filter(
        Q(pressaoAlta__gte=140) |
        Q(pressaoBaixa__gte=90)
    )

    qtd_pressao_alta = contar_pacientes(pressao_alta)

    qtd_pressao_alta_ht = contar_pacientes(
        pressao_alta.filter(
            paciente__condicao_saude__in=['HT', 'DM1&HT', 'DM2&HT']
        )
    )

    qtd_pressao_alta_nao_ht = contar_pacientes(
        pressao_alta.exclude(
            paciente__condicao_saude__in=['HT', 'DM1&HT', 'DM2&HT']
        )
    )

    # Retorno dos dados
    return {
        'evento': evento,

        'participantes': participantes,
        'medicoes': medicoes,
        'total_participantes': total_participantes,

        'porc_dm1': percentual(
            qtd_dm1_puro + qtd_dm1_ht,
            total_participantes
        ),

        'porc_dm2': percentual(
            qtd_dm2_puro + qtd_dm2_ht,
            total_participantes
        ),

        'porc_ht': percentual(qtd_ht, total_participantes),

        'porc_nenhum': percentual(qtd_nenhum, total_participantes),

        'porc_ht_dm1': percentual(
            qtd_dm1_ht,
            qtd_dm1_puro + qtd_dm1_ht
        ),

        'porc_ht_dm2': percentual(
            qtd_dm2_ht,
            qtd_dm2_puro + qtd_dm2_ht
        ),

        'porc_glicemia_alta': percentual(
            qtd_glicemia_alta,
            total_participantes
        ),

        'porc_glicemia_alta_dm1': percentual(
            qtd_glicemia_alta_dm1,
            qtd_glicemia_alta
        ),

        'porc_glicemia_alta_dm2': percentual(
            qtd_glicemia_alta_dm2,
            qtd_glicemia_alta
        ),

        'porc_glicemia_alta_nao_dm': percentual(
            qtd_glicemia_alta_nao_dm,
            qtd_glicemia_alta
        ),

        'porc_pressao_alta': percentual(
            qtd_pressao_alta,
            total_participantes
        ),

        'porc_pressao_alta_ht': percentual(
            qtd_pressao_alta_ht,
            qtd_pressao_alta
        ),

        'porc_pressao_alta_nao_ht': percentual(
            qtd_pressao_alta_nao_ht,
            qtd_pressao_alta
        ),
    }
