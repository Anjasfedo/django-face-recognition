from django.db import models

from django.contrib.auth.models import User
# Create your models here.

from PIL import Image
from . import face_app  # Import your face recognition logic module

import io

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(
        default='default-avatar.png', upload_to='users/', null=True, blank=True)
    embedding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Generate embedding if profile image is updated
        if self.profile_image:
            image = Image.open(self.profile_image)
            with io.BytesIO() as output:
                image.save(output, format='JPEG')
                output.seek(0)
                # Assuming generate_emb() takes a file-like object as input
                embedding = face_app.generate_emb(output)
            self.embedding = embedding.tostring()
            super().save(*args, **kwargs)  # Save the model again to update the embedding field
