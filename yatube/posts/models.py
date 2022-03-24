from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             help_text='задайте заголовок')
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Текст поста', help_text='Текст нового поста')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group,
                              blank=True,
                              null=True,
                              related_name='group',
                              on_delete=models.SET_NULL,
                              verbose_name='Группа',
                              help_text=('Группа, к которой '
                                         'будет относиться пост'))

    def __str__(self):
        return self.text