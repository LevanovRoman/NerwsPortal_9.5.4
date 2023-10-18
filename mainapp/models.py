from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.template.defaultfilters import slugify

from .config import transliteration


POST_TYPE_CHOICES = [
    ("St", "Статья"),
    ("Nv", "Новость"),
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    post_per_day = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.user)

    def update_rating(self):
        if self.user.user_comment.all():
            sum_rating_comment = self.user.user_comment.aggregate(res=Sum('rating'))['res']
        else:
            sum_rating_comment = 0

        author_posts = self.author_post.all()
        if author_posts:
            sum_rating_post = author_posts.aggregate(res=Sum('rating'))['res']
            comment_list = [i.post_comment.aggregate(res=Sum('rating'))['res'] for i in author_posts]
            sum_rating_comment_to_posts = sum(comment_list)
        else:
            sum_rating_post = sum_rating_comment_to_posts = 0

        self.rating = sum_rating_comment + sum_rating_post*3 + sum_rating_comment_to_posts

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    subscribers = models.ManyToManyField(User, verbose_name='Подписки', related_name='followers', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def get_users_list(self):
        queryset_users = self.subscribers.values()
        return [i['username'] for i in queryset_users]


class Post(models.Model):
    STATYA = "St"
    NOVOST = "Nv"
    POST_TYPE_CHOICES = [
        (STATYA, "Статья"),
        (NOVOST, "Новость"),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_post', verbose_name='Автор')
    type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=NOVOST, verbose_name='Тип поста')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    category = models.ManyToManyField(Category, through="PostCategory", verbose_name='Категория', related_name='cats')
    title = models.CharField(max_length=255, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def update_post_per_day(self):
        self.author.post_per_day += 1

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        return self.text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def get_category_list(self):
        queryset_category = self.category.values()
        return [i['name'] for i in queryset_category]

    def save(self, *args, **kwargs):
        string = transliteration(self.title)
        self.slug = slugify(string)
        super(Post, self).save(*args, **kwargs)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f"{self.post} - {self.category}"

    class Meta:
        verbose_name = 'Пост-Категория'
        verbose_name_plural = 'Посты-Категории'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment', verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return f"Post: {self.post} - user: {self.user} - rating: {self.rating}"

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


