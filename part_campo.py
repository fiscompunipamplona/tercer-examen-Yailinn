#Modelar, usando la librería vpython, la trayectoria en 3d que realiza una partícula cargada, que parte del reposo, y que se propaga en un 
#campo magnético de magnitud 1.0 orientado en dirección z. La partícula tiene masa 1.0, y condiciones iniciales: vx = 10.0, vy = 6.0, 
#vz = 2.0. nterprete y analice físicamente.

from numpy import array, linspace
from math import sin, cos, pi
from pylab import plot, xlabel, ylabel, show
from scipy.integrate import odeint

from vpython import sphere, scene, vector, color, arrow, text, sleep

arrow_size = 3.0

arrow_x = arrow(pos=vector(0,0,0), axis=vector(arrow_size,0,0), color=color.red)
arrow_y = arrow(pos=vector(0,0,0), axis=vector(0,arrow_size,0), color=color.green)
arrow_z = arrow(pos=vector(0,0,0), axis=vector(0,0,arrow_size))

R =0.5  #Radio de la esfera

def func (conds, t, q, m, B,t0): #Función que devuelve valores de theta y omega(arreglo)
    dvx=(q*B)/m*conds[1]
    dvy=(-q*B)/m*conds[0]
    dvz=0*conds[2]
    return array([dvx,dvy,dvz], float)


q=2.0
B=1.0
m=1.0

vx=10.0
vy=6.0
vz=2.0

to=0.1

initcond = array([vx,vy,vz], float) #Arreglo de condiciones iniciales

n_steps = 1000 #Número de pasos
t_start = 0.   #Tiempo inicial
t_final = 15.  #Tiempo final
t_delta = (t_final - t_start) / n_steps #Diferencial de tiempo (Paso temporal)
t = linspace(t_start, t_final, n_steps) #Arreglo de diferencial de tiempo

solu, outodeint = odeint( func, initcond, t, args = (q,m,B,to), full_output=True) #Solución de la ecuación diferencial(Parámetros acordes a los definidos en la función) 
#solu (Matriz de n filas y 2 columnas) es la solución diferencial para cada paso(columnas) de theta y omega

vvx,vvy,vvz=solu.T
#theta, omega = solu.T #Devuelve la matriz transpuesta (a cada una de las variables de la izquierda, theta y omega, le define el respectivo vector)

# =====================

scene.range = 8 #Tamaño de la ventana de fondo

xp=(m/q*B)*(vx*sin(q*B*to/m)+vy*(1-cos(q*B*to/m)))
yp=(m/q*B)*(vx*(cos(q*B*to/m)-1)+vy*sin(q*B*to/m))
zp = (2*pi*m*vz*cos(q*vz*to/m))/q*B

sleeptime = 0.0001 #Tiempo con que se actualiza la posición de la partícula

prtcl = sphere(pos=vector(xp,yp,zp), radius=R, color=color.cyan) #Define objeto con que se va a trabajar

time_i = 0 #Contador que se mueve en el espacio temporal en el que se resolvió la ecuación diferencial
t_run = 0  #Tiempo en el que se ejecuta la animación

#for i in omega:
#    print(i)


while t_run < t_final: #ANIMACIÓN
    prtcl.pos = vector( (m/q*B)*(vvx[time_i])*sin(q*B*to/m)-(vvy[time_i])*cos(q*B*to/m), (m/q*B)*(vvx[time_i])*(cos(q*B*to/m)-1)+(vvy[time_i])*sin(q*B*to/m), (2*pi*m*(vvz[time_i])*cos(q*(vvz[time_i])*to/m))/q*B )
    
    t_run += t_delta
    sleep(sleeptime)
    time_i += 1
