from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SkinAnalysis
from .serializers import SkinAnalysisSerializer, AnalysisResultSerializer
from users.permissions import IsOwnerOrAdmin

class SkinAnalysisCreateView(generics.CreateAPIView):
    queryset = SkinAnalysis.objects.all()
    serializer_class = SkinAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnalysisResultsView(generics.RetrieveAPIView):
    queryset = SkinAnalysis.objects.all()
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = 'id'