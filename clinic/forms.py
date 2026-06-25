from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from .models import (
    Paciente,
    Consulta,
    Prontuario,
    EstoqueItem,
    TransacaoFinanceira,
    Relatorio,
    Usuario,
)


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


only_letters = RegexValidator(
    regex=r'^[A-Za-zÀ-ÿ ]+$',
    message='Use apenas letras e espaços.',
)

only_digits = RegexValidator(
    regex=r'^[0-9]+$',
    message='Use apenas números.',
)


class PacienteForm(forms.ModelForm):
    nome = forms.CharField(
        validators=[only_letters],
        widget=forms.TextInput(
            attrs={
                'pattern': '^[A-Za-zÀ-ÿ ]+$',
                'inputmode': 'text',
                'title': 'Use apenas letras e espaços.',
            }
        ),
    )
    telefone = forms.CharField(
        validators=[only_digits],
        widget=forms.TextInput(
            attrs={
                'pattern': '^[0-9]+$',
                'inputmode': 'numeric',
                'title': 'Use apenas números.',
                'maxlength': '15',
            }
        ),
    )
    especialidade = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'pattern': '^[A-Za-zÀ-ÿ ]*$',
                'inputmode': 'text',
                'title': 'Use apenas letras e espaços.',
            }
        ),
    )

    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'telefone', 'email', 'especialidade', 'status']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }


class ConsultaForm(forms.ModelForm):
    data_consulta = forms.DateTimeField(widget=DateTimeLocalInput())
    dentista = forms.CharField(
        validators=[only_letters],
        widget=forms.TextInput(
            attrs={
                'pattern': '^[A-Za-zÀ-ÿ ]+$',
                'inputmode': 'text',
                'title': 'Use apenas letras e espaços.',
            }
        ),
    )
    procedimento = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'inputmode': 'text',
            }
        ),
    )

    class Meta:
        model = Consulta
        fields = ['paciente', 'data_consulta', 'procedimento', 'dentista', 'status', 'observacoes']


class ProntuarioForm(forms.ModelForm):
    procedimento = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'inputmode': 'text',
            }
        ),
    )

    class Meta:
        model = Prontuario
        fields = ['paciente', 'procedimento', 'observacoes']


class EstoqueItemForm(forms.ModelForm):
    quantidade = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'inputmode': 'numeric',
                'min': '0',
            }
        )
    )

    class Meta:
        model = EstoqueItem
        fields = ['nome', 'quantidade', 'unidade', 'nivel_alerta']


class TransacaoFinanceiraForm(forms.ModelForm):
    data_operacao = forms.DateTimeField(widget=DateTimeLocalInput())
    valor = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'inputmode': 'decimal',
                'step': '0.01',
                'min': '0',
            }
        ),
    )

    class Meta:
        model = TransacaoFinanceira
        fields = ['data_operacao', 'descricao', 'tipo', 'valor', 'categoria', 'observacoes']


class UsuarioForm(forms.ModelForm):
    nome = forms.CharField(
        validators=[only_letters],
        widget=forms.TextInput(
            attrs={
                'pattern': '^[A-Za-zÀ-ÿ ]+$',
                'inputmode': 'text',
                'title': 'Use apenas letras e espaços.',
            }
        ),
    )
    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha')

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'funcao', 'status', 'permissoes']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('senha')
        if password:
            user.senha_hash = make_password(password)
        if commit:
            user.save()
        return user


class PermissaoForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), label='Usuário')
    permissoes = forms.CharField(max_length=255, required=False, label='Permissões')


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['nome', 'periodo', 'status']
