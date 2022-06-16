from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import datetime

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    
class User(AbstractUser):
    gender= (('male','Male'), ('female','Female'))
    email=models.EmailField(unique=True)
    gender=models.CharField(max_length=10,choices=gender,null=True,blank=True)
    mobile=models.CharField(max_length=15,null=True,blank=True)
    company_name=models.CharField(max_length=100,null=True,blank=True)
    role=models.CharField(default='hr',max_length=10)
    
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

  
    
    def __str__(self):
        return self.email
    
    
class JobPost(models.Model):
    time=(('part-time','Part-time'),('full-time','full-time'))
    cate=(
        ('marketing','Marketing'),
        ('customer service','Customer service'),
        ('human resource','Human resource'),
        ('project management','Project management'),
        ('business devlopment','Business devlopment'),
        ('sales & communication','Seles & communication'),
        ('teaching & education','Teaching & education'),
        ('information technology','Information technology'),
    )
    HR=models.ForeignKey(User,on_delete=models.CASCADE)
    position=models.CharField(max_length=100)
    salary=models.CharField(max_length=100)
    addres=models.TextField(max_length=200)
    categories=models.CharField(max_length=100,choices=cate)
    job_description=models.TextField(max_length=200)
    experience=models.CharField(max_length=50)
    slot=models.IntegerField()
    type=models.CharField(max_length=25,choices=time)
    city=models.CharField(max_length=20)
    time=models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.categories
    
    
class Application(models.Model):
    gender= (('male','Male'), ('female','Female'))
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)    
    gender=models.CharField(max_length=30,choices=gender)
    Bod=models.DateField(max_length=20)
    mobile=models.CharField(max_length=15)
    resume=models.FileField(upload_to='resume')
    company_name=models.ForeignKey(JobPost,on_delete=models.CASCADE,related_name='company')

    
    def __str__(self):
        return self.email
