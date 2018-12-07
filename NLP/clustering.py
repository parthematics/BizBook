import pickle

embedding_to_terms = {}
cluster_to_points = {}

def map_clusters(cluster_num=100):
    num_clusters = cluster_num
    points = [term[2] for term in terms_with_embeddings]
    file_name = "cluster_file.txt"
    
    for i, data in enumerate(points):
        embedding_to_terms[data.tostring()] = [terms_with_embeddings[i][1], terms_with_embeddings[i][0]]
        
    kmeans = tf.contrib.factorization.KMeansClustering(num_clusters=num_clusters, use_mini_batch=False)

    def input_fn():
        return tf.train.limit_epochs(tf.convert_to_tensor(points, dtype=tf.float32), num_epochs=1)
    
    # train clusters
    prevBest = float("inf")
    kmeans.train(input_fn)
    currBest = kmeans.score(input_fn)
    while (prevBest - currBest > 0.1):
        prevBest = currBest
        kmeans.train(input_fn)
        currBest = kmeans.score(input_fn)
        cluster_centers = kmeans.cluster_centers()
        print('score:', currBest)
        
    cluster_indices = list(kmeans.predict_cluster_index(input_fn))
    
    # map the input points to their clusters
    for i, point in enumerate(points):
        cluster_index = cluster_indices[i]
        center = cluster_centers[cluster_index]
        if center not in self.cluster_to_points.keys():
            cluster_to_points[center] = []
        cluster_to_points[center].append(point.tolist())
        
    # once optimal cluster number is determined, clusters are saved to a file
    with open(file_name, 'wb') as f:
        pickle.dump(cluster_to_points, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

map_clusters()