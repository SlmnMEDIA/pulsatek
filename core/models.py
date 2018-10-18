from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Sum, Q, Value as V
from django.db.models.functions import Coalesce

from .managers import UserManager
from .utils import generate_pin_code, generate_invitation_code
from sale.models import Cash


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    limit = models.PositiveIntegerField(default=0)
    is_agen = models.BooleanField(default=False)
    saldo_agen = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    guarantee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leader = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    pin = models.CharField(max_length=5, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.pin is None or self.pin == '':
            self.pin = generate_pin_code(self)

        super(User, self).save(*args, **kwargs)

    def limit_max(self):
        free_deposit = self.deposit + 1000000
        c_member = User.objects.filter(leader=self).count()
        return int(free_deposit/c_member)

    def get_avatar(self):
        if self.avatar:
            return '/media/'+self.avatar
        return '/media/avatars/default.jpg'

    def undeliver_cash(self):
        try :
            cash_objs = Cash.objects.filter(
                validateby=self
            ).aggregate(
                undeliver = Coalesce(Sum('nominal', filter=Q(delivered=False)), V(0))
            )
            return cash_objs['undeliver']
        except :
            return 0

    @property
    def get_telegram(self):
        return self.telegram.telegram


class Telegram(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram = models.CharField(max_length=10, unique=True)


class StatusTransaction(models.Model):
    code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class Invitation(models.Model):
    agen = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=True)
    code = models.CharField(max_length=20, blank=True)
    closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = generate_invitation_code(self)
        
        super(Invitation, self).save(*args, **kwargs)


class SiteMaster(models.Model):
    code = models.CharField(max_length=20, unique=True)
    status = models.BooleanField(default=False)
    keterangan = models.CharField(max_length=200)


    def __str__(self):
        return self.code


class MessagePost(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    send_to = models.ManyToManyField(User, related_name='receiver')
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    schedule = models.DateTimeField()
    closed = models.BooleanField(default=False)
    sent_message_now = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
