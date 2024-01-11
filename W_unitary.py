import numpy as np
import qiskit as qk

def theta_gate(qc,theta,i):
    assert len(theta) == 3, "theta incorrect size"
    qc.rx(theta[0],i)
    qc.ry(theta[1],i)
    qc.rz(theta[2],i)
    return 0

def add_Z_gates(qc, n, j):
    if n >2:
        connects = []
        for k in range(j%(n-1)+1):
            connects+=range(k,n,j%(n-1)+1)
        for i in range(len(connects)-1):
            qc.cz(connects[i],connects[i+1])
        qc.cz(connects[-1],connects[0])
    if n ==2:
        qc.cz(0,1)
    return 0


def W(qc,Theta, n, l):
    # qc = qk.QuantumCircuit(n)
    for j in range(l):
        for i in range(n):
            theta_gate(qc,Theta[i,j,:],i)
        add_Z_gates(qc, n, j)
    return qc

# ## Initialize
# n = 4
# d = 4

# ## Initial Theta, this is a vector of 3*n*d elements, here implemented as nxdx3 array.
# ## Theta is obtained frrom training with some minimisation method.
# Theta = np.round(np.random.rand(n,d,3),2)

# qc = W(Theta, n, d)
# qc.draw()