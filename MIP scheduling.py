import gurobipy as gb
from gurobipy import *
import time

a = list(map(float, input('processing time:').split()))
m = list(map(float, input('PM numbers for each step:').split()))
dmax = float(input('the maximum wafer delay time:'))
ε = float(input('the robot move time:'))
η = float(input('the robot load time:'))
o = list(map(float, input('PM cleaning time:').split()))
n = len(a)  # processing steps number
inf = 1e-6
k = float(input('cleaning period:'))

start = time.process_time()
model = gb.Model('cluster_tool_with_cleaning')  # building the model

w_b = model.addVars(n, lb=0.0, vtype=GRB.CONTINUOUS, name="w_b")  # waiting before unloading
w_s = model.addVars(n, lb=0.0, vtype=GRB.CONTINUOUS, name="w_s")  # waiting after swap
z = model.addVars(n, lb=0, vtype=GRB.INTEGER, name="z")  # blank PM
d = model.addVars(n, lb=0.0, vtype=GRB.CONTINUOUS, name="d")  # wafer delay time
C = model.addVar(vtype=GRB.CONTINUOUS, obj=1.0, name="C")  # cycle time
u = model.addVars(n, vtype=GRB.BINARY, name="u")  # decision variables for z
q = model.addVars(n, vtype=GRB.CONTINUOUS, name="q")

model.addConstr((2*(n+1)*(ε+η)+sum(w_b[i] for i in range(n))+sum(w_s[i] for i in range(n)))-C == 0)
for i in range(n):
    model.addConstr(2*η+ε+w_s[i]+a[i]+d[i] == (m[i]-z[i])*C)
    model.addConstr(d[i] <= 30)
    model.addConstr(z[i]>= m[i]//2-(m[i]//2)*u[i])
    model.addConstr(z[i]<= (m[i]//2)-inf*u[i])
    model.addConstr(z[i]*C == q[i])
    model.addConstr((ε+w_s[i]+q[i])*u[i]+(ε+w_s[i]+k*z[i]+1)*(1-u[i]) >= o[i])

obj = C+sum(d[i] for i in range(n))
model.setObjective(obj, GRB.MINIMIZE)
model.write("paper.lp")
model.params.NonConvex = 2
model.optimize()

print("cycle time add total wafer delay time:"+str(model.objval))
tab = ''
for i in range(n):
    print('w_b' + str(i) + ':' + tab + str(w_b[i]))
    print('w_s' + str(i) + ':' + tab + str(w_s[i]))
    print('z' + str(i) + ':' + tab + str(z[i]))
    print('u' + str(i) + ':' + tab + str(u[i]))
    print('d' + str(i) + ':' + tab + str(d[i]))
end = time.process_time()
print('Running time: % seconds' %(end-start))