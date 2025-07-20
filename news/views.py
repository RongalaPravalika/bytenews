from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from .models import Article, Category
from django.shortcuts import render
from django.views.generic import TemplateView


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-published_date')
        category = self.request.GET.get('category')
        query = self.request.GET.get('q')

        # ✅ Filter by category if provided
        if category:
            queryset = queryset.filter(category__name__iexact=category)

        # ✅ Apply search filter
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(article_count=Count('article'))
        context['current_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

class HomePageView(TemplateView):
    template_name = 'news/homepage.html'


def landing_page(request):
    return render(request, 'landing.html') 

