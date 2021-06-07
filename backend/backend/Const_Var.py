from backend.settings import BASE_DIR
import pickle
import os
import torch

with open(os.path.join(BASE_DIR, 'songid2embeddings.pickle'), 'rb') as Fin:
    SongId2Emb = pickle.load(Fin)

Embeddings = []
Pos2SongId, SongId2Pos = {}, {}

for k, v in SongId2Emb.items():
    Embeddings.append(v)
    Pos2SongId[len(Embeddings) - 1] = k
    SongId2Pos[k] = len(Embeddings) - 1

Embeddings = torch.tensor(Embeddings, requires_grad=False)
Embeddings = Embeddings / \
    torch.sqrt(torch.sum(Embeddings * Embeddings, 1)).reshape(-1, 1)
