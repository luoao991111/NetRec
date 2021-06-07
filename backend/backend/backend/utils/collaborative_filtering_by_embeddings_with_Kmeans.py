import time
import torch
import random
import pickle
import numpy as np
from tqdm import tqdm
from Kmeans import K_means

def IOU(set1, set2):
    return len(set1 & set2) / len(set1 | set2)

def collaborative_filtering_by_embeddings(userid, chosen_song_num, K=5):
    global uid2songid, songid2uid, songids, songid2id, id2songid, embeddings_torch
    record = uid2songid[userid]
    board = [tpl[0] for tpl in record]
    ids = [songid2id[song[0]] for song in record]
    scores = torch.tensor([song[1] for song in record])
    local_embeddings = embeddings_torch[ids]

    record = K_means(local_embeddings.detach().numpy(), K)
    masks = []
    weigths = []
    for k in range(K):
        mask = np.where(record == k)
        masks.append(mask)
        weigths.append(scores[mask].sum().item())
    weigths = np.ceil(np.array(weigths) / np.sum(weigths) * chosen_song_num)

    chosen = []
    for k, mask in enumerate(masks):
        embeddings_k = local_embeddings[mask]
        wijs = embeddings_torch.matmul(embeddings_k.T)
        wijs *= scores[mask]
        ranking = wijs.sum(axis=1)

        values, indices = ranking.topk(int(weigths[k])+scores.shape[0])

        cnt = 0
        for i in range(len(indices)):
            songid = id2songid[indices[i].item()]
            if songid not in board:
                chosen.append((songid, values[i].item()))
                cnt += 1
                if cnt == int(weigths[k]):
                    break

    return chosen[:chosen_song_num]

if __name__ == "__main__":
    with open("data/records.pickle", 'rb') as f:
        uid2songid = pickle.load(f)

    with open("data/songid2uid_pure.pickle", 'rb') as f:
        songid2uid = pickle.load(f)

    with open("data/songids.pickle", 'rb') as f:
        songids = pickle.load(f)

    with open("data/songid2id.pickle", 'rb') as f:
        songid2id = pickle.load(f)

    with open("data/song_infos.pickle", 'rb') as f:
        song_infos = pickle.load(f)

    id2songid = dict()
    for songid in songid2id:
        id2songid[songid2id[songid]] = songid

    embeddings = np.load("data/embeddings/embeddings_epoch=200_new.npy")
    embeddings /= np.sqrt(np.sum(embeddings**2, axis=1)).reshape(-1, 1)
    embeddings_torch = torch.tensor(embeddings)

    userid = 79792586
    time_start = time.time()
    chosen_song = collaborative_filtering_by_embeddings(userid, 100)
    time_end = time.time()
    print("[INFO] Use time:", time_end-time_start, "s")
    for i, song in enumerate(chosen_song):
        # print(i+1, song_infos[song[0]]['name'], song[1])
        print(str(i+1)+'.', song_infos[song[0]]['name'])
    exit()

    for userid in tqdm(uid2songid):
        chosen_song = collaborative_filtering_by_embeddings_faster(userid, 100)
