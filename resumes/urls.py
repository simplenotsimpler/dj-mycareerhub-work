from django.urls import path
from . import views
from .views import ResumeDetailView

urlpatterns = [
    path('<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('<int:pk>/word/', views.get_word, name='get_word_with_pk')
]