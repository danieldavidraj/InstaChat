from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_cryptography.fields import encrypt

class userManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("User must have first name!")

        if not email:
            raise ValueError("User must have an email address!")

        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user=self.create_user(
            username = username,
            email = self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True,max_length=250)
    email = models.EmailField(unique=True)
    Messages=encrypt(models.TextField(max_length=1000,default={}))
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = userManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class AllLogin(models.Model):
    id = models.AutoField(primary_key=True)
    user= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.user)

