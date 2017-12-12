from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import File


class FileView(APIView):
    def get(self, request, fileid):
        file = get_object_or_404(File, id=fileid)


