# -*- coding: utf-8 -*-
import mdle_modeling
import numpy as npy
import random as rand
import math
import time
def inversio_VFSA(P,P0,D0,Nzd,Np):
	Ntemp 	= 	200
	Nmod 	= 	300
	y		= 	0.0
	c 		= 	0.17
	T0 		= 	550.0
	delt	=   0.0
	Pinv 	=	[0.0]*Np 
	P00 	=	[0.0]*Np 
	Pmin    =   [0.0]*Np
	Pmax    =   [0.0]*Np
	for l in range(0,Np):
		Pmin[l]    =  P[l]*0.2
		Pmax[l]    =  P[l]*2.3
		P00[l]	   =   P0[l]
		Pinv[l]    =   P0[l]
	Q0=Objetive(D0,P0,Nzd)
	arq1 = open("objetivo.dat","w")
	arq1.write(str(Q0))
	for j in range(1,Ntemp): # loop' das temperaturad
		Temp = T0*math.exp(-c*j)
		for k in range(1,Nmod): # Loop dos modelos
			for i in range(0,Np): #loop dos parametros dos modelos
				u= rand.random()
				sinal=npy.sign(u-0.5)
				y=sinal*Temp*((1. + (1./Temp))**(math.fabs(2.*u -1.)) -1.)
				piter= float(P0[i]) + y*(float(Pmax[i]) - float(Pmin[i]))
				# Evitando que os parametros saiam dos limites
				if( (piter < Pmin[i]) or (piter > Pmax[i])):
					if (piter < Pmin[i]):					
						piter = 2*Pmin[i] - piter
					elif(piter > Pmax[i]):
						piter = 2*Pmax[i] - piter								
					if( (piter < Pmin[i]) or (piter > Pmax[i])):
						piter = Pmin[i]	
				P00[i] = piter				
				Q=Objetive(D0,P00,Nzd)
				delt = Q - Q0
				if delt <= 0. :
					Pinv[i] = P00[i]
					P0[i]   = P00[i]
					Q0 	= Q
				else:
					prob = math.exp(-1*(delt/Temp))
					r=rand.random()
					if prob > r:
						Pinv[i] = P00[i]
						P0[i]   = P00[i]
						Q0   = Q
		arq1.write("\n")
		arq1.write(str(Q0))
	arq1.close()
	return Pinv


def Objetive(D0,P,Nzd):
	x,D=mdle_modeling.modeling_forward(P,Nzd)
	Q = 0.
	for i in range(0,Nzd):
		Q = float(Q + (float(D[i])-float(D0[i]))**2)	
	return Q
