import time
import torch
import random
import pickle
import numpy as np
from tqdm import tqdm
from .Kmeans import K_means
import torch
import numpy as np

from Const_Var import Embeddings, Pos2SongId, SongId2Pos, Forbidden


def Recomend_fun(songlist, number, K=5):
    songidlist = [x['songid'] for x in songlist]
    scores = np.array([x['score'] for x in songlist])
    score_tensor = torch.tensor(scores)
    Indexes = [SongId2Pos[x] for x in songidlist]
    songset = set(songidlist)
    local_Embeddings = Embeddings.index_select(0, torch.tensor(Indexes))

    Kmeans_label = K_means(local_Embeddings.detach().numpy(), K)
    # print(Kmeans_label)

    Masks, Weights = [], []
    for k in range(K):
        mask = np.where(Kmeans_label == k)
        Masks.append(mask[0])
        Weights.append(np.sum(scores[mask[0]]))

    Weights = np.ceil(np.array(Weights) / np.sum(Weights) * number)
    Chosen = []
    for k, mask in enumerate(Masks):
        embeddings_k = local_Embeddings.index_select(0, torch.tensor(mask))
        wijs = Embeddings.matmul(embeddings_k.T)
        wijs *= score_tensor.index_select(0, torch.tensor(mask))
        ranking = wijs.sum(axis=1)

        values, indices = ranking.topk(int(Weights[k]) + scores.shape[0])
        cnt = 0
        for idx, pos in enumerate(indices):
            songid = Pos2SongId[pos.item()]
            if songid not in songset and songid not in Forbidden:
                Chosen.append((songid, values[idx].item()))
                cnt += 1
                if cnt == Weights[k]:
                    break

    return Chosen[:number]


def Recommend_Song(songid, number):
    selfEmb = Embeddings[SongId2Pos[songid]]
    ranks = Embeddings.matmul(selfEmb)
    values, indices = ranks.topk(number)
    Ans = [Pos2SongId[x.item()] for x in indices[:number]
           if x.item() not in Forbidden and x.item() != songid]
    return Ans
