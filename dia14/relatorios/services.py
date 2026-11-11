
from django.db.models import Q
from formulario.models import Participate


def percentual(valor, total):
    if total == 0:
        return 0

    return round(valor / total * 100, 1)


def gerar_estatisticas():
    participantes = Participate.objects.all()
    total_participantes = participantes.count()

    # Quantidade por condição de saúde
    qtd_dm1_puro = participantes.filter(condicao_saude='DM1').count()
    qtd_dm1_ht = participantes.filter(condicao_saude='DM1&HT').count()

    qtd_dm2_puro = participantes.filter(condicao_saude='DM2').count()
    qtd_dm2_ht = participantes.filter(condicao_saude='DM2&HT').count()

    qtd_ht = participantes.filter(
        condicao_saude__in=['HT', 'DM1&HT', 'DM2&HT']
    ).count()

    qtd_nenhum = participantes.filter(condicao_saude='Nenhum').count()

    # Glicemia elevada
    glicemia_alta = participantes.filter(glicemia__gte=180)

    qtd_glicemia_alta = glicemia_alta.count()

    qtd_glicemia_alta_dm1 = glicemia_alta.filter(
        condicao_saude__in=['DM1', 'DM1&HT']
    ).count()

    qtd_glicemia_alta_dm2 = glicemia_alta.filter(
        condicao_saude__in=['DM2', 'DM2&HT']
    ).count()

    qtd_glicemia_alta_nao_dm = glicemia_alta.filter(
        condicao_saude__in=['Nenhum', 'HT']
    ).count()

    # Pressão elevada
    pressao_alta = participantes.filter(
        Q(pressaoAlta__gte=140) | Q(pressaoBaixa__gte=90)
    )

    qtd_pressao_alta = pressao_alta.count()

    qtd_pressao_alta_ht = pressao_alta.filter(
        condicao_saude__in=['HT', 'DM1&HT', 'DM2&HT']
    ).count()

    qtd_pressao_alta_nao_ht = pressao_alta.exclude(
        condicao_saude__in=['HT', 'DM1&HT', 'DM2&HT']
    ).count()

    # Retorno dos dados
    return {
        'participantes': participantes,
        'total_participantes': total_participantes,

        'porc_dm1': percentual(qtd_dm1_puro + qtd_dm1_ht, total_participantes),
        'porc_dm2': percentual(qtd_dm2_puro + qtd_dm2_ht, total_participantes),
        'porc_ht': percentual(qtd_ht, total_participantes),
        'porc_nenhum': percentual(qtd_nenhum, total_participantes),

        'porc_ht_dm1': percentual(
            qtd_dm1_ht, qtd_dm1_puro + qtd_dm1_ht
        ),
        'porc_ht_dm2': percentual(
            qtd_dm2_ht, qtd_dm2_puro + qtd_dm2_ht
        ),

        'porc_glicemia_alta': percentual(
            qtd_glicemia_alta, total_participantes
        ),
        'porc_glicemia_alta_dm1': percentual(
            qtd_glicemia_alta_dm1, qtd_glicemia_alta
        ),
        'porc_glicemia_alta_dm2': percentual(
            qtd_glicemia_alta_dm2, qtd_glicemia_alta
        ),
        'porc_glicemia_alta_nao_dm': percentual(
            qtd_glicemia_alta_nao_dm, qtd_glicemia_alta
        ),

        'porc_pressao_alta': percentual(
            qtd_pressao_alta, total_participantes
        ),
        'porc_pressao_alta_ht': percentual(
            qtd_pressao_alta_ht, qtd_pressao_alta
        ),
        'porc_pressao_alta_nao_ht': percentual(
            qtd_pressao_alta_nao_ht, qtd_pressao_alta
        ),
    }
