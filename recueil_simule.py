from graph import *
from reader import *
from score import score

S = np.array(S)
def verify(S,M,X):
    for i in range(len(X)):
        if np.dot(M[i,:], S)>X:
            return False
    return True

def latency_endpoint(M,film,latences,endpoint,lat_db):
    lat = lat_db
    latency = latences[endpoint]
    for key, value in latency.items():
        c = M[int(key),film]*value
        if c<lat and c>0:
            lat = c

    return lat

def value(M,R,L,lat_dbs):
    val=0
    for video, endpoint ,value in R:
        lat = latency_endpoint(M, video, L, endpoint, lat_dbs[endpoint])

        val += value/lat
    return val



def create_M(S,X, size):
    M = np.zeros(size)
    inv_S = np.reciprocal(S)
    par = 1

    probs = (np.max(inv_S))*np.ones(len(S)) - par*inv_S

    probs = probs/sum(probs)
    for i in range(size[0]):
        indices = -1
        while(np.dot(S,M[i,:])<X):
            if indices>-1:
                M[i, int(indices)]=1
            indices = np.random.choice(size[1], p = probs)

    return M


def create_graph(S,X,R,L,N_cache, N_films, lat_dbs,qt):
    graph = []
    size=(N_cache,N_films)
    for j in range(qt):
        M = create_M(S,X,size)
        val = score(M,L,R,N_cache,lat_dbs)

        graph.append(node(M,val))
        graph[-1].linkneighbours(graph[:len(graph)-1])
    return graph


graph = create_graph(S,X,requests,cacheLatencies,C,V,Ld,30000)
resultat = graph[0].hasting(20000,1000000,.999)

print(resultat.value)
print(score(resultat.state,cacheLatencies,requests,C,Ld))
