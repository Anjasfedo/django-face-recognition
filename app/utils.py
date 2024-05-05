from .models import Profile
import numpy as np


class EmbeddingsDataset():

    def __init__(self):
        self.user_ids = []
        self.embeddings = []

        profiles = Profile.objects.all()
        for p in profiles:
            if p.embedding is not None:
                e = np.frombuffer(p.embedding, dtype=np.float32)
                self.user_ids.append(p.user.id)
                self.embeddings.append(e)
