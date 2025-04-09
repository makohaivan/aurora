from django.urls import path
from .views import SkinAnalysisCreateView, AnalysisResultsView

urlpatterns = [
    path('analyze/', SkinAnalysisCreateView.as_view(), name='analyze-image'),
    path('results/<int:id>/', AnalysisResultsView.as_view(), name='analysis-results'),
]