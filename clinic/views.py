import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import (
    ConsultaForm,
    EstoqueItemForm,
    PacienteForm,
    PermissaoForm,
    ProntuarioForm,
    RelatorioForm,
    TransacaoFinanceiraForm,
    UsuarioForm,
)
from .models import (
    Consulta,
    EstoqueItem,
    Paciente,
    Prontuario,
    Relatorio,
    TransacaoFinanceira,
    Usuario,
)
from django.test import Client


def dashboard(request):
    try:
        pacientes_count = Paciente.objects.count()
    except Exception:
        pacientes_count = 0
    return render(request, 'dashboard/dashboard.html', {'pacientes_count': pacientes_count})


def pacientes(request):
    pacientes = Paciente.objects.all().order_by('-data_cadastro')
    return render(request, 'pacientes/list.html', {'pacientes': pacientes})


def paciente_add(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm()

    return render(request, 'pacientes/form.html', {'form': form, 'cancel_url': reverse('pacientes')})


def pacientes_export(request):
    pacientes = Paciente.objects.all().order_by('nome')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pacientes.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Nome',
        'Data Nascimento',
        'Telefone',
        'Email',
        'Especialidade',
        'Status',
        'Data Cadastro',
    ])
    for paciente in pacientes:
        writer.writerow([
            paciente.nome,
            paciente.data_nascimento.strftime('%Y-%m-%d') if paciente.data_nascimento else '',
            paciente.telefone,
            paciente.email,
            paciente.especialidade,
            paciente.status,
            paciente.data_cadastro.strftime('%Y-%m-%d %H:%M'),
        ])
    return response


def agenda(request):
    consultas = Consulta.objects.select_related('paciente').order_by('data_consulta')
    return render(request, 'agenda/list.html', {'consultas': consultas})


def agenda_add(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agenda')
    else:
        form = ConsultaForm()
    return render(request, 'agenda/form.html', {'form': form, 'cancel_url': reverse('agenda')})


def prontuarios(request):
    prontuarios = Prontuario.objects.select_related('paciente').order_by('-data_registro')
    return render(request, 'prontuarios/list.html', {'prontuarios': prontuarios})


def prontuario_add(request):
    if request.method == 'POST':
        form = ProntuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prontuarios')
    else:
        form = ProntuarioForm()
    return render(request, 'prontuarios/form.html', {'form': form, 'cancel_url': reverse('prontuarios')})


def estoque(request):
    itens = EstoqueItem.objects.all().order_by('nome')
    return render(request, 'estoque/list.html', {'itens': itens})


def estoque_add(request):
    if request.method == 'POST':
        form = EstoqueItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estoque')
    else:
        form = EstoqueItemForm()
    return render(request, 'estoque/form.html', {'form': form, 'cancel_url': reverse('estoque')})


def estoque_relatorio(request):
    itens = EstoqueItem.objects.filter(nivel_alerta__in=['Baixo', 'Crítico']).order_by('nivel_alerta', 'nome')
    return render(request, 'estoque/report.html', {'itens': itens})


def financeiro(request):
    transacoes = TransacaoFinanceira.objects.all().order_by('-data_operacao')
    now = timezone.localtime(timezone.now())
    mensal = TransacaoFinanceira.objects.filter(
        data_operacao__year=now.year,
        data_operacao__month=now.month,
    )
    receitas = sum(t.valor for t in mensal if t.tipo == 'Receita')
    despesas = sum(t.valor for t in mensal if t.tipo == 'Despesa')
    saldo = receitas - despesas
    return render(request, 'financeiro/list.html', {
        'transacoes': transacoes,
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo,
    })


def financeiro_add(request):
    if request.method == 'POST':
        form = TransacaoFinanceiraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financeiro')
    else:
        form = TransacaoFinanceiraForm()
    return render(request, 'financeiro/form.html', {'form': form, 'cancel_url': reverse('financeiro')})


def financeiro_relatorio(request):
    now = timezone.localtime(timezone.now())
    mensal = TransacaoFinanceira.objects.filter(
        data_operacao__year=now.year,
        data_operacao__month=now.month,
    )
    receitas = sum(t.valor for t in mensal if t.tipo == 'Receita')
    despesas = sum(t.valor for t in mensal if t.tipo == 'Despesa')
    return render(request, 'financeiro/report.html', {
        'mensal': mensal,
        'receitas': receitas,
        'despesas': despesas,
        'saldo': receitas - despesas,
        'periodo': now.strftime('%B/%Y'),
    })


def relatorios(request):
    relatorios = Relatorio.objects.all().order_by('-data_geracao')
    return render(request, 'relatorios/list.html', {'relatorios': relatorios})


def relatorio_add(request):
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relatorios')
    else:
        form = RelatorioForm()
    return render(request, 'relatorios/form.html', {'form': form, 'cancel_url': reverse('relatorios')})


def administracao(request):
    usuarios = Usuario.objects.all().order_by('nome')
    return render(request, 'administracao/list.html', {'usuarios': usuarios})


def administracao_add(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administracao')
    else:
        form = UsuarioForm()
    return render(request, 'administracao/form.html', {'form': form, 'cancel_url': reverse('administracao')})


def administracao_permissoes(request):
    if request.method == 'POST':
        form = PermissaoForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            usuario.permissoes = form.cleaned_data['permissoes']
            usuario.save()
            return redirect('administracao')
    else:
        form = PermissaoForm()
    return render(request, 'administracao/permissions.html', {'form': form, 'cancel_url': reverse('administracao')})


def check_pages(request):
    client = Client()
    paths = [
        '/',
        '/pacientes/',
        '/agenda/',
        '/prontuarios/',
        '/estoque/',
        '/financeiro/',
        '/relatorios/',
        '/administracao/',
    ]
    results = []
    for p in paths:
        try:
            resp = client.get(p)
            content = resp.content.decode('utf-8', errors='ignore')[:1000]
            # try to extract <title>
            import re
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE|re.DOTALL)
            title = m.group(1).strip() if m else ''
            results.append({'path': p, 'status': resp.status_code, 'title': title})
        except Exception as e:
            results.append({'path': p, 'status': 'ERROR', 'title': str(e)})
    return render(request, 'dashboard/check_pages.html', {'results': results})
