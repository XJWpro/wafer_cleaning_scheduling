import gurobipy as gb
from gurobipy import *
import time

a = [50,54]
m = [1,1]
dmax = 40
ε = 8
η = 4
n = len(a)  # processing steps number

start = time.process_time()
model = gb.Model('cluster_tool_with_cleaning')  # building the model

w_b = model.addVars(n, lb=0.0, vtype=GRB.CONTINUOUS, name="w_b")  # waiting before unloading
w_s = model.addVars(n, lb=0.0, vtype=GRB.CONTINUOUS, name="w_s")  # waiting after swap
d = model.addVars(n, lb=0.0, vtype=GRB.CONTINUOUS, name="d")  # wafer delay time
C = model.addVar(vtype=GRB.CONTINUOUS, obj=1.0, name="C")  # cycle time

model.addConstr((2*(n+1)*(ε+η)+sum(w_b[i] for i in range(n))+sum(w_s[i] for i in range(n)))-C == 0)
for i in range(n):
    model.addConstr(2*η+ε+w_s[i]+a[i]+d[i] == m[i]*C)
    model.addConstr(d[i] <= 40)
obj = C+sum(d[i] for i in range(n))
model.setObjective(obj, GRB.MINIMIZE)
model.optimize()

print(str(C))
print("cycle time add total wafer delay time:"+str(model.objval))
tab = ''
for i in range(n):
    print('w_b' + str(i) + ':' + tab + str(w_b[i]))
    print('w_s' + str(i) + ':' + tab + str(w_s[i]))
    print('d' + str(i) + ':' + tab + str(d[i]))
end = time.process_time()
print('Running time: % seconds' % (end - start))