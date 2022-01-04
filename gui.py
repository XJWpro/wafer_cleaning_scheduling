import copy
import numpy as np
import guitest
import matplotlib.pyplot as plt
from matplotlib import rcParams
config={"font.family":'serif',"font.size":10.5,"font.serif":['SimSun']}
rcParams.update(config)
m = [1, 1, 2]
a = [80, 120, 240]
o = [90, 60, 80]
d = [0, 0, 0]
ε, η = 5, 3
c = 131
ans = 0  # 加工周期时间和
dans = 0  # 晶圆驻留时间和
QE = [0]  # 加工腔利用时间指数
pre = []  # 优先级
num = []  # 已经加工的晶圆数
k = 2
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
    if num_cy[-1][i][0]==k:
        wa = 0
    else:
        wa = 1
    while i < len(m):
        if max(pre_cy[-1][i])<k*m[i] and 0 not in num_cy[-1][i] and wa==1:  # 对应pre[1,2] num[1,1]机械手携带晶圆这种类型
            j=pre_cy[-1][i].index(min(pre_cy[-1][i]))
            num_cy[-1][i][j]+=1
            pre_cy[-1][i][j]+=m[i]
            wa=1
        elif max(pre_cy[-1][i])<k*m[i] and 0 not in num_cy[-1][i] and wa==0:  # 对应pre[1,2] num[1,1]机械手不携带晶圆这种类型
            j=pre_cy[-1][i].index(min(pre_cy[-1][i]))
            num_cy[-1][i][j]=0
            pre_cy[-1][i][j]=a[i]
            wa = 1
        elif min(num_cy[-1][i])==k and wa==1:  # 对应pre[3,4] num[2,2]机械手携带晶圆这种类型
            j=pre_cy[-1][i].index(min(pre_cy[-1][i]))
            num_cy[-1][i][j]=0
            pre_cy[-1][i][j]=o[i]
            if i not in LL:
                LL[i] = 1
            else:
                LL[i] += 1
            wa = 1
        elif min(num_cy[-1][i]) == k and wa == 0:  # 对应pre[3,4] num[2,2]机械手不携带晶圆这种类型
            j=pre_cy[-1][i].index(min(pre_cy[-1][i]))
            num_cy[-1][i][j]=0
            pre_cy[-1][i][j]=o[i]
            wa = 1
        elif min(pre_cy[-1][i])>k * m[i] and max(num_cy[-1][i])==0 and wa==1: # 对应pre[90] num[0]机械手携带晶圆这种类型
            j=num_cy[-1][i].index(max(num_cy[-1][i]))
            num_cy[-1][i][j]=1
            pre_cy[-1][i][j]=1
            wa = 0
        elif min(pre_cy[-1][i])>k * m[i] and max(num_cy[-1][i])==0 and wa==0:  # 对应pre[90] num[0]机械手不携带晶圆这种类型
            if LL[i]>0:
                j = num_cy[-1][i].index(max(num_cy[-1][i]))
                num_cy[-1][i][j] = 1
                pre_cy[-1][i][j] = 1
                wa = 0
                LL[i]-=1
            else:
                wa = 0
        elif wa == 1 and 0 in num_cy[-1][i] and max(num_cy[-1][i]) <= k:
            j = num_cy[-1][i].index(max(num_cy[-1][i]))
            if num_cy[-1][i][j] == num_cy[-3][i][j] and max(num_cy[-1][i])<k:
                num_cy[-1][i][j]+=1
                pre_cy[-1][i][j]+=2
                wa=1
            elif num_cy[-1][i][j] == num_cy[-3][i][j] and max(num_cy[-1][i])==k:
                q = pre_cy[-1][i].index(max(pre_cy[-1][i]))
                num_cy[-1][i][j]=0
                num_cy[-1][i][q]=1
                pre_cy[-1][i][j]=o[i]
                pre_cy[-1][i][q]=1
                wa=1
            elif num_cy[-1][i][j] != num_cy[-3][i][j]:
                q = pre_cy[-1][i].index(max(pre_cy[-1][i]))
                num_cy[-1][i][q]=num_cy[-1][i][j]
                pre_cy[-1][i][q]=min(pre_cy[-1][i])+1
                wa=0
        if i == len(m)-1:
            if wa==1:
                h+=1
                H.append(h)
            else:
                h=h
                H.append(h)
        i+=1
    print(num_cy[-1])
    if h==16:
        break
    else:
        pass
print(H)
for i in range(len(H)):
    avg_ans2=c*(i+1)/H[i]
    Avg_ans2.append(avg_ans2)
print(Avg_ans2)
Avg_ans =[131 for i in range(len(H))]  # 平均加工周期统计A1
print(Avg_ans)
Avg_dans=[0 for i in range(len(H))]
Avg_dans2=[0 for i in range(len(H))]

