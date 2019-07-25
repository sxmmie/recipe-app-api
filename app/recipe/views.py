from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# from core.models import Tag
# from ..recipe import serializers
from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned recipe sttributes"""
    authentication_classes = (TokenAuthentication,) # token authentication is used
    permission_classes = (IsAuthenticated,) # user is required to be authenticated

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self):
        """Create a new tag"""
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()    # queryset to return
    serializer_classes = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage Ingrediens in the database"""
    queryset = Ingredient.objects.all()    # queryset to return
    serializer_classes = serializers.TagSerializer
