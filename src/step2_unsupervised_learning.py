import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from data_cleanup import remove_stopwords_and_tfidf
from utils import getStoredModelFromTopic, getDataFilenameFromTopic,writeModelToFile

def get_cleaned_data(topic):
    """
    get tweets stored on file, remove stopwords and do TFIDF
    :returns: 
        X: Matrix converting sentences to TFIDF values. 
            Size = numOfSentences,numOfUniqueWords)
        vectorizer : TF-IDF Vectorizer.
    """
    filename = getDataFilenameFromTopic(topic)
    tweets = [line.rstrip('\n').lower() for line in open(filename)]
    # 2. remove stopwords, do tfidf
    X, vectorizer = remove_stopwords_and_tfidf(tweets)
    return X, vectorizer

# 3. do elbow method
def elbow_method(X):
    """
    Carry out the elbow method - do KMeans on several values of number of clusters. 
    And give a plot showing how the error changes.
    """
    Sum_of_squared_distances = []
    K=range(1,15)
    for k in K:
        print("elbow method - doing kmeans for K=",k)
        model = doKMeans(k,X)
        Sum_of_squared_distances.append(model.inertia_)

    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()

# 4. Do unsupervised learning
def doKMeans(num_cluster,X):
    """
    Do KMeans on a given number of clusters and data
    :returns:
        model : KMeans learned model
    """
    model = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    return model

def printClusterCentroidFeatureNames(topic):
    """
    Prints first 20 feature of each cluster.
    topic: int
    """
    vectorizer, model, n_cluster = getStoredModelFromTopic(topic)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    # prints keywords in each cluster
    for i in range(n_cluster):
        print("\nCluster %d:" % (i+1))
        for ind in order_centroids[i, :20]:
            print(' %s' % terms[ind], end='')


if __name__ == '__main__' :

    topic=int(input("Which topic (1 for brexit / 2 for corona)?: "))
    #TODO: Convert topic to enum!
    print("1. Train new model")
    print("2. Get trained KMeans cluster info")
    trainOrNot = int(input("Enter your choice [1/2]: "))    

    if(trainOrNot==2):    
        printClusterCentroidFeatureNames(topic)
    else:
        X,vectorizer = get_cleaned_data(topic)
        print("done cleaning data")
        elbow_method(X)
        user_input = input("Number of clusters needed: ")
        n_cluster = int(user_input) # obtained after doing elbow method
        model = doKMeans(n_cluster,X)

        # prints keywords in each cluster
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        for i in range(n_cluster):
            print("\nCluster %d:" % (i+1))
            for ind in order_centroids[i, :20]:
                print(' %s' % terms[ind], end='')

        file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
        #Save model and vectorizer:
        writeModelToFile(model,vectorizer,file_name)