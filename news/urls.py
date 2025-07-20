from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),  # ✅ This name='home' must exist!
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]
