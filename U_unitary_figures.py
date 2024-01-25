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
            theta = 2*x[i-1]
            label = 'P(2$\Phi_{%s}$)'%i
            circuit.x(i-1,label=label)
        else:
            if abs(i[0]-i[1])>1:
                continue
            else:
                theta = 2*phi_ij(x[i[0]-1],x[i[1]-1])
                circuit.cx(i[0]-1,i[1]-1)
                label = 'P(2$\Phi_{%s,%s}$)'%(i[0],i[1])
                circuit.x(i[1]-1,label=label)
                circuit.cx(i[0]-1,i[1]-1)

    return 0

def Hn(n,circuit):
    circuit.h(range(n))
    return 0

def U(qc,x,n,d):
    for i in range(d):
        Hn(n,qc)
        qc.barrier()
        U_single(x,n,qc)
        qc.barrier()
    return qc


