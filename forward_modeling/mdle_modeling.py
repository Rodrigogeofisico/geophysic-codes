def modeling_forward(P,Nzd):
	import math
	T = [0]*Nzd
	x = [0]*Nzd
	theta = P[2]
	h = P[1]
	v = P[0]
	a1=2*h*math.cos(theta)
	a2=2*h*math.sin(theta)
	for i in xrange(Nzd):
		x[i] = -600 + 50*(i-1)
	for i in xrange(Nzd):
		T[i]=(math.sqrt((x[i] + a2)**2 + a1**2)) / v
	return T