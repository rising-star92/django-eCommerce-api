from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, ProductViews
from drf_extra_fields.fields import Base64ImageField


class CategoryListSerializer(serializers.ModelSerializer):
    # lft = serializers.SlugRelatedField(slug_field='lft', read_only=True)
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        fields = "__all__"


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class ProductDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()
    def get_category(self, obj):
        return obj.category.name

        
    class Meta:
        model = Product
        fields = "__all__"

class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        fields = "__all__"