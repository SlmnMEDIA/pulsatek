from django.db import models
from django.conf import settings

from .managers import OutcomeManager

# Create your models here.

class Sale(models.Model):
    INCOME = 'IN'
    OUTCOME = 'OUT'
    TYPEIN = (
        (INCOME, 'Income'),
        (OUTCOME, 'Outcome')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type_income = models.CharField(max_length=3)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ref = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    outcome = OutcomeManager()

    class Meta:
        ordering = ['-timestamp']

    def trx_obj(self):
        try :
            if hasattr(self, 'salepulsa') :
                return self.salepulsa
            if hasattr(self, 'salegame') :
                return self.salegame
            if hasattr(self, 'saletransport'):
                return self.saletransport
            if hasattr(self, 'salelistrik'):
                return self.salelistrik
        except Exception as e :
            return None


    def profit(self):
        try :
            if hasattr(self, 'salepulsa') :
                return (self.credit - self.salepulsa.responsetrx.saldo_terpotong)
            if hasattr(self, 'salegame') :
                return  (self.credit - self.salegame.responsetrx.saldo_terpotong)
            if hasattr(self, 'saletransport'):
                return  (self.credit - self.saletransport.responsetrx.saldo_terpotong)
            if hasattr(self, 'salelistrik'):
                return  (self.credit - self.salelistrik.responsetrx.saldo_terpotong)
        except:
            return 0

    def user_balance(self):
        return self.user.saldo

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nominal = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Cash(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cashuser')
    agen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cashagen')
    nominal = models.PositiveIntegerField()
    validated = models.BooleanField(default=False)
    validateby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='cashvalid')
    delivered = models.BooleanField(default=False)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
