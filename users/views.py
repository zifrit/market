from django.db.models import Avg
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from clo.pagination import CustomPagination
from context import swagger_json
from shop.api.serializers import ViewProductSerializers
from shop.models import Product, CustomUserFavoriteProduct
from users.models import CustomUser
from .serializers import (
    PhoneNumberSerializer,
    VerifyCodeSerializer,
    CustomUserSerializer,
    UpdateCustomUserSerializer,
)


class RequestCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.save()
            return Response(
                {"message": "Код отправлен", "code": code}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            user_groups = serializer.validated_data["user_groups"]
            verification = serializer.validated_data["verification"]
            verification.is_used = True  # Помечаем код как использованный
            verification.save()

            # Генерируем refresh и access токены для пользователя
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access["roles"] = user_groups
            return Response(
                {
                    "message": "Успешный вход",
                    "refresh": str(refresh),  # Refresh-токен
                    "access": str(access),  # Access-токен
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CustomUserSerializer
        if self.request.method in ["PUT"]:
            return UpdateCustomUserSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        custom_user = (
            CustomUser.objects.select_related("userdata")
            .filter(id=kwargs["pk"])
            .first()
        )
        if not custom_user:
            return Response(
                {"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if (
            custom_user.id == request.user.id
            or request.user.is_superuser
            or "IsAdmin" in request.user_groups_name
        ):
            if serializer.is_valid():
                serializer.update(custom_user, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        result = super().retrieve(request, *args, **kwargs)
        if (
            self.get_object().id == request.user.id
            or request.user.is_superuser
            or "IsAdmin" in request.user_groups_name
        ):
            return result
        return Response(status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        if request.user.is_superuser or "IsAdmin" in request.user_groups_name:
            return result
        return Response(status=status.HTTP_403_FORBIDDEN)


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateCustomUserSerializer()
    queryset = CustomUser.objects.all()


class CreateViewUserFavoriteView(generics.ListCreateAPIView):
    serializer_class = ViewProductSerializers
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ViewProductSerializers
        if self.request.method == "POST":
            return None
        return None

    def get_queryset(self):
        user_id = self.request.user.id
        favorites_products = (
            Product.objects.filter(favorites__user_id=user_id)
            .select_related("brands", "category", "shop")
            .prefetch_related(
                "sizes",
                "color",
                "images__color",
                "ratings",
                "favorites",
            )
            .annotate(rating=Avg("ratings__rating"))
        )
        return favorites_products

    @extend_schema(
        parameters=[
            OpenApiParameter(name="page", type=int, description="Номер страницы"),
        ],
        examples=[
            OpenApiExample("get example", value=swagger_json.product_list_retrieve)
        ],
    )
    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="product_id", type=int, description="Продукт", required=True
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        product_id = self.request.query_params.get("product_id", False)
        if not product_id:
            return Response(
                {"error": "product_id is required field"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = self.request.user.id
        CustomUserFavoriteProduct.objects.create(user_id=user_id, product_id=product_id)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="product_id", type=int, description="Продукт", required=True
            ),
        ]
    )
    def delete(self, request):
        product_id = self.request.query_params.get("product_id", False)
        if not product_id:
            return Response(
                {"error": "product_id is required field"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = self.request.user.id
        CustomUserFavoriteProduct.objects.filter(
            user_id=user_id, product_id=product_id
        ).delete()
        return Response(status=status.HTTP_200_OK)
