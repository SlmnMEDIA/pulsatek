from django.db import models
from django.conf import settings

# Create your models here.
from .managers import ActiveManager
from .utils import generate_trx
from sale.models import Sale
import re

class Operator(models.Model):
    operator = models.CharField(max_length=20, unique=True)
    parse = models.CharField(max_length=20, blank=True,)
    is_active = models.BooleanField(default=False, verbose_name='aktif?')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    onactive = ActiveManager()


    class Meta:
        verbose_name_plural = 'Provider Telekomunikasi'

    def __str__(self):
        return self.operator

    def save(self, *args, **kwargs):
        if self.parse is None or self.parse == '':
            self.parse = '-'.join(self.operator.lower().strip().split())
        super(Operator, self).save(*args, **kwargs)


    def get_pulsa(self):
        return Product.objects.filter(product_type=1, operator=self)

    def get_data(self):
        return Product.objects.filter(product_type=2, operator=self)


class PrefixNumber(models.Model):
    prefix = models.CharField(max_length=4, unique=True, help_text='Nomor prefix operator')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prefix

    class Meta:
        verbose_name_plural = 'Prefix'


class Server(models.Model):
    code = models.CharField(max_length=12, verbose_name='kode', help_text='Kode produk layanan H2H')
    product_name = models.CharField(max_length=200, blank=True, verbose_name='nama produk')
    price = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} / {}'.format(self.code, self.product_name)

    class Meta:
        verbose_name_plural = 'Rajabiller Pulsa'



class Product(models.Model):
    PULSA_ = 1
    DATA_ = 2
    TYPE_PROD = (
        (PULSA_, 'PULSA'),
        (DATA_, 'DATA')
    )
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, verbose_name='Pilih operator')
    product_type = models.PositiveSmallIntegerField(choices=TYPE_PROD, default=1, verbose_name='tipe')
    product_code = models.CharField(max_length=12, unique=True, verbose_name='kode')
    product_name = models.CharField(max_length=200, blank=True, verbose_name='Produk', help_text='Nama produk website')
    nominal = models.PositiveIntegerField(verbose_name='nilai nominal')
    price = models.PositiveIntegerField(verbose_name='harga')
    server = models.OneToOneField(Server, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='title app', help_text='Nama produk pada aplikasi / telegram')
    description = models.TextField(max_length=500, blank=True, verbose_name='deskripsi app', help_text='Deskripsi produk')
    additional_info = models.TextField(max_length=500, blank=True, verbose_name='info pemesanan', help_text='* Opsional')
    is_active = models.BooleanField(default=False, verbose_name='aktif?')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    onactive = ActiveManager()

    class Meta:
        ordering = ['operator', 'product_type', 'nominal']
        verbose_name_plural = 'Produk Data Pulsa'

    def __str__(self):
        return self.product_title()

    def product_desc(self):
        if self.description: 
            return self.description
        return "{} harga Rp. {:0,.2f}".format(self.product_title().title(), self.price)

    def add_info(self):
        if self.additional_info:
            return self.additional_info
        return 'Ketikkan No.Handphone tujuan! (diawali angka 0).\nContoh : 081234567890'

    def product_title(self):
        if self.product_name:
            return self.product_name
        return "PULSA {} {:0,.0f}".format(self.operator.operator.title(), self.nominal)

    # def get_server(self):
    #     return ''.format(self.server.code, 

class Transaction(models.Model):
    trx_code = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=18)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=1, related_name='buyerpulsa')
    record = models.OneToOneField(Sale, on_delete=models.SET_NULL, null=True, blank=True, related_name='salepulsa')
    closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trx_code

    def save(self, *args, **kwargs):
        if self.trx_code is None or self.trx_code == '':
            self.trx_code = generate_trx(self)
        super(Transaction, self).save(*args, **kwargs)

    def get_responsetrx(self):
        return self.responsetrx.trx

    def get_trx_status(self):
        try :
            return self.statustransaction_set.latest()
        except:
            return None

    def product_name(self):
        return self.product.product_title()

    def price_out(self):
        return self.product.price

    def customer(self):
        return re.sub(r'\d{3}$','xxx', self.phone)   



class StatusTransaction(models.Model):
    INPROCESS = 'IN'
    PENDING = 'PE'
    SUCCESS = 'SS'
    FAILED = 'FA'
    CANCEL = 'CA'
    STATUS_TYPE = (
        (INPROCESS, 'IN PROCESS'),
        (PENDING, 'PENDING'),
        (SUCCESS, 'SUCCESS'),
        (FAILED, 'FAILED'),
        (CANCEL, 'CANCELED')
    )
    trx = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_TYPE, default='IN')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        get_latest_by = ['timestamp']

    def __str__(self):
        return str(self.status)


class ResponseTrx(models.Model):
    trx = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    kode_produk = models.CharField(max_length=200)
    waktu = models.CharField(max_length=200)
    no_hp = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    ref1 = models.CharField(max_length=200)
    ref2 = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    ket = models.CharField(max_length=200)
    saldo_terpotong = models.PositiveIntegerField(default=0)
    sisa_saldo = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)