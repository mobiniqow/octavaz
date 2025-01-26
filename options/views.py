from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Options
from .serializers import OptionsSerializer

class OptionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # فقط یک آبجکت را بازگرداند
        options = Options.objects.first()
        if options:
            serializer = OptionsSerializer(options)
            return Response(serializer.data)
        return Response({"detail": "No options object exists."}, status=status.HTTP_404_NOT_FOUND)
