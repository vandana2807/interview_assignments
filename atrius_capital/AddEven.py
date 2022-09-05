def addEven(graph):
    odd = 0
    odd_vertices = []
    for i in range(0,len(graph)):
        deg=0
        for j in range(0,len(graph[i])):
            if graph[i][j]:
                deg+=1
        if deg%2==1:
            odd+=1
            odd_vertices.append(i)

    if (odd == 0) :
        return True
    elif (odd == 2):
        a = odd_vertices[0]
        b = odd_vertices[1]
        for k in range(0,len(graph)):
            if not graph[a][k] and not graph[b][k]:
                return True
        
        return False
    elif (odd == 4):
        a = odd_vertices[0]
        b = odd_vertices[1]
        c = odd_vertices[2]
        d = odd_vertices[3]
        if ((not graph[a][b] and not graph[c][d]) or
            (not graph[a][c] and not graph[b][d]) or
            (not graph[a][d] and not graph[b][c])) :
            return True
        
        return False
    else:
        return False
#keep first letter as capital
graph = [[False, True, False, False],
         [True, False, True, False],
         [False, True, False, True],
         [False, False, True, False]]
addEven(graph)

graph = [[False, True, True, True],
[True, False, True, False],
[True, True, False, True],
[True, False, True, False]]
addEven(graph)
