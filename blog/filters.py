import django_filters
from .models import Post, Category


class PostFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['category']
