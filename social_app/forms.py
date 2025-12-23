from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta: # Определяем метаинформацию для формы
        model = Post # Указываем модель, с которой связана форма то есть берёт со скалда( модели Post)
        fields = ['text'] # Указываем поля модели, которые будут включены в форму и берёт это из модели Post
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Что у вас нового?', 'class': 'post-input'}) # Textarea это виджет для многострочного текстового ввода а attrs позволяет задать HTML-атрибуты для виджета и attrs={'placeholder': 'Что у вас нового?', 'class': 'post-input'} задаёт плейсхолдер и CSS класс для стилизации
        }

class CommentForm(forms.ModelForm): # Создаем форму для модели Comment
    class Meta:
        model = Comment # Указываем модель, с которой связана форма то есть берёт со скалда( модели Comment)
        fields = ['text'] # Указываем поля модели, которые будут включены в форму и берёт это из модели Comment
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Написать комментарий…'}) # Textarea это виджет для многострочного текстового ввода а attrs позволяет задать HTML-атрибуты для виджета и attrs={'placeholder': 'Написать комментарий…'} задаёт плейсхолдер для стилизации
        }