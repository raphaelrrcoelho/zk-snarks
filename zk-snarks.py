from hashlib import sha256
from random import getrandbits

def C(x, w):
    return sha256(w).hexdigest() == x

def G(l):
    """Key Generator Funcion

    Generates a proving key and a verification key given a program C
    that should be satisfied.

    Args:
        l (int): Lambda key.
    Returns
        pk (int): Proving key that equals l + id(C).
        vk (int): Verification key that equals l + id(C).
    """

    pk = l + id(C)
    vk = l - id(C)

    return pk, vk

def P(pk, x, w):
    """Proof Generator Funcion

    Generates a verifiable proof that the prover knows a witness w that
    satisfies the program C. If C(x, w) is True, proof equals pk + 1.

    Args:
        pk (int): Proving key.
        x (str): Hashed witness.
        w (str): Witness.
        C (function): Program that should be satisfied.
    Returns
        proof (int): Verifiable proof that x and w satisfies C.
    """

    proof = pk + C(x, w)
    return proof

def V(vk, x, proof):
    #FIXME: Think how to attach the correct proof to x
    correct_proof = vk + 2 * id(C) + 1
    return proof == correct_proof

lambda_key = getrandbits(256)

witness = 'zk-snarks'.encode('utf-8') # secret parameter
H = sha256(witness).hexdigest()

pk, vk = G(lambda_key)

false_witness = 'non-zk-snarks'.encode('utf-8')
false_proof = P(pk, H, false_witness)
false_verification = V(vk, H, false_proof)
print(false_witness, false_proof, false_verification)

proof = P(pk, H, witness)
verification = V(vk, H, proof)
print(witness, proof, verification)
