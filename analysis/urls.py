from django.urls import path
from .views import SkinAnalysisCreateView

urlpatterns = [
    path('analyze/', SkinAnalysisCreateView.as_view(), name='analyze-image'),
]