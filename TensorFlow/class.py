import numpy as np
import matplotlib.pyplot as plt

def f1(t):
    # return np.exp(-t)*np.cos(2*np.pi*t)
	return (0.8 * np.sin(t) + 0.1 * np.sin(4*t) + 0.1 * np.sin(8*t))

t = np.arange(0.0,50.0,0.05)

plt.figure(figsize=(8,7),dpi=98)

plt.plot(t,f1(t),"g-",label="p1")

plt.axis([0.0,25.01,-1.0,1.0])

plt.grid(True)
plt.legend()

plt.show()