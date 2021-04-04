from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=RichTextUploadingField()
    slug=models.SlugField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body[:20]}'

    def get_absolute_url(self):
        return reverse('post:post_detail' , args=[self.created.year , self.created.month , self.created.day , self.slug])

    class Meta:
        ordering = ['-created']

