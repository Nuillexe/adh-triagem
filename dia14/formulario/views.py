
from django.shortcuts import render
from django.db import transaction
from django.contrib import messages

from .models import Paciente, Evento, Medical_measurement

import re


def cadastrar_participante(request):

    if request.method == 'POST':

        # Dados pessoais
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        condicao_saude = request.POST.get('condicao_saude')
        telefone = request.POST.get('telefone')
        sexo = request.POST.get('sexo')

        # Endereço
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('rua')
        numero_da_residencia = request.POST.get('numero_da_residencia')

        # Dados da medição
        glicemia = request.POST.get('glicemia')
        pressao_arterial = request.POST.get('pressao_arterial')
        observacao = request.POST.get('observacao')

        # Validação dos campos obrigatórios
        campos_obrigatorios = [
            nome, idade, condicao_saude,
            glicemia, pressao_arterial,
            cidade, bairro, telefone
        ]

        if not all(campos_obrigatorios):
            messages.error(request, "Há campos obrigatórios em branco.")
            return render(request, 'formulario/formulario.html')

        # Validação da pressão arterial
        if not validar_pressao(pressao_arterial):
            messages.error(request, "Pressão arterial inválida.")
            return render(request, 'formulario/formulario.html')

        # Separação da pressão arterial
        pressao_sistolica, pressao_diastolica = (
            get_pressao_arterial(pressao_arterial)
        )

        try:
            with transaction.atomic():

                # 1. Recupera ou cria o evento
                evento, criado = Evento.objects.get_or_create(
                    nome='dia14-Ação social de Educação em diabetes',
                    defaults={
                        'descricao': 'Ocorreu no Projeto Social Vila América.',
                        'data': '2026-11-14'
                    }
                )

                # 2. Recupera ou cadastra o paciente
                paciente, criado = Paciente.objects.get_or_create(
                    nome=nome,
                    defaults={
                        'idade': idade,
                        'condicao_saude': condicao_saude,
                        'telefone': telefone,
                        'sexo': sexo or None,
                        'cidade': cidade,
                        'bairro': bairro,
                        'rua': rua,
                        'numero_da_residencia': numero_da_residencia
                    }
                )

                # 3. Verifica se já existe medição desse paciente
                # neste evento
                if Medical_measurement.objects.filter(
                    paciente=paciente,
                    evento=evento
                ).exists():

                    messages.warning(
                        request,
                        "Este paciente já possui uma medição cadastrada neste evento."
                    )

                    return render(
                        request,
                        'formulario/formulario.html'
                    )

                # 4. Registra a medição
                Medical_measurement.objects.create(
                    paciente=paciente,
                    evento=evento,
                    glicemia=glicemia,
                    pressaoAlta=pressao_sistolica,
                    pressaoBaixa=pressao_diastolica,
                    observacao=observacao
                )

            messages.success(
                request,
                f"Cadastro realizado com sucesso! Paciente: {paciente.nome}"
            )

        except Exception as erro:
            messages.error(
                request,
                f"Não foi possível realizar o cadastro: {erro}"
            )

    return render(request, 'formulario/formulario.html')


def validar_pressao(pressao):

    padrao = r"^(\d{2,3})/(\d{2,3})$"

    return re.match(padrao, pressao) is not None


def get_pressao_arterial(pressao):

    match = re.match(r"^(\d{2,3})/(\d{2,3})$", pressao)

    sistolica = int(match.group(1))
    diastolica = int(match.group(2))

    return sistolica, diastolica
