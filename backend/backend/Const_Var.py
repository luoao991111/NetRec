from backend.settings import BASE_DIR
import pickle

import os
with open(os.path.join(BASE_DIR, 'songid2embeddings.pickle'), 'rb') as Fin:
    SongId2Emb = pickle.load(Fin)
