from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS = ((0, "Draft"), (1, "Publish"))


class Account(AbstractUser):
    birth_of_place = models.CharField(verbose_name=_('Место рождения'), max_length=50, blank=True, null=True)
    birth_of_date = models.DateField(verbose_name=_('Дата рождения'), blank=True, null=True)
    living_place = models.CharField(verbose_name=_('Место проживания'), max_length=80, blank=True, null=True)
    nation = models.CharField(verbose_name=_('Нация'), max_length=30, blank=True, null=True)
    occupation = models.CharField(verbose_name=_('Профессия'), max_length=50, blank=True, null=True)
    phone_number = models.IntegerField(verbose_name=_('Номер телефона'), max_length=10, blank=True, null=True)
    is_tor_aga = models.BooleanField(verbose_name=_('Тор Ага'), default=False)
    is_zam = models.BooleanField(verbose_name=_('Заместитель Тор Ага'), default=False)
    is_katchy = models.BooleanField(verbose_name=_('Катчы'), default=False)
    is_delegat = models.BooleanField(verbose_name=_('Делегат'), default=False)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.get_full_name()


class Rubrics(models.Model):
    title = models.CharField(max_length=24, verbose_name='Название рубрики')
    content = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="blog_posts")
    rubric_id = models.ForeignKey(Rubrics, on_delete=models.CASCADE, verbose_name='Рубрика')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name='Active')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)






