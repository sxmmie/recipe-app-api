from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# from core.models import Tag
# from ..recipe import serializers
from core.models import Tag, Ingredient
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,) # token authentication is used
    permission_classes = (IsAuthenticated,) # user is required to be authenticated
    queryset = Tag.objects.all()    # queryset to return
    serializer_classes = serializers.TagSerializer

    def query_set(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Ingrediens in the database"""
    authentication_classes = (TokenAuthentication,) # token authentication is used
    permission_classes = (IsAuthenticated,) # user is required to be authenticated
    queryset = Ingredient.objects.all()    # queryset to return
    serializer_classes = serializers.TagSerializer

    def query_set(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
