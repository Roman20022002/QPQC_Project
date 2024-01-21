import qiskit as qk
import numpy as np

def theta_gate(qc,theta,i):
    assert len(theta) == 3, "theta incorrect size"
    qc.rx(theta[0],i)
    qc.ry(theta[1],i)
    qc.rz(theta[2],i)
    return 0


def split_Z_gates(qc, n, j, indices,dag):
    phi = (-1)**dag*(np.pi/2)
    B = 2 in indices
    # if j%2 ==0:
    qc.cz(0,1)
    qc.p(phi ,1-B)
    # else:
    #     qc.p(phi ,1-B)
    #     qc.cz(0,1)
    return qc
    
def split_Z_gates_alt(qc, n, j, dag):
    phi = (-1)**dag*(np.pi/2)
    # if j%2 ==0:
    qc.cz(0,1)
    qc.p(phi ,1)
    qc.p(phi ,2)
    qc.cz(2,3)
    # else:
    #     qc.cz(2,3)
    #     qc.p(phi ,2)
    #     qc.p(np.pi/2 ,1)
    #     qc.cz(0,1)
    return qc           

def W_4_split(qc,theta, n, l, indices,dag):
    # Gets 2 qubit circuit, then adds W gate
    Theta_matrix = np.reshape(theta, (n,l,3))[indices,:,:]
    for j in range(l):
        for i in range(2):
            theta_gate(qc,Theta_matrix[i,j,:],i)
        split_Z_gates(qc, n, j, indices,dag[j])        
    return qc

def W_4_split_alt(qc,theta, n, l,dag):
    # Gets 4 qubit circuit, then adds W gate
    Theta_matrix = np.reshape(theta, (n,l,3))
    for j in range(l):
        for i in range(n):
            theta_gate(qc,Theta_matrix[i,j,:],i)
        split_Z_gates_alt(qc, n, j, dag[j])        
    return qc

def make_dags(i,splits):
    dags = np.zeros(splits)
    j=0
    for e in bin(i)[2:].zfill(splits):
        dags[j] = e
        j+=1
    return dags