from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, ProductViews
from .serializers import (CategoryListSerializer, ProductSerializer,
                        CreateProductSerializer, ProductViewsSerializer,
                        ProductDetailSerializer)
from .permissions import IsOwnerAuth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CategoryListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    filter_backends = [DjangoFilterBackend]
    # queryset = Category.objects.all()

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class CategoryAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class ListProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter,)
    search_fields = ('title','user__username',)
    ordering_fields = ('created',)
    filter_fields = ('views',)
    queryset = Product.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = Product.objects.filter(user=user)
    #     return queryset

class CreateProductAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DestroyProductAPIView(DestroyAPIView):
    permission_classes = [IsOwnerAuth]
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()

class ProductViewsAPIView(ListAPIView):
    # permission_classes = [IsOwnerAuth]
    serializer_class = ProductViewsSerializer
    queryset = ProductViews.objects.all()


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if not ProductViews.objects.filter(product=product, ip=ip).exists():
            ProductViews.objects.create(product=product, ip=ip)

            product.views += 1
            product.save()
        serializer = ProductDetailSerializer(product, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

