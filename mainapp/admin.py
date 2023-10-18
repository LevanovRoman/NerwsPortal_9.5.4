from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'get_category_list', 'type', 'time_created', 'title', 'slug', 'rating')
    list_display_links = ('id', 'author')
    prepopulated_fields = {"slug": ("title",)}
    filter_vertical = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'get_users_list')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'post_per_day')
    list_display_links = ('id', 'user')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'time_created', 'text', 'rating')
    list_display_links = ('id', 'post')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'category')
    list_display_links = ('id', 'post')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
