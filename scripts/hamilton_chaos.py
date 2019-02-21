#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 15:43:00 2018

@author: ert
"""

import numpy as np
import matplotlib.pyplot as plt

N = 500000

om1 = 4*np.random.rand(N)
om2 = 4*np.random.rand(N)

condi = np.ones(N, dtype=bool)

kmax = 30

gam = 0.5
tau = 1.0

for k1 in range(1,kmax+1):
    for k2 in range(-kmax-1,0):
        condi[abs(k1*om1 + k2*om2) < gam/(abs(k1)+abs(k2))**tau] = False

plt.plot(om1[condi], om2[condi], ',')
plt.axis('equal')
plt.grid(True)