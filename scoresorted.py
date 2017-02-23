import time

def score(sol,cachLatencies,requests,C,Ld):
    start_time = time.time()


    n_total_requests=0
    final_score =0
    for r in requests:
        videoID = r[0]
        endpointID = r[1]
        nrequests =r[2]

        n_total_requests+=nrequests

        Lmin= Ld[endpointID]

#        for cacheid in cachLatencies[endpointID].keys():
#            if sol[cacheid][videoID]==1:
#                Lmin=min(Lmin,cachLatencies[endpointID][cacheid])
#        for cacheid in cachLatencies[endpointID]:
#            if sol[cacheid[0]][videoID]==1:
#                Lmin=min(Lmin,cacheid[1])
        for cacheid in cachLatencies[endpointID]:
            if sol[cacheid[0]][videoID] == 1:
                Lmin=cacheid[1]
                break
                
                
        final_score+=(Ld[endpointID]-Lmin)*nrequests
    final_score=final_score*1000/n_total_requests
    
    print(time.time() - start_time)

    return final_score
