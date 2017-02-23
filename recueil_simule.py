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


def get_voisins(graph, M):
    crit = .5
    voisins = []
    div = len(M)
    while(len(voisins)==0):
        for q in graph:
            cur = np.multiply(q.state,M)
            val_q = np.multiply(q.state,q.state)
            val_M = np.multiply(M,M)
            cur = np.sum(cur,axis=None)/np.min([val_M, val_q])

            if cur>crit:
                voisins.append(q)
        crit = crit-.1
    return voisins


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
        if len(graph)>1:
            graph[-1].linkneighbours(get_voisins(graph[:len(graph)-1],M))
        if j%100==0:
            print(j)

    return graph

def line_ok(line):
    return sum(int(S[i]) for i in range(len(line)) if line[i] == 1) <= X

def create_M_2(n_pop):
        
    # pour chaque cache server
    M = np.zeros((C,V))

    for i in range(C):
        shuffled_videos = np.arange(V)
        np.random.shuffle(shuffled_videos)
        for v in shuffled_videos:
            tmp = M[i].copy()
            tmp[v] = 1
            if line_ok(tmp):
                M[i,v] = 1


    return M




graph = create_graph(S,X,requests,cacheLatencies,C,V,Ld,3000)
resultat = graph[0].hasting(20000,1000000,.999)

print(resultat.value)
print(score(resultat.state,cacheLatencies,requests,C,Ld))
