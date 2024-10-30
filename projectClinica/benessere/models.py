from django.db import models
from django.contrib.auth.models import User


class Uf(models.Model):
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    uf = models.ForeignKey(Uf, on_delete=models.CASCADE, related_name='cidades')
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome

class UnidadeClinica(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='unidadeclinica')
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f'{self.nome} - {self.cidade.nome}, {self.cidade.uf.sigla}'

class Especialidade(models.Model):
    nome = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Agora usando User
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)
    crm = models.CharField(max_length=20)

    def __str__(self):
        return self.usuario.username

class Recepcionista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Agora usando User

    def __str__(self):
        return self.usuario.username


class Gestor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.usuario.username

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    data_hora = models.DateTimeField()
    unidade_clinica = models.ForeignKey(UnidadeClinica, on_delete=models.CASCADE)
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Consulta com {self.medico.usuario.username} em {self.data_hora}'


class Pagamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()

    def __str__(self):
        return f'Pagamento de {self.valor} para {self.paciente.nome}'

class CheckIn(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    data = models.DateField(auto_now=True)
    hora = models.TimeField(auto_now=True)
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Check-in de {self.consulta.paciente.nome} para consulta em {self.data}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)  # Campo para foto de perfil

    def __str__(self):
        return self.user.username
    
class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensagem de {self.remetente} para {self.destinatario} - {self.timestamp.strftime("%Y-%m-%d %H:%M")}'
    
class Prontuario(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name="prontuario")
    historico = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Prontuário de {self.paciente.nome}"

class Diagnostico(models.Model):
    consulta = models.OneToOneField('Consulta', on_delete=models.CASCADE, related_name='diagnostico')
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico da consulta de {self.consulta.paciente.nome} em {self.data}"

class Medicacao(models.Model):
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, related_name='medicacoes')
    nome = models.CharField(max_length=100)
    dosagem = models.CharField(max_length=50)
    instrucoes = models.TextField()

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"
