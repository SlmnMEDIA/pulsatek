from django.db import models
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce

class OutcomeQuerySet(models.QuerySet):
    def proListrik(self):
        obj = self.filter(salelistrik__isnull=False, success=True).aggregate(
            sell=Coalesce(Sum('credit'), V(0)),
            buy=Coalesce(Sum('salelistrik__responsetrx__saldo_terpotong'), V(0))
        )
        return obj['sell'] - obj['buy']

    def proPulsa(self):
        obj = self.filter(salepulsa__isnull=False, success=True).aggregate(
            sell=Coalesce(Sum('credit'), V(0)),
            buy=Coalesce(Sum('salepulsa__responsetrx__saldo_terpotong'), V(0))
        )
        return obj['sell'] - obj['buy'] 

    def proGame(self):
        obj = self.filter(salegame__isnull=False, success=True).aggregate(
            sell=Coalesce(Sum('credit'), V(0)),
            buy=Coalesce(Sum('salegame__responsetrx__saldo_terpotong'), V(0))
        )
        return obj['sell'] - obj['buy']

    def proTrans(self):
        obj = self.filter(saletransport__isnull=False, success=True).aggregate(
            sell=Coalesce(Sum('credit'), V(0)),
            buy=Coalesce(Sum('saletransport__responsetrx__saldo_terpotong'), V(0))
        )
        return obj['sell'] - obj['buy']


    def profit(self):
        return self.proGame() + self.proListrik() + self.proPulsa() + self.proTrans()
    
    

class OutcomeManager(models.Manager):
    def get_queryset(self):
        return OutcomeQuerySet(self.model, using=self._db).filter(type_income='OUT', success=True)

    def proListrik(self):
        return self.get_queryset().proListrik()

    def proPulsa(self):
        return self.get_queryset().proPulsa()

    def proGame(self):
        return self.get_queryset().proGame()

    def proTrans(self):
        return self.get_queryset().proTrans()

    def profit(self):
        return self.get_queryset().profit()