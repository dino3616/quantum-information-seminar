from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def main() -> None:
    # Case of constant function
    constant_oracle = QuantumCircuit(2)
    qc_const, counts_const = deutsch_algorithm(constant_oracle)
    print(qc_const.draw("text"))
    print("Constant function result:", counts_const)

    print("\n\n")

    # Case of balanced function
    balanced_oracle = QuantumCircuit(2)
    balanced_oracle.cx(0, 1)  # Apply CNOT gate to create a balanced function
    qc_balanced, counts_balanced = deutsch_algorithm(balanced_oracle)
    print(qc_balanced.draw("text"))
    print("Balanced function result:", counts_balanced)


def deutsch_algorithm(oracle: QuantumCircuit) -> tuple[QuantumCircuit, dict[str, int]]:
    """Simulate Deutsch's algorithm."""

    # Setup quantum circuit
    qc = QuantumCircuit(2, 1)  # 2-qubit, 1-classical-bit

    # Initialize quantum circuit
    qc.x(1)  # Second qubit is set to |1>
    qc.h([0, 1])  # Hadamard gate is applied to both qubits

    # Apply oracle
    qc.compose(oracle, inplace=True)

    # Apply Hadamard gate to the first qubit
    qc.h(0)

    # Measure the first qubit
    qc.measure(0, 0)

    # Simulate the quantum circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    return qc, counts


if __name__ == "__main__":
    main()
