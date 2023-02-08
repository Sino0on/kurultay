from django.db import models
from kurultai.models import Account as User
from django.urls import reverse


class Voting(models.Model):
    title = models.CharField(max_length=123)
    content = models.TextField()
    chat = models.OneToOneField('Chat', on_delete=models.CASCADE, related_name='voting_chat')

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=40)
    users = models.ManyToManyField(User, related_name='users_votes', blank=True, null=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='questions_vote')

    def __str__(self):
        return self.title

    def get_total_votes(self):
        return self.users.count()


class News(models.Model):
    title = models.CharField(max_length=123)
    preview = models.CharField(max_length=244)
    content = models.TextField()
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='news/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_news', args=[self.pk])


class Chat(models.Model):
    title = models.CharField(
        max_length=123,
        verbose_name='Название',
        default='.',
        blank=True
    )
    description = models.TextField(
        default='.',
        blank=True
    )
    avatar = models.ImageField(
        upload_to='images/avatars/%Y/%m/%d/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавление'
    )
    is_privat = models.BooleanField(
        default=False,
        blank=True
    )
    users = models.ManyToManyField(User, related_name='chats_user')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-date']


class Message(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField(
        verbose_name='Сообщение'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавление'
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщении'


class QuestionMessage(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    image = models.ImageField(upload_to='questionmessage/', blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_questions')
    created_date = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(User, related_name='to_user_questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос от товарища'
        verbose_name_plural = 'Вопросы от людей'
        ordering = ['-created_date']

