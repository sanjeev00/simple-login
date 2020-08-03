from djongo import models
from django.core.validators import RegexValidator
from cryptography.fernet import Fernet
from django.conf import settings
# Create your models here.
phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits long")


class UserData(models.Model):
    phone = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    mailVerified = models.BooleanField(default=False)
    phoneVerified  = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,blank=True)
    #phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)

class UserEncData(models.Model):
    name= models.CharField(max_length=130)
    phone = models.CharField(max_length=130)
    email = models.CharField(max_length=130)
    userid = models.CharField(unique=True,max_length=50)

    def save(self, *args, **kwargs):

        key = settings.FIELD_ENCRYPTION_KEY
        cipher_suite = Fernet(key)
        self.name =self.name.encode()
        self.name = cipher_suite.encrypt(self.name).decode("utf-8")


        self.phone = self.phone.encode()
        self.phone = cipher_suite.encrypt(self.phone).decode("utf-8")
        self.email = self.email.encode()
        self.email = cipher_suite.encrypt(self.email).decode("utf-8")


        super().save(*args, **kwargs)  # Call the "real" save() method.



    def getname(self):
        key = settings.FIELD_ENCRYPTION_KEY
        cipher_suite = Fernet(key)
        byte = self.name.encode()
        return cipher_suite.decrypt(byte).decode('utf-8')

    def getPhone(self):
        key = settings.FIELD_ENCRYPTION_KEY
        cipher_suite = Fernet(key)
        byte = self.phone.encode()
        return cipher_suite.decrypt(byte).decode('utf-8')

    def getEmail(self):
        key = settings.FIELD_ENCRYPTION_KEY
        cipher_suite = Fernet(key)
        byte = self.email.encode()
        return cipher_suite.decrypt(byte).decode('utf-8')