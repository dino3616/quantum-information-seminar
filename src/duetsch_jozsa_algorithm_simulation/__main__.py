from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def main() -> None:
    n = 3  # Input qubits
    # Case of constant function
    constant_oracle = constant_oracle_circuit(n)
    qc_const, counts_const = deutsch_jozsa_algorithm(constant_oracle, n)
    print(qc_const.draw("text"))
    print("Constant function result:", counts_const)

    print("\n\n")

    # Case of balanced function
    balanced_oracle = balanced_oracle_circuit(n)
    qc_balanced, counts_balanced = deutsch_jozsa_algorithm(balanced_oracle, n)
    print(qc_balanced.draw("text"))
    print("Balanced function result:", counts_balanced)


def deutsch_jozsa_algorithm(oracle: QuantumCircuit, n: int) -> tuple[QuantumCircuit, dict[str, int]]:
    """Simulate Deutsch-Jozsa algorithm."""

    # Setup quantum circuit
    qc = QuantumCircuit(n + 1, n)  # n qubits for input, 1 auxiliary qubit, n classical bits

    # Initialize quantum circuit
    qc.x(n)  # The auxiliary qubit is set to |1>
    qc.h(range(n + 1))  # Hadamard gate is applied to all qubits

    # Apply oracle
    qc.compose(oracle, inplace=True)

    # Apply Hadamard gate to the first n qubits
    qc.h(range(n))

    # Measure the first n qubits
    qc.measure(range(n), range(n))

    # Simulate the quantum circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    return qc, counts


def constant_oracle_circuit(n: int) -> QuantumCircuit:
    """Create a constant oracle circuit that returns 0 regardless of the input."""
    return QuantumCircuit(n + 1)


def balanced_oracle_circuit(n: int) -> QuantumCircuit:
    """Create a balanced oracle circuit that returns 0 for half the inputs and 1 for the other half."""
    oracle = QuantumCircuit(n + 1)
    for qubit in range(n):
        oracle.cx(qubit, n)  # Apply CNOT gate to create a balanced function

    return oracle


if __name__ == "__main__":
    main()
