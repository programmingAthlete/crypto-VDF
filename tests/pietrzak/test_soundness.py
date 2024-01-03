import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
#from crypto_VDF.utils.number_theory import

class TestPietrazSoundness(unittest.TestCase):

# Quadratic Residue: An integer a is a quadratic residue modulo m if there exists an integer x such that x^2 ≡ a (mod m).
# For this implementation:
# If check_quadratic_residue(x, modulus) returns True, it means that x is a quadratic residue modulo modulus.
# If it returns False, it means that x is not a quadratic residue modulo modulus.
# In the soundness tests, we should choose values for x such that check_quadratic_residue(x, modulus) should return True. This ensures that the verification process correctly identifies valid quadratic residues.
# For modulus = 21, quadratic residues mod 21 = {0, 1, 4, 7, 9, 15, 16, 18} ??

    def test_fake_proof_verification(self):
        modulus = 21
        x = 10
        pp = PublicParams(delay=604, modulus=modulus)
        
        # out = PietrzakVDF.sol(public_params=pp, input_param=x)
        # proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # fake_proof = [1 for _ in proof]
        # # Run the verification with a fake proof
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=fake_proof)
        # # Check that the verification returns False
        # self.assertFalse(verification)

        # Add test cases here
        # Test with different input values and fake proofs
        for x in range(1, 11):
            out = PietrzakVDF.sol(public_params=pp, input_param=x)
            proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
            # Test with a fake proof (all elements set to 1)
            fake_proof = [1 for _ in proof]
            # Run the verification with a fake proof
            verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=out, proof=fake_proof)
            # Check that the verification returns False
            self.assertFalse(verification, f"Failed for input {x} with fake proof")



    def test_fake_output(self):
        modulus = 21
        x = 10
        pp = PublicParams(delay=604, modulus=modulus)
        
        # output, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)
        # # Run the verification with a fake proof
        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=11, proof=proof)
        # # Check that the verification returns False
        # self.assertFalse(verification)

        # verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=1000, proof=proof)
        # self.assertFalse(verification)

        # Add test cases here
        # Test with different input values and fake outputs
        for x in range(1, 11):
            output, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x)

            # Run the verification with a fake proof
            # Test with a fake output (increased by 1)
            verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=output + 1, proof=proof)
            # Check that the verification returns False
            self.assertFalse(verification, f"Failed for input {x} with fake output (increased)")

            # Test with a fake output (decreased by 1)
            verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=output - 1, proof=proof)
            # Check that the verification returns False
            self.assertFalse(verification, f"Failed for input {x} with fake output (decreased)")

            # Test with a fake output (set to a random value)
            verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=999, proof=proof)
            # Check that the verification returns False
            self.assertFalse(verification, f"Failed for input {x} with fake output (random value)")


if __name__ == '__main__':
        unittest.main()

