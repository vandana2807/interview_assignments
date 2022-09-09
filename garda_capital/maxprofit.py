def maxProfit(a,k):
    preSum =[]
    preSum.append(a[0])
    for i in range(1,len(a)):
        preSum.append(preSum[i-1] + a[i])

    heap = []

    for i in range(0,k):
        heap.append(preSum[i])


    ans = max(heap)
    for i in range(k,len(preSum)):
        heap.remove(preSum[i-k])
        heap.append(preSum[i])
        ans=max(ans,(max(heap)-preSum[i-k]))


    preMaxAccu = 0

    for i in range(len(a)-k+1,len(a)):
        if(preMaxAccu >= 0):
            preMaxAccu += a[i]

        else:
            preMaxAccu = a[i];
        ans = max(ans, preMaxAccu);



    return ans

arr=[-3,4,3,-2,2,5]
k=4
print(maxProfit(arr,k))

arr = [4,3,-2,9,-4,2,7]
k = 6
n = len(arr)
print(maxProfit(arr, k))

arr = [5,-7,8,-6,4,1,-9]
k = 5
n = len(arr)
print(maxProfit(arr, k))
