#===================================================================
#-------------------------------------------------------------------
# Codigo de modelagem e inversao. O codigo main chama as funcoes de
# modelagem 'mdle_modeling.modeling_forward' e invesao 
# 'mdle_VFSA.inversio_VFSA'.  A ideia da gerar o dado observado T e
# tentar restituir por meio de inversao VFSA o modelo verdadeiro.
#-------------------------------------------------------------------
# AUTOR : RODRIGO SANTANA		DATA: 17/07/2018
#===================================================================
import mdle_modeling
import mdle_VFSA
import math
import matplotlib.pyplot as plt
import time
#===================================================================
#-------------------------------------------------------------------
### Inicio do codigo
ini = time.time()
Np 		= 3
Nzd 	= 25
P		= [0]*Np
P0 		= [500.]*Np 
v 		= 1500.
h 		= 600.
theta 	= (5*math.pi)/180
P[0] 	= v
P[1] 	= h
P[2] 	= theta
#-------------------------------------------------------------------
# Modelagem do dado observado 
x,T 	= mdle_modeling.modeling_forward(P,Nzd)
#-------------------------------------------------------------------
# Inversao por VFSA
Pinv=mdle_VFSA.inversio_VFSA(P,P0,T,Nzd,Np)
#-------------------------------------------------------------------
# Modelagem do dado calculado
xinv,Tinv 	= mdle_modeling.modeling_forward(Pinv,Nzd)
#-------------------------------------------------------------------
fim = time.time()
### Fim do codigo
#-------------------------------------------------------------------
#===================================================================
print ("Tempo de trabalho: %s" %(fim-ini))
print ("Verdadeiro %s -- Inverso %s" %(P,Pinv))
#-------------------------------------------------------------------
### Exportando o dado observado
arq = open("tempos.dat","w")
for i in range(0,Nzd):
	arq.write(str(x[i]))
	arq.write(',')	
	arq.write(str(T[i]))
	arq.write("\n")
arq.close()

#-------------------------------------------------------------------
# Plotando os resultados
plt.xlabel('Posicao do receptor em relacao a fonte (m)')
plt.ylabel('Tempos de transito (s)')
plt.grid(which='major', linestyle='-', linewidth='0.1', color='red')
plt.grid(which='minor', linestyle=':', linewidth='0.1', color='black')
plt.xlim(-600,600)
plt.ylim(0.93,0.78)
plt.plot(x, T, c='#FF0000', label='True date')
plt.plot(x, Tinv,".",c='#006400', label='Best date')
plt.legend()
#plt.plot(x, T, "y-")
plt.title('Tempos de transito') 
plt.show()

