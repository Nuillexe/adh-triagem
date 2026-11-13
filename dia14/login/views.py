from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

def logar_usuario(request):
    if request.method == 'POST':
        identificador = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario=None
        try:
            if '@' in identificador:
            
                user_obj=User.objects.get(email=identificador)#Buscando usuario pelo o e-mail

                usuario=authenticate(request,username=user_obj.username, password=senha)

            else:
                usuario=authenticate(request,username=identificador, password=senha)
                
        except User.DoesNotExist:
            usuario=None
            
        if usuario is not None:
            login(request, usuario)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('relatorios')  # Redireciona para o painel de relatórios
        else:
            messages.error(request, "E-mail ou senha inválidos.")
            return render(request, 'login/login.html')

    return render(request, 'login/login.html')



def deslogar_usuario(request):
    logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect('login')

# --- DICA DE PROTEÇÃO DE ROTA ---
# No seu app de relatórios, adicione o @login_required acima da view painel_relatorio:
# @login_required(login_url='login')
# def painel_relatorio(request):
#     ...
