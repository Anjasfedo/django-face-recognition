from django.shortcuts import render


# 

import uuid
import base64
import os

from core import settings

from . import face_app

from . import utils

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponseServerError, JsonResponse
# Create your views here.

def index(request):
    context = {}
    
    return render(request, 'index.html', context)

def check_face(request):
    if request.method == 'POST':
        filename = str(uuid.uuid4())
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        image_b64 = request.POST.get('imageBase64')
        imgstr = image_b64.split(',')[1]
        output = open(file_path, 'wb')
        decoded = base64.b64decode(imgstr)
        output.write(decoded)

        user_ids = []
        names = []
        score, idx = face_app.get_similarity(
            file_path, utils.EmbeddingsDataset().embeddings)
        os.remove(file_path)

        if score is not None:
            user = User.objects.get(id=utils.EmbeddingsDataset().user_ids[idx])
            if user:
                data = {
                    'id': user.id,
                    'name': user.username,
                    'score': round(score * 100, 2)
                }
                login(request, user)
                return JsonResponse(data)
        return HttpResponseServerError('Invalid user')
