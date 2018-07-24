import numpy as npy
import random as rand
import math
import time
import mdle_wave_modeling as mwm
import struct
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
ns      =   1
nx 		=   192
nz		=   46
dt		=	0.001
nt		=	1001
fpeak 	=	25.0
b       = 	4
pulso2=[0 for x in range(nx*nz)]

#----------------------------------------------------------
# Geração da fonte
pulso = mwm.source(nt,dt,fpeak)
# Exportando a fonte
arq = open("fonte2.bin","w+b")
for x in pulso:
	arq.write(struct.pack('=f',x))
arq.close()

#----------------------------------------------------------
# Leitura do campo de velocidades em binário
arq2 = open("modelos/inclusion.bin","rb")
pulso2=npy.fromfile(arq2,dtype=npy.float32).tolist()
arq2.close()
# Colocando o campo em uma matriz
t=0
w,h=nx,nz  ### nx numero de colunas, nz numero de linhas
c1=[[0 for x in range(w)] for y in range(h)]  ##c1[nz][nx]

for j in range(0,nx):
	for i in range(0,nz):
		c1[i][j]=pulso2[t]
		t=t+1

secvec=[0 for x in range(ns*nx*nt)]  
sect=mwm.extrapolation(b,c1,ns,nx,nz,nt,dt,fpeak)
arq3 = open("dado.bin","wb")
t=0
for i in range(nx*ns):
	for j in range(nt):
#		secvec[t] = sect[j][i]
		t=t+1
		arq3.write(struct.pack('=f',sect[j][i]))
arq.close()



# Testando o laplaceano
#w,h = nx,nz  
#u   = nt  
#b   = 2
#dx  = 5.
#dz  = 5.
#P   = [[0. for x in range(w)] for y in range(h)]
#lap = mwm.laplaceano(b,nx,nz,c1,dx,dz)

'''
#-------------------------------------------------------------------
# Plotando os resultados perfil 1D
plt.xlabel('Posicao do receptor em relacao a fonte (m)')
plt.ylabel('Tempos de transito (s)')
plt.grid(which='major', linestyle='-', linewidth='0.1', color='red')
plt.grid(which='minor', linestyle=':', linewidth='0.1', color='black')
#plt.xlim(-600,600)
#plt.ylim(0.93,0.78)
plt.plot(c, c='#FF0000', label='True date')
plt.legend()
#plt.plot(x, T, "y-")
plt.title('Tempos de transito') 
plt.show()
'''


'''
#-------------------------------------------------------------------
# Plotando os resultados gráfico 2D
#x,y,temp = np.loadtxt('data.txt').T #Transposed for easier unpacking
plt.figure(figsize=(6, 10))
plt.subplot(1, 1, 1)
imgplot=plt.imshow(sect,cmap=cm.gist_rainbow, interpolation="nearest")

imgplot=plt.imshow(sect,cmap=cm.gist_rainbow, interpolation="nearest")
plt.colorbar(orientation="horizontal", pad=0.1)
#print("shape ", npy.shape(c1), max(pulso2))
#imgplot.set_cmap('nipy_spectral')
#plt.imshow(c1)
#plt.plot(sect)

plt.show()

#plt.plot(pulso)
#plt.show(2)

'''