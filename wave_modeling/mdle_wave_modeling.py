import numpy as npy
import random as rand
import math
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import struct

##############################################################################
# Função que gerar o pulso sismico sendo este uma wavelet do tipo ricker. esse
# pulso é usado com fonta na modelagem.
#-----------------------------------------------------------------------------
# Autor: Rodrigo Santana
# Data : inicio /07/2018 fim  /07/2018 
# Última atualização /07/2018  BY: Rodrigo Santana
#-----------------------------------------------------------------------------
def source(nt,dt,fpeak):
	wpeak  	= 2.0*math.pi*fpeak
	waux	= 0.5*wpeak
	tdelay	= 6.0/(5.0*fpeak)
	pulso   =   [0.0]*nt
	for i in range(0,nt):
		t = i*dt
		tt	= t - tdelay
		pulso[i]= math.exp(-((waux**2)*(tt**2))/(4.0))*math.cos(wpeak*tt)
	return pulso
#============================================================================

##############################################################################
# Função que extrapola o campo de pressao. Isto eh, realiza a modelagem sismica
# sendo esta feita por meio do metodo de diferencas finitas. 
#-----------------------------------------------------------------------------
# Autor: Rodrigo Santana
# Data : inicio /07/2018 fim  /07/2018 
# Última atualização /07/2018  BY: Rodrigo Santana
#-----------------------------------------------------------------------------
def extrapolation(b,c,ns,nx1,nz1,nt,dt,fpeak):
	dsx = 1 # intervalo entre tiros
	sz  = 2 #  
	dx  = 5.
	dz  = 5.
	izr = 1
	nb	= 40
	nx = nx1+(2*nb)
	nz = nz1+(2*nb)
	sx0 = int(nx/2) # posicao do primeiro tiro
#	M[nz][nx]
#	M[Nlinhas][Ncolunas]
#   M[Posição da linha][Posição da coluna]
	pulso = source(nt,dt,fpeak)
	w,h = nx,nz  
	sect = [[0. for m in range(nx1*ns)] for n in range(nt)]
#	c2,tp =  extend_field(c,nx1,nz1,nb)

	c2,tp =  extend_field_version2(c,nx1,nz1,nb)

	arq4 = open("snap.bin","wb")
	secvec = [0. for m in range(nx*nz)]

	for j in range(ns):
		P_f = [[0. for m in range(w)] for n in range(h)]
		P_a = [[0. for m in range(w)] for n in range(h)]
		P_p = [[0. for m in range(w)] for n in range(h)]
		sx  = sx0 + (j*dsx) - 1
		for it in range(nt):
			lap = laplaceano(b,nx,nz,P_a,dx,dz)
			for x in range(nx):
				for y in range(nz):
					P_f[y][x] = 2*P_a[y][x] - P_p[y][x] + (((dt*c2[y][x])**2)*lap[y][x]) 

			P_f[sz+nb][sx] += pulso[it]
#			print('y=',sz+nb,'x=',sx)
#			time.sleep(0.5)
#			print(P_f[:][:])
#			print( '\n ')
#			print(30*'-', npy.shape(P_f))
#			print(max(P_f))
#			time.sleep(0.5)

			P_a = [[(P_a[y][x]*tp[y][x]) for x in range(w)] for y in range(h)]
			P_f = [[(P_f[y][x]*tp[y][x]) for x in range(w)] for y in range(h)]
			for k in range(nx1):
				sect[it][j*nx1 + k] = P_f[izr+nb][k+nb]

			for x in range(nx):
				for y in range(nz):
					P_p[y][x] = P_a[y][x] 
					P_a[y][x] = P_f[y][x] 

			if it%200 == 200:
				plt.subplot(221)  # plt.sbuplot(Ty,Tx,P) Tx=tamanho x (1 ou 2), Ty=tamnanho y (1 ou 2), P=posicao (1=TL,2=TR, 3=BL,4=BR),B=bottom, T=Top, R=Right e L=Left
				plt.imshow(c2, cmap=cm.gist_rainbow)
				plt.subplot(222)
				plt.imshow(tp, cmap=cm.gist_rainbow)
				plt.subplot(223)
				plt.imshow(lap, cmap=cm.gist_rainbow) #	plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
				plt.subplot(224)
				plt.imshow(P_f, cmap=cm.gist_rainbow)
				cax = plt.axes([0.12, 0.1, 0.8, 0.06]) # plt.axes(Px,Py,Tx,Ty)
				plt.colorbar(orientation="horizontal", pad=0.1, cax=cax)#	plt.figure(figsize=(8, 4))
#				plt.show() #print(max(sect))
#			if it%200 == 0:
			#	imgplot=plt.imshow(sect)
			#	plt.colorbar(orientation="horizontal", pad=0.1)
			#	plt.figure(figsize=(8, 4))
				plt.show()
