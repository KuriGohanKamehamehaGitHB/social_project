from django.db import models
from django.contrib.auth.models import User # Импортируем встроенную модель пользователя Django

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор") # Связь с пользователем при помощи ForeignKey которое говорит, что один пользователь может иметь много постов
    text = models.TextField(verbose_name="Текст поста") # Текст поста в виде TextField которое позволяет хранить большие объемы текста
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания") # Дата и время создания поста, автоматически устанавливается при создании c помощью DateTimeField
    # Лайки реализуем через ManyToMany
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True) # Связь многие ко многим с пользователями, которые лайкнули пост и позволяет хранить множество лайков от разных пользователей

    def total_likes(self):
        return self.likes.count() # Метод для подсчета общего количества лайков поста действие которое возвращает количество лайков и делает всё это через count() и django ORM

    def __str__(self):
        return f"Пост {self.author.username} в {self.created_at}" # Метод для строкового представления модели, возвращает имя автора и дату создания поста

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # Связь с постом при помощи ForeignKey которое говорит, что один пост может иметь много комментариев
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Связь с пользователем при помощи ForeignKey которое говорит, что один пользователь может иметь много комментариев
    text = models.TextField(verbose_name="Комментарий") # Текст комментария в виде TextField которое позволяет хранить большие объемы текста а verbose_name для удобства администрирования
    created_at = models.DateTimeField(auto_now_add=True) # Дата и время создания комментария, автоматически устанавливается при создании c помощью DateTimeField

    def __str__(self):
        return f"Коменатрии от {self.author.username}" # Метод для строкового представления модели, возвращает имя автора комментария