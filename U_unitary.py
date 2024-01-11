import qiskit as qk
import numpy as np
import itertools

#Create subset S with |S| <= 2:
def S(n):
    numbers = list(range(1,n+1))
    combinations = list(itertools.combinations(numbers,2))

    #Combine numbers and combinations into one list
    S = numbers+combinations

    return S

def phi_ij(xi,xj):
    return (np.pi-xi)*(np.pi-xj)

#Initialize quantum circuit with n qubits

def U_single(x,n,circuit):
    assert len(x) == n, "x must be of length n" 

    set = S(n)
    
    for i in set:
        if type(i) == int:
            theta = 2*i
            circuit.p(theta,i-1)
        else:
            theta = 2*phi_ij(x[i[0]-1],x[i[1]-1])
            circuit.cx(i[0]-1,i[1]-1)
            circuit.p(theta,i[1]-1)
            circuit.cx(i[0]-1,i[1]-1)

    return 0

def Hn(n,circuit):
    circuit.h(range(n))
    return 0

def U(qc,x,n,d):
    # qc = qk.QuantumCircuit(n,n)
    for i in range(d):
        Hn(n,qc)
        U_single(x,n,qc)
    return qc


