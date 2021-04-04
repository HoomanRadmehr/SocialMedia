from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from ckeditor.fields import RichTextField

class Comment(models.Model):
    user= models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomment')
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self' , on_delete=models.CASCADE , null=True , blank=True , related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:10]}'

    class Meta:
        ordering = ['-created']
