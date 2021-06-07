import time
import random
import pickle
import numpy as np

def pick_k_points_random(K, pntFeatures):
    random.seed(time.time())
    array = []
    N = pntFeatures.shape[0]
    for i in range(K):
        array.append(random.randint(0, N-1))
    return pntFeatures[array]

def pick_k_points_farthest(K, pntFeatures):
    random.seed(time.time())
    p1 = random.randint(0, pntFeatures.shape[0]-1)
    array = [p1]
    for i in range(K-1):
        tmps = None
        for p in array:
            # tmp = np.array([pntFeatures.dot(pntFeatures[p]) / np.sqrt(np.sum(pntFeatures**2, axis=1) * np.sum(pntFeatures[p]**2))])
            tmp = np.array([np.sum((pntFeatures-pntFeatures[p])**2, axis=1)])
            if tmps is None:
                tmps = tmp
            else:
                tmps = np.concatenate((tmps, tmp), axis=0)
        tmps = np.min(tmps, axis=0)
        array.append(np.argmax(tmps))
    return pntFeatures[array]

# def find_the_nearest_cluster(pnts, centroids):
#     distances = pnts.dot(centroids.T) / np.sqrt(np.sum(pnts**2, axis=1)).reshape(-1, 1).dot(np.sqrt(np.sum(centroids**2, axis=1)).reshape(1, -1))
#     return np.argmax(distances, axis=1)

def find_the_nearest_cluster(pnts, centroids):
    tmp1 = np.tile(np.array([centroids]), (pnts.shape[0], 1, 1))
    tmp2 = np.tile(np.array([pnts]), (centroids.shape[0], 1, 1)).transpose(1, 0, 2)
    distances = (np.sum((tmp1-tmp2)**2, axis=2))
    return np.argmin(distances, axis=1)

def K_means(embeddings, K):
    N = embeddings.shape[0]

    # Pick K points
    centroids = pick_k_points_farthest(K, embeddings)

    count = 1
    test = False
    while True:
        new_centroids = []
        # Assign all points to their closest centroid
        record = find_the_nearest_cluster(embeddings, centroids)
        for i in range(K):
            # Update all the centroids
            cluster = embeddings[np.where(record == i)]
            new_centroid = np.sum(cluster, axis=0) / cluster.shape[0]
            new_centroids.append(new_centroid)
        new_centroids = np.array(new_centroids)
        if test:
            print(count)
            count += 1
            dis = np.sum((centroids - new_centroids)**2, axis=1)
            print(dis)
            print("-------------------------------")
        if (centroids == new_centroids).all():
            break
        centroids = new_centroids

    return record

if __name__ == "__main__":

    with open("data/records.pickle", 'rb') as f:
        uid2songid = pickle.load(f)
    with open("data/songid2id.pickle", 'rb') as f:
        songid2id = pickle.load(f)
    with open("data/song_infos.pickle", 'rb') as f:
        song_infos = pickle.load(f)

    id2songid = dict()
    for songid in songid2id:
        id2songid[songid2id[songid]] = songid

    K = 5

    embeddings = np.load("data/embeddings/embeddings_epoch=200_new.npy")

    uid = 79792586
    # for uid in uid2songid:
    #     if random.random() > 0.9:
    #         break
    # print(uid)
    songids = [song[0] for song in uid2songid[uid]]
    tmpids = [songid2id[song[0]] for song in uid2songid[uid]]
    sub_embeddings = embeddings[tmpids]
    sub_embeddings /= np.sqrt(np.sum(sub_embeddings**2, axis=1)).reshape(-1, 1)

    print("K =", K)

    record = K_means(sub_embeddings, K)

    W_K = 0
    for k in range(K):
        # print("cluster", k)
        mask = np.where(record == k)
        D_k = 0
        sub_sub_embeddings = sub_embeddings[mask]
        for id in mask[0]:
            print(song_infos[songids[id]]["name"])
            D_k += np.sum(1 - sub_sub_embeddings.dot(sub_embeddings[id]) / np.sqrt(np.sum(sub_sub_embeddings**2, axis=1) * np.sum(sub_embeddings[id]**2)))
        # print(k, D_k / len(mask[0]))
        W_K += D_k / len(mask[0])
        print("--------------------------------")
    # print(K, W_K)
    # print("--------------------------------")
