from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def main() -> None:
    # Oracle that marks the state |11> as the solution
    oracle = QuantumCircuit(2)
    oracle.cz(0, 1)  # Apply a Z gate when both qubits are |1>

    # Grover's algorithm simulation
    qc, counts = grover_algorithm(oracle)
    print(qc.draw("text"))
    print("Grover's algorithm result:", dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)))


def grover_algorithm(oracle: QuantumCircuit) -> tuple[QuantumCircuit, dict[str, int]]:
    """Simulate Grover's algorithm for 2-qubit system."""

    # Setup quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Step 1: Initialize both qubits to |0>, then apply Hadamard gate to create superposition
    qc.h([0, 1])

    # Step 2: Apply the oracle
    qc.compose(oracle, inplace=True)

    # Step 3: Apply Grover's diffusion operator (inversion about the mean)
    # Apply Hadamard to both qubits
    qc.h([0, 1])
    # Apply X (Pauli-X gate) to both qubits
    qc.x([0, 1])
    # Apply a CZ gate (controlled-Z) between the two qubits
    qc.h(1)
    qc.cz(0, 1)
    qc.h(1)
    # Apply X to both qubits again
    qc.x([0, 1])
    # Apply Hadamard to both qubits again
    qc.h([0, 1])

    # Step 4: Measure the qubits
    qc.measure([0, 1], [0, 1])

    # Simulate the quantum circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    return qc, counts


if __name__ == "__main__":
    main()
