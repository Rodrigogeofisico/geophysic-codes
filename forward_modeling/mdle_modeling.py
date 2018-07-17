import math

def modeling_forward(P,Nzd):
	T 	  = [0]*Nzd
	x 	  = [0]*Nzd
	v     = P[0] 
	h     = P[1]
	theta = P[2]
	a1	  = float(2*h*math.cos(theta))
	a2	  = float(2*h*math.sin(theta))
	for i in range(Nzd):
		x[i] = float(-600.0 + 50.0*(i))
		T[i] = float((math.sqrt((x[i] + a2)**2 + a1**2)) / v)
	return x,T