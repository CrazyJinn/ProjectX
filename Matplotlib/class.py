import numpy as np
import matplotlib.pyplot as plt

def f1(t):
	# return (0.8 * np.sin(t) + 0.1 * np.sin(4*t) + 0.1 * np.sin(8*t))
    return np.sin(t)

t = np.arange(0.0,50.0,0.1)

plt.figure(figsize=(8,7),dpi=98)

plt.plot(t,f1(t),"g-",label="p1")

plt.axis([0.0,25.01,-1.0,1.0])

plt.grid(True)
plt.legend()

plt.show()