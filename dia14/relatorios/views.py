from django.shortcuts import render, redirect
from formulario.models import Participate
from django.db.models import Q
from django.contrib import messages

def painel_relatorio(request):
    participantes=Participate.objects.all()
    total_participantes=participantes.count()

    porc_dm1 = 0
    porc_dm2 = 0
    porc_ht = 0
    porc_nenhum = 0

    porc_ht_dm1=0
    porc_ht_dm2= 0
            
    porc_glicemia_alta = 0
    porc_glicemia_alta_dm1 = 0
    porc_glicemia_alta_dm2 = 0
    porc_glicemia_alta_nao_dm = 0

    porc_pressao_alta = 0
    porc_pressao_alta_ht = 0
    porc_pressao_alta_nao_ht = 0
    
    if(total_participantes>0):
    
        qtd_dm1_puro=participantes.filter(condicao_saude='DM1').count()
        qtd_dm1_ht=participantes.filter(condicao_saude='DM1&HT').count()
        qtd_dm2_puro=participantes.filter(condicao_saude='DM2').count()
        qtd_dm2_ht=participantes.filter(condicao_saude='DM2&HT').count()
        qtd_ht=participantes.filter(condicao_saude__in=['HT','DM2&HT','DM1&HT']).count()
        qtd_nenhum=participantes.filter(condicao_saude='Nenhum').count()
        
        qtd_glicemia_alta=participantes.filter(glicemia__gte=180).count()
        qtd_glicemia_alta_dm1=participantes.filter(glicemia__gte=180, condicao_saude__in=['DM1','DM1&HT'] ).count()
        qtd_glicemia_alta_dm2=participantes.filter(glicemia__gte=180, condicao_saude__in=['DM2','DM2&HT'] ).count()
        qtd_glicemia_alta_nao_dm=participantes.filter(glicemia__gte=180, condicao_saude__in=['Nenhum','HT'] ).count()

        qtd_pressao_alta=participantes.filter( Q(pressaoAlta__gte=140) | Q(pressaoBaixa__gte=90)).count()
        qtd_pressao_alta_ht=participantes.filter(Q(pressaoAlta__gte=140) | Q(pressaoBaixa__gte=90), condicao_saude__in=['HT','DM1&HT','DM2&HT']).count()
        qtd_pressao_alta_nao_ht=participantes.filter(Q(pressaoAlta__gte=140) | Q(pressaoBaixa__gte=90), ~Q(condicao_saude__in=['HT','DM1&HT','DM2&HT'])).count()

        porc_dm1 = round((qtd_dm1_ht + qtd_dm1_puro)/total_participantes *100 ,1)
        porc_dm2 = round((qtd_dm2_ht + qtd_dm2_puro)/total_participantes *100 ,1)
        porc_ht = round((qtd_dm2_ht + qtd_dm1_ht + qtd_ht)/total_participantes *100 ,1)
        porc_nenhum = round(qtd_nenhum / total_participantes*100,1)

        if qtd_dm1_ht>0 and qtd_dm1_puro>0:
            porc_ht_dm1= round(qtd_dm1_ht/total_participantes *100,1)
            porc_ht_dm2= round(qtd_dm2_ht/total_participantes * 100,1)

        if qtd_glicemia_alta>0:
            porc_glicemia_alta = round(qtd_glicemia_alta / total_participantes*100,1)
            porc_glicemia_alta_dm1 = round(qtd_glicemia_alta_dm1 / qtd_glicemia_alta*100,1)
            porc_glicemia_alta_dm2 = round(qtd_glicemia_alta_dm2 / qtd_glicemia_alta *100,1)
            porc_glicemia_alta_nao_dm = round(qtd_glicemia_alta_nao_dm / qtd_glicemia_alta*100,1)

        if qtd_pressao_alta>0:
            porc_pressao_alta = round(qtd_pressao_alta/total_participantes*100,1)
            porc_pressao_alta_ht = round(qtd_pressao_alta_ht/qtd_pressao_alta *100,1)
            porc_pressao_alta_nao_ht= round(qtd_pressao_alta_nao_ht/qtd_pressao_alta*100,1)
        
   
        
    context={

        'participantes' : participantes,
        'total_participantes' : total_participantes,
        'porc_dm1': porc_dm1,
        'porc_dm2':porc_dm2,
        'porc_ht':porc_ht,
        'porc_nenhum':porc_nenhum,
        'porc_ht_dm1': porc_ht_dm1,
        'porc_ht_dm2': porc_ht_dm2,
        'porc_glicemia_alta':porc_glicemia_alta,
        'porc_glicemia_alta_dm1':porc_glicemia_alta_dm1,
        'porc_glicemia_alta_dm2':porc_glicemia_alta_dm2,
        'porc_glicemia_alta_nao_dm':porc_glicemia_alta_nao_dm,
        'porc_pressao_alta':porc_pressao_alta,
        'porc_pressao_alta_ht':porc_pressao_alta_ht,
        'porc_pressao_alta_nao_ht':porc_pressao_alta_nao_ht
    }

    return render(request, "relatorios/relatorios.html", context)

def deletar_participante(request, participante_id):

    p=Participate.objects.get(id=participante_id)
    p.delete()
    messages.success(request, "Participante deletado com sucesso!")
    return redirect('relatorios') 

   
