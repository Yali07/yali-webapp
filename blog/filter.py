import django_filters
from .models import BlogPost

class BlogFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = BlogPost
        fields = ['title']