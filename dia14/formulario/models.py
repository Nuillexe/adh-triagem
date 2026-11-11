from django.db import models

# Create your models here.


class Participate(models.Model):
    CONDICAO_CHOICES=[
        ('DM1', 'Diabetes Tipo 1'),
        ('DM2', 'Diabetes Tipo 2'),
        ('DM1&HT','Diabetes Tipo 1 e Hipertenso'),
        ('DM2&HT','Diabetes Tipo 2 e Hipertenso'),
        ('HT', 'Hipertenesao'),
        ('Nenhum','Nenhum'),
    ]


    nome=models.CharField(max_length=150,unique=True)
    #cpf=models.CharField(max_length=11, unique=True)
    idade=models.IntegerField();
    condicao_saude= models.CharField(max_length=10, choices=CONDICAO_CHOICES)
    
    #Dados de mediçoes
    glicemia=models.IntegerField();
    pressaoAlta=models.IntegerField()
    pressaoBaixa=models.IntegerField()
    observacao=models.CharField(max_length=200);
    

    #Endereço
    #bairro=models.CharField(max_length=150)
    #rua=models.CharField(max_length=150)
    #numero=models.CharField(max_length=10)
    
    criado_em=models.DateTimeField(auto_now_add=True);

    def pressao_arterial_str(self):
        return f"{self.pressaoAlta}/{self.pressaoBaixa}"
    
    def __str__(self):
        return f"Nome: {self.nome}, Idade: {self.idade}, Condição de saude: {self.condicao_saude}, glicemia: {self.glicemia}, pressao arterial: {self.pressaoAlta}/{self.pressaoBaixa}"


