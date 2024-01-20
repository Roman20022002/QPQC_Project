import numpy as np
import qiskit as qk

def theta_gate(qc,theta,i):
    assert len(theta) == 3, "theta incorrect size"
    qc.rx(theta[0],i)
    qc.ry(theta[1],i)
    qc.rz(theta[2],i)
    return 0

def add_Z_gates(qc, n, j,complicated_entangle):
    if n >2:
        if complicated_entangle:
            connects = []
            for k in range(j%(n-1)+1):
                connects+=range(k,n,j%(n-1)+1)
            for i in range(len(connects)-1):
                qc.cz(connects[i],connects[i+1])
            qc.cz(connects[-1],connects[0])
        else:
            if j%2==0:
                for i in range(n-1):
                    qc.cz(i,i+1)
                qc.cz(0,n-1)
            else:
                for i in range(n-1,0,-1):
                    qc.cz(i-1,i)
                qc.cz(0,n-1)
    elif n ==2:
        qc.cz(0,1)
    return 0


def W(qc,theta, n, l, complicated_entangle =False):
    Theta_matrix = np.reshape(theta, (n,l,3))
    for j in range(l):
        for i in range(n):
            theta_gate(qc,Theta_matrix[i,j,:],i)
        add_Z_gates(qc, n, j, complicated_entangle)
    return qc