static_1=copy.deepcopy(pre_cy)  # 清洗还是非清洗
for i in range(len(static_1)):
    for j in range(3):
        for K in range(m[j]):
            if static_1[i][j][K] <= k*m[j]+1:
                static_1[i][j][K]=0
# print(np.array(static_1))
static_2=copy.deepcopy(static_1)  # 空过的周期
for i in range(len(static_2)):
    for j in range(3):
        for K in range(m[j]):
            if static_1[i][j][K]>0 and static_1[i-1][j][K]==0:
                static_2[i][j][K]=1
            elif static_1[i][j][K]>0 and static_1[i-1][j][K]>0:
                static_2[i][j][K]=static_2[i-1][j][K]+1
# print(np.array(static_2))
static_3=copy.deepcopy(static_2)
for i in range(len(static_3)-1):
    ws = [40, 0, 11, 0]
    wb = [16, 0, 0, 0]
    a = [80, 120, 240]
    o = [90, 60, 80]
    for j in range(3):
        for K in range(m[j]):
            if static_2[i][j][K]==0 and static_2[i+1][j][K]>0:
                if static_1[i+1][j][K]==a[j]:
                    static_3[i][j][K]=2*(3-j)*(ε+η)+sum(ws[j:])+sum(wb[j+1:])
                elif static_1[i+1][j][K]==o[j]:
                    static_3[i][j][K] = max(2 * (3 - j) * (ε + η) + sum(ws[j:]) + sum(wb[j + 1:])-o[j],0)
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]==0:
                if static_1[i][j][K]==o[j]:
                    static_3[i][j][K] = static_2[i][j][K]*c+ε+ws[j]-o[j]
                elif static_1[i][j][K]==a[j]:
                    static_3[i][j][K] = static_2[i][j][K] * c + ε + ws[j]
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]>0:
                static_3[i][j][K]=static_2[i][j][K]*c+2 * (3 - j) * (ε + η) + sum(ws[j:]) + sum(wb[j + 1:])
static_3[-1][2][0]=c+ε+ws[2]-o[2]
for i in range(1,len(static_3)-1):
    Q=QE[i-1]*(H[i]-1)
    for j in range(3):
        for K in range(m[j]):
            if static_2[i][j][K]==0 and static_2[i+1][j][K]>0:
                Q+=static_3[i][j][K]
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]>0:
                Q = Q-static_3[i-1][j][K]+static_3[i][j][K]
            elif static_2[i][j][K]>0 and static_2[i+1][j][K]==0:
                Q = Q - static_3[i - 1][j][K] + static_3[i][j][K]
    QE.append(Q/H[i])
QE.append((QE[-1]*H[-2]+67)/H[-1])
print(QE)
QE_1 = guitest.A()
print(QE_1)
u=QE[:-1]
u1=QE_1

x = [i+1 for i in range(len(static_3)-1)]
x1 = [s+1 for s in range(16)]
y = Avg_ans
y1 = Avg_ans2
z = Avg_dans
z1 = Avg_dans2
# plt.figure(figsize=(10,5))
# # ax1 = plt.subplot(2,1,1)
# # ax2 = plt.subplot(2,1,2)
# # plt.sca(ax1)
# # plt.tick_params(labelsize=10.5)
# # plt.plot(x, y, label='部分装载策略晶圆平均加工时间')
# # plt.plot(x, y1, label='满负荷装载策略晶圆平均加工时间')
# # plt.legend()
# # plt.ylim(55, 200)
# # plt.margins(0)
# # plt.xlabel("加工周期")
# # plt.ylabel("晶圆平均加工时间(s)")
# # plt.title("晶圆平均加工时间对比", y=-0.5)
# # plt.tight_layout()
# # plt.sca(ax2)
# # plt.tick_params(labelsize=10.5)
# # plt.plot(x, z, label='部分装载策略晶圆平均驻留时间延迟')
# # plt.plot(x, z1, label='满负荷装载策略晶圆平均驻留时间延迟')
# # plt.legend()
# # plt.ylim(-5, 5)
# # plt.margins(0)
# # plt.xlabel("加工周期")
# # plt.ylabel("晶圆平均驻留时间延迟(s)")
# # plt.title("晶圆平均驻留时间延迟对比", y=-0.5)
# # plt.tight_layout(pad=1, h_pad=1)
plt.plot(x, u, label='满负荷装载策略晶圆平均浪费时间')
plt.plot(x1, u1[0:16], label='部分装载策略晶圆平均浪费时间')
plt.legend()
plt.tick_params(labelsize=10.5)
plt.ylim(0, 500)
plt.margins(0)
plt.xlabel("加工周期")
plt.ylabel("晶圆平均驻留时间延迟(s)")
# plt.title("晶圆平均加工时间对比")
ax=plt.gca()
ax.xaxis.set_major_locator(plt.MultipleLocator(2))
labels=ax.get_xticklabels()+ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.xlim(1,23)
plt.show()
