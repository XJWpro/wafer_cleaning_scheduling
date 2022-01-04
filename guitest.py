import copy
import numpy as np
def A():
    k=2
    m=[2,5]
    o=[100,240]
    c=123.6667
    ε = 5
    η = 3
    wafer = [[[1, 0], [1, 1, 1, 0, 0]],
             [[2, 0], [2, 1, 1, 0, 0]],
             [[0, 1], [2, 2, 1, 0, 0]],
             [[0, 2], [2, 2, 2, 0, 0]],
             [[1, 0], [0, 2, 2, 1, 0]],
             [[2, 0], [0, 0, 2, 1, 1]],
             [[0, 1], [1, 0, 0, 1, 1]],
             [[0, 2], [1, 0, 0, 2, 1]],
             [[1, 0], [1, 0, 0, 2, 2]],
             [[2, 0], [2, 0, 0, 2, 2]],
             [[0, 1], [2, 1, 0, 0, 2]],
             [[0, 2], [2, 1, 1, 0, 0]],
             [[1, 0], [0, 1, 1, 1, 0]],
             [[2, 0], [0, 2, 1, 1, 0]],
             [[0, 1], [0, 2, 2, 1, 0]],
             [[0, 2], [0, 2, 2, 2, 0]],
             [[1, 0], [0, 0, 2, 2, 1]],
             [[2, 0], [1, 0, 0, 2, 1]]]
    pre = [[[1, 100], [1, 2, 3, 240, 239]],
           [[1, 100], [1, 2, 3, 240, 239]],
           [[89, 1], [1, 2, 3, 240, 239]],
           [[89, 1], [1, 2, 3, 240, 239]],
           [[1, 89], [238, 2, 3, 1, 239]],
           [[1, 89], [238, 238, 3, 1, 2]],
           [[89, 1], [3, 238, 237, 1, 2]],
           [[89, 1], [3, 238, 237, 1, 2]],
           [[1, 89], [3, 238, 237, 1, 2]],
           [[1, 89], [3, 238, 237, 1, 2]],
           [[89, 1], [3, 1, 237, 238, 2]],
           [[89, 1], [3, 1, 2, 238, 237]],
           [[1, 89], [238, 1, 2, 3, 237]],
           [[1, 89], [238, 1, 2, 3, 237]],
           [[89, 1], [238, 1, 2, 3, 237]],
           [[89, 1], [238, 1, 2, 3, 237]],
           [[1, 89], [238, 237, 2, 3, 1]],
           [[1, 89], [2, 237, 238, 3, 1]]
           ]
    waste=copy.deepcopy(pre)
    for i in range(len(waste)):
        for j in range(2):
            for K in range(m[j]):
                if pre[i][j][K]<=k*int(m[j]//2) or pre[i][j][K]>=o[j]-int(m[j]//2)+1:
                    waste[i][j][K]=0
    # print(np.array(waste))
    static = copy.deepcopy(waste)
    for i in range(1,len(static)-1):
        for j in range(2):
            for K in range(m[j]):
                if waste[i][j][K]>0 and waste[i-1][j][K]==0:
                    static[i][j][K] =1
                elif waste[i][j][K]>0 and waste[i-1][j][K]>0:
                    static[i][j][K] = static[i-1][j][K]+1
                elif waste[i][j][K] == 0 and waste[i - 1][j][K] > 0:
                    static[i][j][K] =0
    # print(np.array(static))
    cal_waste = copy.deepcopy(waste)
    QE=[0]
    for i in range(1,16):
        wb_1=[63,0,0]
        ws_1=[12.6667,0,0]
        Q = QE[-1]*i
        for j in range(2):
            for K in range(m[j]):
                if static[i][j][K]==0 and static[i+1][j][K]>0:
                    cal_waste[i][j][K]=max(2*(2-j)*(ε+η)+sum(ws_1[j:])+sum(wb_1[j+1:])-o[j],0)
                    Q += cal_waste[i][j][K]
                elif static[i][j][K]>0 and static[i+1][j][K]>0:
                    cal_waste[i][j][K]= max(static[i][j][K]*c+2*(2-j)*(ε+η)+sum(ws_1[j:])+sum(wb_1[j+1:])-o[j],0)
                    Q = Q-cal_waste[i-1][j][K]+cal_waste[i][j][K]
                elif static[i][j][K]>0 and static[i+1][j][K]==0:
                    cal_waste[i][j][K]= static[i][j][K]*c+ε+ws_1[j]-o[j]
                    Q = Q-cal_waste[i-1][j][K]+cal_waste[i][j][K]
        QE.append(Q/(i+1))
    return QE