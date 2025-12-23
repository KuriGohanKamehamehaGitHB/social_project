from django.shortcuts import render, redirect, get_object_or_404 # Скажете почему написано get object_or_404? Потому что это удобный способ получить объект из базы данных или вернуть ошибку 404, если объект не найден
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from .forms import PostForm, CommentForm # Импортируем формы из forms.py для создания постов и комментариев

# 1. Главная страница
def index(request):
    posts = Post.objects.all().order_by('-created_at') # Получаем все посты, отсортированные по дате создания (новые первыми). Post.objects.all() возвращает все объекты модели Post а order_by('-created_at') сортирует их по полю created_at в порядке убывания (от новых к старым)
    return render(request, 'index.html', {'posts': posts}) # Рендерим шаблон index.html и передаем в него контекст с постами

# 2. Детальная страница поста + Комментарии
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # Получаем пост по первичному ключу (pk) или возвращаем 404 ошибку, если пост не найден
    
    # Обработка формы комментария
    if request.method == 'POST': # Проверяем, был ли отправлен POST-запрос (форма комментария)
        if not request.user.is_authenticated: # Проверяем, авторизован ли пользователь
            return redirect('login') # Если не авторизован, перенаправляем на страницу логина
        form = CommentForm(request.POST) # Создаем форму комментария с данными из запроса
        if form.is_valid(): # Проверяем, валидна ли форма
            comment = form.save(commit=False) # Создаем объект комментария, но не сохраняем его в базу данных сразу
            comment.post = post # Связываем комментарий с текущим постом
            comment.author = request.user # Устанавливаем автора комментария как текущего пользователя
            comment.save()  # Сохраняем комментарий в базу данных
            return redirect('post_detail', pk=pk) # Перенаправляем обратно на детальную страницу поста
    else:
        form = CommentForm() # Если запрос не POST, создаем пустую форму комментария

    # Проверяем, лайкнул ли текущий юзер этот пост (для отображения текста)
    user_has_liked = False # Изначально считаем, что пользователь не лайкал пост
    if request.user.is_authenticated: # Проверяем, авторизован ли пользователь
        if post.likes.filter(id=request.user.id).exists(): # Проверяем, есть ли лайк от текущего пользователя
            user_has_liked = True # Если есть, устанавливаем флаг в True

    return render(request, 'detail.html', {
        'post': post, # Передаем пост в шаблон то есть берёт со скалда( модели Post) чтобы связать с комментарием
        'comments': post.comments.all().order_by('-created_at'), # Получаем все комментарии к посту, отсортированные по дате создания (новые первыми)
        'form': form, # forms.py который создан для модели Comment нужен для рендеринга формы комментария в шаблоне
        'user_has_liked': user_has_liked # Передаем информацию о том, лайкал ли пользователь пост
    })

# 3. Лайк поста
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user) # Убрать лайк
    else:
        post.likes.add(request.user) # Поставить лайк
    # Возвращаем пользователя туда, откуда он пришел (или в деталку)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

# 4. Создание поста
@login_required # Декоратор, требующий авторизацию для доступа к представлению и работает только для авторизованных пользователей
def create_post(request):
    if request.method == 'POST': # Проверяем, был ли отправлен POST-запрос (форма создания поста)
        form = PostForm(request.POST) # Создаем форму поста с данными из запроса
        if form.is_valid(): # Проверяем, валидна ли форма
            post = form.save(commit=False) # Создаем объект поста, но не сохраняем его в базу данных сразу
            post.author = request.user # Устанавливаем автора поста как текущего пользователя
            post.save() # Сохраняем пост в базу данных
            return redirect('index') # Перенаправляем на главную страницу после создания поста
    else:
        form = PostForm() # Если запрос не POST, создаем пустую форму поста
    return render(request, 'post_creat.html', {'form': form}) # Рендерим шаблон создания поста и передаем в него форму

# 5. Регистрация пользователя
def register(request): 
    if request.method == "POST": # Проверяем, был ли отправлен POST-запрос (форма регистрации)
        form = UserCreationForm(request.POST) # Создаем форму регистрации с данными из запроса
        if form.is_valid(): # Проверяем, валидна ли форма
            user = form.save() # Сохраняем нового пользователя в базу данных
            login(request, user) # Логиним пользователя сразу после регистрации
            return redirect('index') # Перенаправляем на главную страницу после регистрации
    else:
        form = UserCreationForm() # Если запрос не POST, создаем пустую форму регистрации
    return render(request, 'register.html', {'form': form}) # Рендерим шаблон регистрации и передаем в него форму

