import random
hyp=[]
ans=[]
for _ in range(10):
    candidate=[]
    while True:
        x = random.random()
        y = random.random()
        if 1-x-y<0:
            pass
        else:
            z=1-x-y
            candidate.append(x)
            candidate.append(y)
            candidate.append(z)
            break
    hyp.append(candidate)
print(hyp)
for i in range(10):
    ans.append(-40.5*hyp[i][0]+0.375*hyp[i][1]+44.9646*hyp[i][2])
print(ans)