#				print(max(sect))
			if it%50 == 0:
				print(npy.shape(secvec))
				tt=0			
				for ii in range(nx):
					for jj in range(nz):
#						secvec[tt] = P_f[jj][ii]
#						tt= tt+1
						arq4.write(struct.pack('=f',P_f[jj][ii]))
	arq4.close()
	return sect
#============================================================================


##############################################################################
# Função que calcula o laplaceano usado na modelagem.
#-----------------------------------------------------------------------------
# Autor: Rodrigo Santana
# Data : inicio /07/2018 fim  /07/2018 
# Última atualização /07/2018  BY: Rodrigo Santana
#-----------------------------------------------------------------------------
def laplaceano(b,nx,nz,P,dx,dz):
	w,h = nx, nz  
	lap = [[0. for x in range(w)] for y in range(h)]
	coef=calccoef(b)

	in_n = int(b/2) 
	lim_nx = nx-int(b/2)
	lim_nz = nz-int(b/2)

	for x in range(in_n,lim_nx):
		for y in range(in_n,lim_nz):
			pxx = 0.
			pzz = 0.
			for k in range(b+1):
				pxx +=  (coef[k]*P[y][x+k-in_n])
				pzz +=  (coef[k]*P[y+k-in_n][x])
			lap[y][x] = (pxx / (dx**2)) + (pzz / (dz**2))
	return lap
#============================================================================


def calccoef(a):
##############################################################################
# Funcao que gerar os coeficientes usados no operador laplaceano. a definicao
# do eh definidos com base na ordem do operador 'b'.
#-----------------------------------------------------------------------------
# Autor: Rodrigo Santana
# Data : inicio /07/2018 fim  /07/2018 
# Última atualização /07/2018  BY: Rodrigo Santana
#-----------------------------------------------------------------------------
	coef = [0. for x in range(a+1)]
	if(a == 2):
		coef[0] =  1.
		coef[1] = -2.
		coef[2] =  1.
	if(a == 4):
		coef[0] = -1./12.
		coef[1] =  4./3.
		coef[2] = -5./2.
		coef[3] =  4./3.
		coef[4] = -1./12.
	if(a == 6):
		coef[0] =    1./90.
		coef[1] =   -3./20.
		coef[2] =    3./2.
		coef[3] =  -49./18.
		coef[4] =    3./2.
		coef[5] =   -3./20.
		coef[6] =    1./90.
	if(a == 8):
		coef[0] =   -1./560.
		coef[1] =    8./315.
		coef[2] =   -1./5.
		coef[3] =    8./5.
		coef[4] = -205./72.
		coef[5] =    8./5.
		coef[6] =   -1./5.	
		coef[7] =    8./315.
		coef[8] =   -1./560.
	return coef
#============================================================================


##############################################################################
# Função que gerar um campo de velocidades ampliado. Ele é usado na modelagem
# Com tratamento de borda. Gera também a borda atenuante.
#-----------------------------------------------------------------------------
# Autor: Rodrigo Santana
# Data : inicio /07/2018 fim  /07/2018 
# Última atualização /07/2018  BY: Rodrigo Santana
#-----------------------------------------------------------------------------
def extend_field(c,nx,nz,nb):
	c_s = [[1. for x in range((2*nb)+nx)] for y in range((2*nb)+nz)]
	tp = [[1. for x in range((2*nb)+nx)] for y in range((2*nb)+nz)]
	taper = [1. for x in range(nb)]
	cc = -0.015**2
#-----------------------------
	for x in range(nx):
		for y in range(nz):
	 		c_s[nb+y][nb+x]=c[y][x] 
	# Area 1
#-----------------------------
	for x in range(nx):
		for y in range(nb):
	 		c_s[y][x+nb]=c[0][x] 
	 		tp[y][x+nb]=math.exp(cc*(nb-y)**2) 
	# Area 2
#-----------------------------
	for x in range(nx):
		for y in range(nb):
	 		c_s[nz+nb+y][x+nb]=c[nz-1][x] 
	 		tp[nz+nb+y][x+nb]=math.exp(cc*(y)**2) 
	# Area 3
#-----------------------------
	for x in range(nb):
		for y in range(nz):
	 		c_s[nb+y][x]=c[y][0]
	 		tp[nb+y][x]=math.exp(cc*(nb-x)**2) 

	# Area 4
#-----------------------------
	for x in range(nb):
		for y in range(nz):
	 		c_s[nb+y][nb+nx+x]=c[y][nx-1]
	 		tp[nb+y][nb+nx+x]=math.exp(cc*(x)**2) 
	# Area 5
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y][x]=c[0][0] 
	 		d = ((nb-y)**2 + (nb-x)**2)
	 		tp[y][x] = math.exp(cc*d) 
