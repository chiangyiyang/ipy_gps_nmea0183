import numpy as np
import matplotlib.pyplot as plt
from time import sleep

x = np.arange(0, 5, 0.1)
y = np.sin(x)
plt.plot(x, y)
plt.show()
# sleep(5)