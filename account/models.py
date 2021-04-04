from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = RichTextField(null=True ,blank=True)
    age = models.PositiveIntegerField(null=True , blank=True)
    phone = models.PositiveIntegerField(null = True , blank = True)
    image = models.ImageField(null=True , blank=True , upload_to='media/')
    
    def __str__(self):
        return self.user.username


def save_profile(sender , **kwargs):
    if kwargs['created']==True:
        p=Profile(user=kwargs['instance'])
        p.save()

post_save.connect(save_profile,sender=User)


class Follow(models.Model):
    from_user = models.ForeignKey(User , on_delete = models.CASCADE , related_name='ffollow')
    to_user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='tfollow')

    def __str__(self):
        return f'{self.from_user} follows {self.to_user}'

class PhoneLogin(models.Model):
    phone = models.PositiveIntegerField()
        
