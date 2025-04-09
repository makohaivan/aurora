from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/', include('users.urls')),
    path('api/analysis/', include('analysis.urls')),
    path('api/recommendations/', include('recommendations.urls', namespace='recommendations')),
    path('api/consultations/', include('consultations.urls', namespace='consultations')),
    path('api/admin', include('admin_panel.urls')),
]
