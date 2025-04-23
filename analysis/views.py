from rest_framework import generics, permissions, status
from rest_framework.response import Response
import requests
from django.conf import settings
from .models import SkinAnalysis
from .serializers import SkinAnalysisSerializer, AnalysisResultSerializer
from users.permissions import IsOwnerOrAdmin

class SkinAnalysisCreateView(generics.CreateAPIView):
    queryset = SkinAnalysis.objects.all()
    serializer_class = SkinAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Validate the incoming image
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image file provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES['image']
        
        # Validate image type and size
        if not image_file.content_type.startswith('image/'):
            return Response(
                {"error": "Invalid file type - only images are allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if image_file.size > settings.MAX_UPLOAD_SIZE:
            return Response(
                {"error": f"Image too large. Max size is {settings.MAX_UPLOAD_SIZE/1024/1024}MB"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Send to AI service without auth header
            files = {'image': (image_file.name, image_file, image_file.content_type)}
            
            response = requests.post(
                settings.AI_SERVICE_URL,
                files=files,
                timeout=10  # seconds
            )
            response.raise_for_status()  # Raises exception for 4XX/5XX responses
            
            ai_data = response.json()
            
            # Save analysis to database
            analysis = SkinAnalysis.objects.create(
                user=request.user,
                image=image_file,
                results=ai_data['analysis'],
                confidence_scores=ai_data['confidence'],
                ai_model_version=ai_data.get('model_version')
            )
            
            # Return formatted response
            serializer = AnalysisResultSerializer(analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"AI service error: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except Exception as e:
            return Response(
                {"error": f"Processing error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
