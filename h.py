#Import necessary libraries
import qiskit as qk
from U_unitary import * 
from W_unitary import *
from qiskit import Aer

#build circuit
def circuit(x,theta,n,d):

    circuit = qk.QuantumCircuit(n,n)
    circuit = U(circuit,x,n,d)
    circuit = W(circuit,theta,n,d)
    
    #Add measurement to circuit
    circuit.measure(range(n),range(n))

    return circuit

'''
Define function h that returns +- 1 depending on the expectation value of Z^n

x: data 
theta: optimization parameter
n: number of qubits
d: depth of circuit
shots: number of repititions for experiment in order to determine expectation value
'''
def h(x,theta,n,d,shots):
    #run circuit
    simulator = Aer.get_backend('aer_simulator',shots=shots)
    job = circuit(x,theta,n,d)
    result = simulator.run(job).result()

    #Get counts and normalize them
    counts = result.get_counts()
    total_counts = sum(counts.values())
    counts_normalized = {state: counts[state]/total_counts for state in counts}

    #Get keys of dictionary
    keys = list(counts_normalized.keys())

    #Calculate expectation value of Z^n 
    expectation_value = 0
    for i in range(len(keys)):
        tmp = keys[i]

        #Extract number of zeros and ones
        num_zeros = tmp.count('0')
        num_ones = tmp.count('1')

        #Determine eigenvalue of operator
        eigenvalue = 1**num_zeros * (-1)**num_ones
        
        #Add to expectation value
        expectation_value += eigenvalue * counts_normalized.get(tmp)

    #Determine h
    if expectation_value >= 0:
        h = 1
    else:
        h = -1

    return h