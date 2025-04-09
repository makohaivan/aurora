from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product, Recommendation
from .serializers import ProductSerializer, RecommendationSerializer
from analysis.models import SkinAnalysis
from .matcher import ProductMatcher
from users.permissions import IsOwnerOrAdmin

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by query params
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class UserRecommendationsView(generics.ListAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Recommendation.objects.filter(
            user=self.request.user
        ).select_related('product', 'analysis')
    

class GenerateRecommendationsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, analysis_id):
        try:
            analysis = SkinAnalysis.objects.get(
                id=analysis_id,
                user=request.user  # Ensure ownership
            )
            
            # Get recommendations
            products = ProductMatcher.recommend(
                analysis_data=analysis.results,
                user_preferences=request.data.get('preferences')
            )
            
            # Create recommendation records
            created_recs = []
            for product in products:
                rec = Recommendation.objects.create(
                    user=request.user,
                    product=product,
                    analysis=analysis,
                    reason=f"Recommended for {', '.join(analysis.results['conditions'])}"
                )
                created_recs.append(rec)
            
            # Return serialized results
            serializer = RecommendationSerializer(created_recs, many=True)
            return Response(serializer.data)
            
        except SkinAnalysis.DoesNotExist:
            return Response(
                {"error": "Analysis not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
