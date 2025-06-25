from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete_at = timezone.now()
        obj.save()
        print(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomDestroyAPIView(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete_at = timezone.now()
        obj.save()
        print(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
