from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.
def get_default_avatar_img():
    return 'defaultavatar/1024px-Circle-icons-profile.svg.png'

class amberuser(User):
    bio = models.TextField(null=True , blank=True , default='')
    avatar = models.ImageField(upload_to = 'profiles' , null = True , blank = True , default = get_default_avatar_img )

class temperoryaccount(models.Model):
    username = models.CharField(max_length=256 , null=True , blank=True)
    password = models.CharField(max_length=256 , null=True , blank=True)
    email = models.CharField(max_length=256 , null=True , blank=True)
    code = models.CharField(max_length=50 , null=True , blank=True)
    isactivenow = models.BooleanField(default=False , null= True , blank=True)


class post(models.Model):
    author = models.ForeignKey(amberuser , on_delete=models.CASCADE , null= True , blank=True )
    title = models.CharField(max_length=256 , null=True , blank=True)
    summary = models.TextField()
    content = models.TextField( null=True , blank=True)
    hascomment = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    def cdate(self):
        return '{}, {} {}'.format(self.date.year , self.date.day , self.date.strftime('%B'))


class resetpassword(models.Model):
    username = models.CharField(max_length=256 , null=True , blank=True)
    linkuseronce = models.BooleanField(default=False)
    code = models.CharField(max_length=50 , null=True , blank=True)




class comment(models.Model):
    author = models.ForeignKey(amberuser , on_delete=models.CASCADE , null= True , blank=True ) 
    content = models.TextField( null=True , blank=True)
    date = models.DateTimeField(auto_now_add=True)
    related_post = models.ForeignKey(post , related_name="related_post" , null= True , blank=True , on_delete=models.CASCADE)
    def __str__(self):
        return '{} said {}'.format(  self.author.username , self.content)
