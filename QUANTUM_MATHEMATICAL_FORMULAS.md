QUANTUM MATHEMATICAL FORMULAS REFERENCE

This document contains all mathematical formulas and equations used in our quantum computing projects, including the Bloch sphere visualization, quantum circuit simulator, and entanglement calculations.

BLOCH SPHERE MATHEMATICS

Quantum State Representation
A single qubit quantum state can be written as:
|ψ⟩ = α|0⟩ + β|1⟩

Where α and β are complex amplitudes satisfying:
|α|² + |β|² = 1

Bloch Sphere Coordinates
The Bloch sphere represents quantum states using spherical coordinates (θ, φ):

x = sin(θ)cos(φ)
y = sin(θ)sin(φ)  
z = cos(θ)

State Vector to Bloch Coordinates Conversion
For a quantum state |ψ⟩ = α|0⟩ + β|1⟩, the Bloch coordinates are:

x = 2(α_real × β_real + α_imag × β_imag)
y = 2(α_imag × β_real - α_real × β_imag)
z = |α|² - |β|²

Probability Calculations
The probability of measuring |0⟩ and |1⟩ states:

P(|0⟩) = (1 + z)/2
P(|1⟩) = (1 - z)/2

QUANTUM GATE MATRICES

Pauli Gates

X Gate (NOT Gate):
X = [0  1]
    [1  0]

Y Gate:
Y = [0  -i]
    [i   0]

Z Gate:
Z = [1   0]
    [0  -1]

Hadamard Gate:
H = (1/√2) × [1   1]
              [1  -1]

Phase Gates

S Gate:
S = [1  0]
    [0  i]

T Gate:
T = [1     0    ]
    [0  e^(iπ/4)]

S† Gate (S dagger):
S† = [1   0]
     [0  -i]

T† Gate (T dagger):
T† = [1      0     ]
     [0  e^(-iπ/4)]

Rotation Gates

RX Gate (X-axis rotation by angle θ):
RX(θ) = [cos(θ/2)    -i×sin(θ/2)]
        [-i×sin(θ/2)   cos(θ/2)  ]

RY Gate (Y-axis rotation by angle θ):
RY(θ) = [cos(θ/2)  -sin(θ/2)]
        [sin(θ/2)   cos(θ/2)]

RZ Gate (Z-axis rotation by angle θ):
RZ(θ) = [e^(-iθ/2)     0    ]
        [   0      e^(iθ/2)]

TWO-QUBIT GATES

CNOT Gate (Controlled-NOT):
CNOT = [1  0  0  0]
       [0  1  0  0]
       [0  0  0  1]
       [0  0  1  0]

CZ Gate (Controlled-Z):
CZ = [1  0  0  0]
     [0  1  0  0]
     [0  0  1  0]
     [0  0  0 -1]

SWAP Gate:
SWAP = [1  0  0  0]
       [0  0  1  0]
       [0  1  0  0]
       [0  0  0  1]

Controlled Rotation Gates

CRX Gate (Controlled X-rotation):
CRX(θ) = [1     0     0     0   ]
         [0     1     0     0   ]
         [0     0  cos(θ/2) -sin(θ/2)]
         [0     0  -sin(θ/2) cos(θ/2)]

CRY Gate (Controlled Y-rotation):
CRY(θ) = [1     0     0     0   ]
         [0     1     0     0   ]
         [0     0  cos(θ/2) -sin(θ/2)]
         [0     0   sin(θ/2) cos(θ/2)]

CRZ Gate (Controlled Z-rotation):
CRZ(θ) = [1     0     0     0     ]
         [0     1     0     0     ]
         [0     0  e^(-iθ/2)  0     ]
         [0     0     0   e^(iθ/2)]

THREE-QUBIT GATES

Toffoli Gate (CCX):
CCX = [1  0  0  0  0  0  0  0]
      [0  1  0  0  0  0  0  0]
      [0  0  1  0  0  0  0  0]
      [0  0  0  1  0  0  0  0]
      [0  0  0  0  1  0  0  0]
      [0  0  0  0  0  1  0  0]
      [0  0  0  0  0  0  0  1]
      [0  0  0  0  0  0  1  0]