#	 		tp[y][x] = math.exp(cc*(nb-x)**2) 
	# Area 6
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y][nb+nx+x]=c[0][nx-1] 
	 		d = ((nb-y)**2 + (x)**2)
	 		tp[y][nb+nx+x] = math.exp(cc*d)
	# Area 7
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y+nb+nz][nb+nx+x]=c[nz-1][nx-1] 
	 		d = (y**2 + x**2)
	 		tp[y+nb+nz][nb+nx+x] = math.exp(cc*d)
	# Area 8
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y+nb+nz][x]=c[nz-1][0]
	 		d = (y**2 + (nb-x)**2)
	 		tp[y+nb+nz][x] = math.exp(cc*d)	 		 
	 		taper[y] = math.exp(cc*d)	 
	# Area 9
#-----------------------------
#	imgplot=plt.imshow(tp,cmap=cm.gist_rainbow, interpolation="nearest")
#	imgplot.set_cmap('nipy_spectral')
#	plt.plot(taper)
#	plt.show()
	return c_s,tp 
#	-----------------------------
#	!		!			!		!
#	!	6	!	  2		!	7	!
#	!		!			!		!
#	-----------------------------
#	!		!			!		!
#	!	4	!	  1		!	5	!
#	!		!	  		!		!
#	!		!			!		!
#	-----------------------------
#	!		!			!		!
#	!	9	!	  3		!	8	!
#	!		!			!		!
#	-----------------------------
#============================================================================


##############################################################################
# Função que gerar um campo de velocidades ampliado. Ele é usado na modelagem
# Com tratamento de borda. Gera também a borda atenuante.
#-----------------------------------------------------------------------------
# Autor: Rodrigo Santana
# Data : inicio /07/2018 fim  /07/2018 
# Última atualização /07/2018  BY: Rodrigo Santana
#-----------------------------------------------------------------------------
def extend_field_version2(c,nx,nz,nb):
	c_s = [[1. for x in range((2*nb)+nx)] for y in range((2*nb)+nz)]
	tp = [[1. for x in range((2*nb)+nx)] for y in range((2*nb)+nz)]
	taper = [1. for x in range(nb)]
	cc = -0.015**2
#-----------------------------
	for x in range(nx):
		for y in range(nz):
	 		c_s[nb+y][nb+x]=c[y][x] 
	# Area 1
#-----------------------------
	for x in range(nx):
		for y in range(nb):
	 		c_s[y][x+nb]=c[0][x] 
	 		tp[y][x+nb]=math.exp(cc*(nb-y)**2) 
	# Area 2
#-----------------------------
	for x in range(nx):
		for y in range(nb):
	 		c_s[nz+nb+y][x+nb]=c[nz-1][x] 
	 		tp[nz+nb+y][x+nb]=math.exp(cc*(y)**2) 
	# Area 3
#-----------------------------
	for x in range(nb):
		for y in range(nz):
	 		c_s[nb+y][x]=c[y][0]
	 		tp[nb+y][x]=math.exp(cc*(nb-x)**2) 

	# Area 4
#-----------------------------
	for x in range(nb):
		for y in range(nz):
	 		c_s[nb+y][nb+nx+x]=c[y][nx-1]
	 		tp[nb+y][nb+nx+x]=math.exp(cc*(x)**2) 
	# Area 5
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y][x]=c[0][0] 
	 		d = ((nb-y)**2 + (nb-x)**2)
	 		tp[y][x] = tp[y][nb]
	# Area 6
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y][nb+nx+x]=c[0][nx-1] 
#	 		d = ((nb-y)**2 + (x)**2)
	 		tp[y][nb+nx+x] = tp[y][nx+nb-1]
	 		tp[y][nb+nx+x] = tp[y][nb+nx+x] *tp[nb+y][nb+nx+x]
	# Area 7
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y+nb+nz][nb+nx+x]=c[nz-1][nx-1] 
	 		d = (y**2 + x**2)
	 		tp[y+nb+nz][nb+nx+x] =  tp[nz+nb+y][nb+nx-1] 	
	# Area 8
#-----------------------------
	for x in range(nb):
		for y in range(nb):
	 		c_s[y+nb+nz][x]=c[nz-1][0]
	 		d = (y**2 + (nb-x)**2)
	 		tp[y+nb+nz][x] = tp[nz+nb+y][nb] 		 
	# Area 9
#-----------------------------
	imgplot=plt.imshow(tp ,cmap=cm.gist_rainbow, interpolation="nearest")
	imgplot.set_cmap('nipy_spectral')
#	plt.plot(taper)
	plt.show()
	return c_s,tp 
#============================================================================