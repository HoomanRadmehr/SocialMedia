from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class LikePost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name= 'ulike')
    post = models.ForeignKey(Post,on_delete=models.CASCADE , related_name='plike')

    def __str__(self):
        return f'{self.user} liked {self.post.body}'
