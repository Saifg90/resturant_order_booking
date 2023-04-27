from django.db import models
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from email_service.services import send_email_and_generate_token
# Create your models here.


class UserProfile(AbstractUser):
    username = None

    regex = r"^[a-zA-Z]+$"

    first_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=regex,
                message="Firstname must contain Alphabets only.",
            )
        ]
    )

    last_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=regex,
                message="Lastname must contain Alphabets only.",
            )
        ]
    )

    email = models.EmailField(
        _("Email Address"),
        unique=True,
        db_index=True,
        error_messages={
            "unique": "User is already exist with given email address"
        }
    )

    date_of_birth = models.DateField(null=True)

    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        db_index=True,
        error_messages={
            "unique": "User is already exist with given phone number"
        }
    )
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  

    REQUIRED_FIELDS = ["date_of_birth"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, dispatch_uid="adhisAY^&*D(h", sender=UserProfile)
def send_email(sender, instance, created, **kwargs):
    user_name = instance.first_name.capitalize() + ' ' + instance.last_name.capitalize()

    if created:
        send_email_and_generate_token(instance.email, user_name=user_name,
                                      email_template='../templates/mails/registration.html',
                                      email_subject="Email Verification Link")