Fredkin Gate (CSWAP):
CSWAP = [1  0  0  0  0  0  0  0]
        [0  1  0  0  0  0  0  0]
        [0  0  1  0  0  0  0  0]
        [0  0  0  1  0  0  0  0]
        [0  0  0  0  1  0  0  0]
        [0  0  0  0  0  0  1  0]
        [0  0  0  0  0  1  0  0]
        [0  0  0  0  0  0  0  1]

QUANTUM STATE EVOLUTION

State Vector Evolution
The evolution of a quantum state under a unitary operator U:

|ψ_final⟩ = U|ψ_initial⟩

For a multi-qubit system with n qubits, the state vector has 2^n components.

Matrix Multiplication for Gate Application
When applying a gate matrix G to a state vector |ψ⟩:

ψ_new[i] = Σ_j G[i][j] × ψ[j]

Where the sum is over all possible basis states.

ENTANGLEMENT MATHEMATICS

Bell States
The four maximally entangled Bell states:

|Φ⁺⟩ = (1/√2)(|00⟩ + |11⟩)
|Φ⁻⟩ = (1/√2)(|00⟩ - |11⟩)
|Ψ⁺⟩ = (1/√2)(|01⟩ + |10⟩)
|Ψ⁻⟩ = (1/√2)(|01⟩ - |10⟩)

Entanglement Entropy
For a bipartite system in state |ψ⟩, the entanglement entropy is:

S = -Tr(ρ_A log₂(ρ_A))

Where ρ_A is the reduced density matrix of subsystem A.

Schmidt Decomposition
Any bipartite state can be written as:

|ψ⟩ = Σ_i λ_i |i_A⟩ ⊗ |i_B⟩

Where λ_i are Schmidt coefficients and |i_A⟩, |i_B⟩ are orthonormal bases.

MEASUREMENT MATHEMATICS

Born Rule
The probability of measuring outcome |i⟩ when the system is in state |ψ⟩:

P(i) = |⟨i|ψ⟩|²

Expectation Value
The expectation value of observable O in state |ψ⟩:

⟨O⟩ = ⟨ψ|O|ψ⟩

Density Matrix
For a mixed state, the density matrix is:

ρ = Σ_i p_i |ψ_i⟩⟨ψ_i|

Where p_i are probabilities and |ψ_i⟩ are pure states.

QUANTUM ALGORITHMS

Deutsch-Jozsa Algorithm
For a function f: {0,1}^n → {0,1}, the algorithm determines if f is constant or balanced using:

|ψ⟩ = (1/√2^n) Σ_x |x⟩ ⊗ (1/√2)(|0⟩ - |1⟩)

Grover's Algorithm
The search algorithm uses the Grover operator:

G = (2|ψ⟩⟨ψ| - I)O

Where |ψ⟩ is the uniform superposition and O is the oracle.

Quantum Fourier Transform
The QFT on n qubits is defined as:

QFT|j⟩ = (1/√2^n) Σ_k e^(2πijk/2^n) |k⟩

COMPLEX NUMBER OPERATIONS

Complex Number Representation
A complex number z = a + bi where:
- a is the real part
- b is the imaginary part
- i = √(-1)

Complex Conjugate
z* = a - bi

Magnitude
|z| = √(a² + b²)

Phase
φ = arctan(b/a)

Euler's Formula
e^(iθ) = cos(θ) + i×sin(θ)

NORMALIZATION CONDITIONS

State Vector Normalization
For a quantum state |ψ⟩ = Σ_i α_i |i⟩:

Σ_i |α_i|² = 1

Unitary Matrix Condition
A matrix U is unitary if:

U†U = UU† = I

Where U† is the conjugate transpose of U.

Hermitian Matrix Condition
A matrix H is Hermitian if:

H = H†

Where H† is the conjugate transpose of H.

PROBABILITY AMPLITUDES

Interference
When two probability amplitudes add:

P = |α₁ + α₂|² = |α₁|² + |α₂|² + 2Re(α₁*α₂)

The last term represents quantum interference.

Superposition
A qubit in superposition state:

|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩

Where θ and φ are the polar and azimuthal angles on the Bloch sphere.

PHASE RELATIONS

Global Phase
Two states |ψ⟩ and e^(iφ)|ψ⟩ represent the same physical state.

Relative Phase
The phase difference between |0⟩ and |1⟩ components affects measurement probabilities.

Phase Gates
Phase gates add relative phases without changing measurement probabilities of |0⟩ and |1⟩.

This comprehensive collection covers all the mathematical foundations used in our quantum computing visualization and simulation projects.
