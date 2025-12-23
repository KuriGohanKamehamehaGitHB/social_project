from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from social_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'), # Детальная страница поста с комментариями и тут возник вопрос? Почему pk а не id? Потому что pk это primary key (первичный ключ) и в Django по умолчанию primary key это поле id. Использование pk делает код более универсальным, так как если в будущем primary key будет изменен на другое поле, код все равно будет работать.   
    path('post/create/', views.create_post, name='create_post'), # pk это первичный ключ (уникальный идентификатор записи в базе данных) и используется для получения конкретного поста из базы данных. Id это конкретное поле то есть реляционная база данных, где id это имя столбца, который хранит первичный ключ. В Django pk это абстракция, которая ссылается на первичный ключ модели, независимо от того, как он называется в базе данных.
    path('post/<int:pk>/like/', views.like_post, name='like_post'), # Лайк поста по его первичному ключу (pk) Это абстракция а значит псевдоним а id это реальное имя поля в базе данных.
     
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]