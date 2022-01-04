import copy
import numpy as np
import guitest2
import matplotlib.pyplot as plt
from matplotlib import rcParams
config={"font.family":'serif',"font.size":10.5,"font.serif":['SimSun']}
rcParams.update(config)
m = [1, 1]
a = [50, 54]
o = [100, 60]
d = [6, 2]
ε, η = 8, 4
c = 72
ans = 0  # 加工周期时间和
dans = 0  # 晶圆驻留时间和
QE = [0]  # 加工腔利用时间指数
pre = []  # 优先级
num = []  # 已经加工的晶圆数
k = 3
LL = dict()  # LL暂存晶圆
pre_cy = []  # 优先度集合
num_cy = []  # 晶圆数量集合
cyc = []  # 周期统计
Avg_ans2 = []  # 平均加工周期统计A2
Avg_dans = []  # 平均驻留时间延迟统计A1
Avg_dans2 = []  # 平均驻留时间延迟统计A2
H=[]  # 统计已完成加工的晶圆
h = 0  # 已完成加工晶圆数量
for i in m:  # 初始化
    q, p = [], []
    for j in range(i):
        q.append(j+1)
        p.append(1)
    pre.append(q)
    num.append(p)
pre_cy.append(pre)
num_cy.append(num)
while True:
    i = 0
    pre_cy.append(copy.deepcopy(pre_cy[-1]))
    num_cy.append(copy.deepcopy(num_cy[-1]))
    if num_cy[-1][0][0]==k*m[i] or (num_cy[-1][0][0]==0 and pre_cy[-1][0][0]!=pre_cy[-3][0][0]):
        wa = 0
    else:
        wa = 1
    while i < len(m):
        if num_cy[-1][i][0]==0 and wa==0 and i not in LL:
            wa=0
        elif num_cy[-1][i][0]<k*m[i]  and num_cy[-1][i][0]>0 and wa==1:
            num_cy[-1][i][0]+=1
            wa=1
            dans+=d[i]
        elif num_cy[-1][i][0]>0 and num_cy[-1][i][0]<k*m[i] and wa==0:
            q=num_cy[-1][i][0]+1
            num_cy[-1][i][0]=0
            pre_cy[-1][i][0]=a[i]
            wa=1
            dans+=d[i]
        elif num_cy[-1][i][0]==k*m[i] and wa==1:
            num_cy[-1][i][0]=0
            pre_cy[-1][i][0]=o[i]
            if i not in LL:
                LL[i]=1
            else:
                LL[i]+=1
            wa=1
            dans+=d[i]
        elif num_cy[-1][i][0]==k*m[i] and wa==0:
            num_cy[-1][i][0]=0
            pre_cy[-1][i][0]=o[i]
            wa=1
            dans+=d[i]
        elif num_cy[-1][i][0]==0 and pre_cy[-1][i][0]==pre_cy[-2-(o[i]//c)][i][0] and pre_cy[-1][i][0]==o[i] and wa==1:
            num_cy[-1][i][0]=1
            pre_cy[-1][i][0]=1
            wa=0
        elif pre_cy[-1][i][0]==a[i] and wa==1:
            num_cy[-1][i][0]=2
            pre_cy[-1][i][0]=1
            wa=0
        elif num_cy[-1][i][0]==0 and pre_cy[-1][i][0]==pre_cy[-2-(o[i]//c)][i][0] and pre_cy[-1][i][0]==o[i] and wa==0:
                if i in LL and LL[i]>0:
                    num_cy[-1][i][0]=1
                    pre_cy[-1][i][0]=1
                    LL[i]-=1
                wa=0
        if i == len(m)-1:
            if wa==1:
                h+=1
                H.append(h)
                Avg_dans2.append(dans/h)
            else:
                h=h
                H.append(h)
                Avg_dans2.append(dans/h)
        i+=1
    print("n: %s " % (num_cy[-1]))
    print("p: %s" % (pre_cy[-1]))
    if h == 16:
        break
    else:
        pass
print(H)
for i in range(len(H)):
    avg_ans2=c*(i+1)/H[i]
    Avg_ans2.append(avg_ans2)
print(Avg_ans2)
Avg_ans =[72 for i in range(len(H))]  # 平均加工周期统计A1
print(Avg_ans)
Avg_dans=[8 for i in range(len(H))]
print(Avg_dans2)

static_1=copy.deepcopy(pre_cy)  # 清洗还是非清洗
for i in range(len(static_1)):
    for j in range(2):
        for K in range(m[j]):
            if static_1[i][j][K] <= k*m[j]:
                static_1[i][j][K]=0
print(np.array(static_1))
static_2=copy.deepcopy(static_1)  # 空过的周期
for i in range(len(static_2)):
    for j in range(2):
        for K in range(m[j]):
            if static_1[i][j][K]>0 and static_1[i-1][j][K]==0:
                static_2[i][j][K]=1
            elif static_1[i][j][K]>0 and static_1[i-1][j][K]>0:
                static_2[i][j][K]=static_2[i-1][j][K]+1
print(np.array(static_2))
static_3=copy.deepcopy(static_2)
for i in range(len(static_3)-1):
    ws = [0, 0, 0]
    wb = [0, 0, 0]
    for j in range(2):
        for K in range(m[j]):
            if static_2[i][j][K]==0 and static_2[i+1][j][K]>0:
                if static_1[i+1][j][K]==a[j]:
                    static_3[i][j][K]=2*(2-j)*(ε+η)+sum(ws[j:])+sum(wb[j+1:])
                elif static_1[i+1][j][K]==o[j]:
                    static_3[i][j][K] = max(2 * (2 - j) * (ε + η) + sum(ws[j:]) + sum(wb[j + 1:])-o[j],0)
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]==0:
                if static_1[i][j][K]!=a[j]:
                    static_3[i][j][K] = static_2[i][j][K]*c+ε+ws[j]-o[j]
                elif static_1[i][j][K]==a[j]:
                    static_3[i][j][K] = static_2[i][j][K] * c + ε + ws[j]
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]>0:
                static_3[i][j][K]=max(static_2[i][j][K]*c+2 * (2 - j) * (ε + η) + sum(ws[j:]) + sum(wb[j + 1:])-o[j],0)
static_3[-1][0][0]=0
static_3[-1][1][0]=c+(ε + η)

print(np.array(static_3))
for i in range(1,len(static_3)-1):
    Q=QE[i-1]*(H[i]-1)
    for j in range(2):
        for K in range(m[j]):
            if static_2[i][j][K]==0 and static_2[i+1][j][K]>0:
                Q+=static_3[i][j][K]
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]>0:
                Q = Q-static_3[i-1][j][K]+static_3[i][j][K]
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]==0:
                Q = Q - static_3[i - 1][j][K] + static_3[i][j][K]
    QE.append(Q/H[i])
# QE.append((QE[-1]*H[-2]+sum(static_3[-1][1])-sum(static_3[-2][1]))/H[-1])
print(QE)
QE_1 = guitest2.A()
print(QE_1)
u=QE
u1=QE_1

x = [i+1 for i in range(len(H))]
x1 = [s+1 for s in range(16)]
y = Avg_ans
y1 = Avg_ans2
z = Avg_dans
z1 = Avg_dans2
plt.plot(x, u, label='满负荷装载策略晶圆平均浪费时间')
plt.plot(x1, u1[0:16], label='部分装载策略晶圆平均浪费时间', linestyle='--')
plt.legend()
plt.tick_params(labelsize=10.5)
plt.ylim(0, 100)
plt.xlim(0,26)
plt.margins(0)
plt.xlabel("加工周期")
plt.ylabel("晶圆平均浪费时间(s)")
# plt.title("晶圆平均加工时间对比")
ax=plt.gca()
ax.xaxis.set_major_locator(plt.MultipleLocator(2))
labels=ax.get_xticklabels()+ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.xlim(1,23)
plt.show()