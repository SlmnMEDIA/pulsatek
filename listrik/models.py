from django.db import models
from django.conf import settings


from sale.models import Sale
from .utils import generate_trx
import re



class Operator(models.Model):
    operator = models.CharField(max_length=20, unique=True, verbose_name='Provider')
    parse = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='aktif?')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Provider Listrik'

    def __str__(self):
        return self.operator

    def save(self, *args, **kwargs):
        if self.parse is None or self.parse == '':
            self.parse = '-'.join(self.operator.lower().strip().split())
        super(Operator, self).save(*args, **kwargs)


class Product(models.Model):
    product_code = models.CharField(max_length=10, unique=True, verbose_name='kode')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, verbose_name='provider')
    product_name = models.CharField(max_length=100, verbose_name='produk', help_text='Nama produk on website')
    nominal = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(verbose_name='harga')
    title = models.CharField(max_length=200, verbose_name='title app', help_text='Nama produk on telegram / apps')
    description = models.TextField(max_length=500, blank=True, verbose_name='Deskripsi', help_text='Deskripsi penjelasan produk')
    additional_info = models.TextField(max_length=500, blank=True, verbose_name='Optional', help_text='Deskripsi tambahan produk')
    is_active = models.BooleanField(default=False, verbose_name='aktif?')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['nominal']
        verbose_name_plural = 'Produk Token Listrik'
    
    def __str__(self):
        return self.product_code

    def product_desc(self):
        if self.description: 
            return self.description
        return "{} harga Rp. {:0,.2f}".format(self.product_title().title(), self.price)

    def add_info(self):
        if self.additional_info:
            return self.additional_info
        return 'Masukan No. ID Pelanggan / No. Meter listrik Anda.\nContoh : 11991888111'

    def product_title(self):
        if self.product_name:
            return self.product_name
        return 'PRODUK LISTRIK'


class Transaction(models.Model):
    trx_code = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=18)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=1, related_name='buyerlistrik')
    record = models.OneToOneField(Sale, on_delete=models.SET_NULL, null=True, blank=True, related_name='salelistrik')
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

    def customer(self):
        return re.sub(r'\d{3}$','xxx', self.phone)

    def get_detail_response(self):
        return self.responsetrx.datail

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
    kode_produk = models.CharField(max_length=50, blank=True)
    waktu = models.CharField(max_length=50, blank=True)
    idpel1 = models.CharField(max_length=50, blank=True)
    idpel2 = models.CharField(max_length=50, blank=True)
    idpel3 = models.CharField(max_length=50, blank=True)
    nama_pelanggan = models.CharField(max_length=50, blank=True)
    periode = models.CharField(max_length=50, blank=True)
    nominal = models.PositiveIntegerField(default=0)
    admin = models.PositiveIntegerField(default=0)
    ref1 = models.CharField(max_length=50, blank=True)
    ref2 = models.CharField(max_length=50, blank=True)
    ref3 = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)
    ket = models.CharField(max_length=200, blank=True)
    saldo_terpotong = models.PositiveIntegerField(default=0)
    sisa_saldo = models.PositiveIntegerField(default=0)
    url_struk = models.CharField(max_length=200, blank=True)
    datail = models.TextField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


