import mdle_modeling
import math
import matplotlib.pyplot as plt
Nzd = 25
P=[0]*3
print P
v=500.
h=600.
theta=(5*math.pi)/180
print theta
P[0] = v
P[1] = h
P[2] = theta
T = mdle_modeling.modeling_forward(P,Nzd)
arq = open("tempos.dat","w")
eixo_x = []
eixo_y = []
for i in xrange(0,Nzd):
	arq.write(str(25*(i+1)))
	arq.write(',')	
	arq.write(str(T[i]))
	arq.write("\n")
arq.close()
#print T


##################################
# Plotando os resultados
plt.xlabel('Posicao do receptor')
plt.ylabel('Tempos de transito')
plt.xlim(0,24)
plt.ylim(2.8,2.3)
plt.plot(T, c='#FFCC00')
plt.show()

