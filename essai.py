%matplotlib inline
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15,10))
ax = plt.axes(projection="3d")

def z_function(x, y):
    return np.where(x<0,np.sin(x),(np.sin(np.sqrt(X**2+(Y-8)**2))+np.sin(np.sqrt(X**2+(Y+8)**2)))/2)

x = np.linspace(-40, 40, 400)
y = np.linspace(-40, 40, 400)

X, Y = np.meshgrid(x, y)
Z = z_function(X, Y)
#ax.plot_wireframe(X, Y, Z, color='green')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_zlim(-2, 2)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='winter', edgecolor='none')
plt.show()
