from collections import deque
def floor_key(d, key):
    if key in d:
        return key
    elif key not in d:
       
        c=[k for k in d if k < key]
        if len(c)>0:
            return max(k for k in d if k < key)
        else:
            return c
    #else:
    #    return None
def queued_seats(n,tickets):
    
    pnts=[]
    setd={}
    ans=[None]*n
    #pntDeque = deque(maxlen=len(n)+1)
    for i in range(0,n+1):

        pnts.append(deque(maxlen=n+1))

    for i in range(0,n):
        pnts[tickets[i]].append(i)
        setd[tickets[i]]=True 
    
    seat=1
    
    while len(setd)!=0:
        #print(k,setd[k])
        #try:  
        cand = floor_key(setd,seat);
        #print("cand,seat",cand,seat,isinstance(cand, int))
        if isinstance(cand, int):
            #print("seat",seat)
            #print("cand",str(cand)+"="+str(setd[cand]))
            
            i = pnts[cand].popleft()
            
            ans[i] = seat
            #print("i",i)
            #print("ans[i]",ans[i])
            if len(pnts[cand])==0:
                del setd[cand]
                #print(setd)            
        #print(len(setd))
        seat=seat+1
        #continue
        

        
    return ans

print(queued_seats(5,[1,2,3,2,4])==[1, 2, 3, 5, 4])
print(queued_seats(4,[4, 1, 3, 2])==[4, 1, 3, 2])
print(queued_seats(3,[1,1,1])==[1, 2, 3])
print(queued_seats(5,[2,5,1,5,2])==[2, 5, 1, 6, 3])
