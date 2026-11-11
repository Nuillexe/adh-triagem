from django.shortcuts import render, redirect
from .models import Participate
import re
from django.contrib import messages

def cadastrar_participante(request):
    if request.method=='POST':
        nome=request.POST.get('nome')        
        idade=request.POST.get('idade')
        condicao_saude=request.POST.get('condicao_saude')
        glicemia=request.POST.get('glicemia')
        pressao_arterial=request.POST.get('pressao_arterial')
        observacao=request.POST.get('observacao')

        if not all([nome,idade,condicao_saude,idade,glicemia,pressao_arterial]):
            messages.error(request,"A campos em branco")
            return render(request, 'formulario/formulario.html')

        if validar_pressao(pressao_arterial)==False:
            messages.error(request,"Pressão Invalida")
            return render(request, 'formulario/formulario.html')

        if Participate.objects.filter(nome=nome).exists():
            messages.error(request,"Ja há um participante cadastrado com este nome")
            return render(request, 'formulario/formulario.html')
        
        pressao_sistolica=get_pressao_sistolica(pressao_arterial)
        pressao_diastolica=get_pressao_diastolica(pressao_arterial)

        
        p=Participate.objects.create(
            nome=nome,
            idade=idade,
            condicao_saude=condicao_saude,
            glicemia=glicemia,
            pressaoAlta=pressao_sistolica,
            pressaoBaixa=pressao_diastolica,
            observacao=observacao
        )
        messages.success(request, "O cadastro de foi um sucesso!\n"+
                         "Dados: "+ p.__str__())
        return render(request, 'formulario/formulario.html')

    return render(request, 'formulario/formulario.html')



def validar_pressao(pressao):
    padrao=r"^(\d{2,3})/(\d{2,3})$"
    
    match = re.match(padrao,pressao)
    
    if not match:
        return False
    
    return True

def get_pressao_sistolica(pressao):
    padrao=r"^(\d{2,3})/(\d{2,3})$"

    match=re.match(padrao,pressao)

    sistolica=match.group(1);
    return sistolica


def get_pressao_diastolica(pressao):
    padrao=r"^(\d{2,3})/(\d{2,3})$"

    match=re.match(padrao,pressao)

    diastolica=match.group(2);
    return diastolica



