from django.db import models

# Create your models here.


class Paciente(models.Model):
    CONDICAO_CHOICES=[
        ('DM1', 'Diabetes Tipo 1'),
        ('DM2', 'Diabetes Tipo 2'),
        ('DM1&HT','Diabetes Tipo 1 e Hipertenso'),
        ('DM2&HT','Diabetes Tipo 2 e Hipertenso'),
        ('HT', 'Hipertenesao'),
        ('Nenhum','Nenhum'),
    ]

    BAIRRO_CHOICES = [
        ('alto_maron', 'Alto Maron'),
        ('ayrton_senna', 'Ayrton Senna'),
        ('bateias', 'Bateias'),
        ('boa_vista', 'Boa Vista'),
        ('brasil', 'Brasil'),
        ('campinhos', 'Campinhos'),
        ('candeias', 'Candeias'),
        ('centro', 'Centro'),
        ('cruzeiro', 'Cruzeiro'),
        ('distrito_industrial', 'Distrito Industrial'),
        ('espirito_santo', 'Espírito Santo'),
        ('felicia', 'Felícia'),
        ('guarani', 'Guarani'),
        ('ibirapuera', 'Ibirapuera'),
        ('jatoba', 'Jatobá'),
        ('jurema', 'Jurema'),
        ('lagoa_das_flores', 'Lagoa das Flores'),
        ('nossa_senhora_aparecida', 'Nossa Senhora Aparecida'),
        ('patagonia', 'Patagônia'),
        ('primavera', 'Primavera'),
        ('recreio', 'Recreio'),
        ('sao_pedro', 'São Pedro'),
        ('universidade', 'Universidade'),
        ('zabele', 'Zabelê'),
        ('miro_cairo', 'Miro Cairo'),

        # Outras localidades e loteamentos
        ('bnh', 'BNH'),
        ('bruno_bacelar', 'Bruno Bacelar'),
        ('comveima', 'Comveima'),
        ('henriqueta_prates', 'Henriqueta Prates'),
        ('iracema', 'Iracema'),
        ('jardim_valeria', 'Jardim Valéria'),
        ('kadija', 'Kadija'),
        ('morada_dos_passaros', 'Morada dos Pássaros'),
        ('nova_cidade', 'Nova Cidade'),
        ('novo_horizonte', 'Novo Horizonte'),
        ('urbis_i', 'Urbis I'),
        ('urbis_ii', 'Urbis II'),
        ('urbis_iii', 'Urbis III'),
        ('urbis_iv', 'Urbis IV'),
        ('urbis_v', 'Urbis V'),
        ('urbis_vi', 'Urbis VI'),
        ('vila_serrana', 'Vila Serrana'),
        ('cidade_modelo', 'Cidade Modelo'),
        ('cidade_maravilhosa', 'Cidade Maravilhosa'),

        # Outras opções
        ('zona_rural', 'Zona Rural'),
        ('outro', 'Outro'),
    ]

    CIDADE_CHOICES=[
        ('vitoria_da_conquista', 'Vitoria da Conquista'),
        ('outra', 'Outra'),
    ]

    nome=models.CharField(max_length=150,unique=True)
    idade=models.PositiveIntegerField()
    condicao_saude= models.CharField(max_length=10, choices=CONDICAO_CHOICES)
    telefone=models.CharField(max_length=20)
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    sexo=models.CharField(max_length=1,choices=SEXO_CHOICES,blank=True, null=True)

    #Endereço
    bairro=models.CharField(max_length=150, choices=CONDICAO_CHOICES)    
    rua=models.CharField(max_length=150)
    numero_da_residencia=models.CharField(max_length=10)
    cidade=models.CharField(max_length=150, choices=CIDADE_CHOICES)
    
    criado_em=models.DateTimeField(auto_now_add=True);

    def pressao_arterial_str(self):
        return f"{self.pressaoAlta}/{self.pressaoBaixa}"


    def __str__(self):
         return f"Nome: {self.nome}, Idade: {self.idade}, Condição de saude: {self.condicao_saude}, glicemia: {self.glicemia}, pressao arterial: {self.pressaoAlta}/{self.pressaoBaixa}"


class Evento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Medical_measurement(models.Model):

    glicemia = models.IntegerField()
    pressaoAlta = models.IntegerField()
    pressaoBaixa = models.IntegerField()
    observacao = models.CharField(max_length=200, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='medicoes'
    )

    evento = models.ForeignKey(
        Evento,
        on_delete=models.SET_NULL,
        related_name='medicoes',
        blank=True,
        null=True
    )

    def pressao_arterial_str(self):
        return f"{self.pressaoAlta}/{self.pressaoBaixa}"

    def __str__(self):
        return f"Medição de {self.paciente.nome} - {self.criado_em}"