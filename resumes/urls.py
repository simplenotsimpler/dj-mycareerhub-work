from django.urls import path
from .views import ResumeDetailView, ResumeDocxView

urlpatterns = [
    path('<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    # path('<int:pk>/word/', views.get_word, name='get_word_with_pk')
    path('<int:pk>/word/', ResumeDocxView.as_view(), name='get_word_with_pk')
]
