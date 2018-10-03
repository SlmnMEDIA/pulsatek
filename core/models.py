from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from .managers import UserManager
from .utils import generate_pin_code


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

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.pin is None or self.pin == '':
            self.pin = generate_pin_code(self)

        super(User, self).save(*args, **kwargs)

    def limit_max(self):
        free_deposit = self.deposit + 1000000
        c_member = User.objects.filter(leader=self).count()
        return free_deposit/c_member

    def get_avatar(self):
        if self.avatar:
            return '/media/'+self.avatar
        return '/media/avatars/default.jpg'


class Telegram(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram = models.CharField(max_length=10, unique=True)


class StatusTransaction(models.Model):
    code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.code