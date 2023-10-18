import django_filters
from django import forms

from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    time_created = django_filters.DateFilter(field_name='time_created',
                                             widget=forms.DateInput(attrs={'type': 'date'}),
                                             lookup_expr='date__gt')

    class Meta:
        model = Post
        fields = ['author']
