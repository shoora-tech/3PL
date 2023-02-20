from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission
from TPL.models import UUIDModel
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# Organization, User, User Type

class Organization(UUIDModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is requirede")
        
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, UUIDModel):
    OPERATOR = "operator"
    VALIDATOR = "validator"
    ADMIN = "admin"

    USER_TYPE_CHOICES = (
        (VALIDATOR, "Validator"),
        (OPERATOR, "Operator"),
        (ADMIN, "Admin"),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES,
        default=ADMIN,
        verbose_name="User Type",
        max_length=20
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, blank=True, null=True, verbose_name="Organization", on_delete=models.CASCADE)

    USERNAME_FIELD = "email"
    objects = AccountManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=Organization)
def create_user_for_organization(sender, instance=None, created=False, **kwargs):
    print("creaed ", created)
    if created:
        user = User.objects.create(
                email = instance.email,
                organization = instance
            )
        user.set_password("qwerty")
        user.save()
