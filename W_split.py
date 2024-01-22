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


def apply_W_top_before_split(qc,theta, n, n_part, l=1):
    # Corresponds to U_top
    Theta_matrix = np.reshape(theta, (n,l,3))[0:2,:,:]
    for j in range(l):
        for i in range(n_part):
            theta_gate(qc,Theta_matrix[i,j,:],i)
    qc.cz(0,1)        
    return qc

def apply_W_bottom_after_split(qc):
    # Corresponds to V_top
    return qc

def apply_W_bottom_before_split(qc,theta, n, n_part, l=1):
    # Corresponds to U_bot
    Theta_matrix = np.reshape(theta, (n,l,3))[2:4,:,:]
    for j in range(l):
        for i in range(n_part):
            theta_gate(qc,Theta_matrix[i,j,:],i)
    return qc

def apply_W_bottom_after_split(qc):
    # Corresponds to V_bot
    qc.cz(0,1)   
    return qc

def apply_u_gate(qc,dag,index_u):
    phi = (-1)**dag*(np.pi/2)
    qc.p(phi ,index_u)
    return qc

def top_circuit(theta, n, n_part,dag):
    circuit = qk.QuantumCircuit(n_part,n_part)

    circuit = apply_W_top_before_split(circuit,theta, n, n_part)
    circuit = apply_u_gate(circuit,dag,1)
    # circuit = apply_W_top_after_split(circuit)

    circuit.barrier()
    circuit.z(range(n_part))
    circuit.measure(range(n_part),range(n_part)) 
    return circuit

def bottom_circuit(theta, n, n_part,dag):
    circuit = qk.QuantumCircuit(n_part,n_part)

    circuit = apply_W_bottom_before_split(circuit,theta, n, n_part)
    circuit = apply_u_gate(circuit,dag,0)
    circuit = apply_W_bottom_after_split(circuit)

    circuit.barrier()
    circuit.z(range(n_part))
    circuit.measure(range(n_part),range(n_part)) 
    return circuit

## These add the split W unitary to a input circuit
## The dag argument is used for the normal S or S^dagger
## dag = 0 uses S, dag = 1 uses S^dagger
## This would mean that W1 is obtained from top_unitary with dag = 0,
## W2 is obtained from top_unitary with dag = 1
## And same for M1,2 with bottom_unitary
def top_unitary(qc,theta,n,n_part,dag):
    qc = apply_W_top_before_split(qc,theta, n, n_part)
    qc = apply_u_gate(qc,dag,1)
    return qc

def bottom_unitary(qc,theta,n,n_part,dag):
    qc = apply_W_bottom_before_split(qc,theta, n, n_part)
    qc = apply_u_gate(qc,dag,0)
    qc = apply_W_bottom_after_split(qc)
    return qc