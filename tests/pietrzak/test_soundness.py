import unittest

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from random import randint
from crypto_VDF.utils.number_theory import NumberTheory

class TestPietrazSoundness(unittest.TestCase):

# Quadratic Residue: An integer a is a quadratic residue modulo m if there exists an integer x such that x^2 ≡ a (mod m).
# For this implementation:
# If check_quadratic_residue(x, modulus) returns True, it means that x is a quadratic residue modulo modulus.
# If it returns False, it means that x is not a quadratic residue modulo modulus.
# In the soundness tests, we should choose values for x such that check_quadratic_residue(x, modulus) should return True. This ensures that the verification process correctly identifies valid quadratic residues.
# For modulus = 21, quadratic residues mod 21 = {0, 1, 4, 7, 9, 15, 16, 18} ??

    
    def test_fake_proof_verification(self):
        modulus = 21
        #x = 10000
        pp = PublicParams(delay=604, modulus=modulus)
        #x_list = [10, 100, 500, 2000, 10000]
        
        
        # Add test cases here
        # Test with different input values and fake proofs
        x_random_number = 10
        x_random_list = []
        for i in range(x_random_number):
            pp = PietrzakVDF.setup(security_param=256, delay=i)
            x = NumberTheory.generate_quadratic_residue(pp.modulus)
            x_random_list.append(x)


        print('\nTests with fake proof, all elements set to 1\n')
        print('Tests with these random input x : ')
        print(x_random_list)
        #for xi in x_list:
        for xi in x_random_list:
            out = PietrzakVDF.sol(public_params=pp, input_param=xi)
            proof = PietrzakVDF.compute_proof(public_params=pp, input_param=xi)
                # Test with a fake proof (all elements set to 1)
            fake_proof = [1 for _ in proof]
            
                # Run the verification with a fake proof
            verification = PietrzakVDF.verify(public_params=pp, input_param=xi, output_param=out, proof=fake_proof)
                # Check that the verification returns False
            self.assertFalse(verification, f"Failed for input {xi} with fake proof")
            
            
        ## Fake proof with all elements set to ? (other than 1?)
        # print('\nTests with fake proof, all elements set to 9\n')
        # for xi in x_list:
        #     out = PietrzakVDF.sol(public_params=pp, input_param=xi)
        #     proof = PietrzakVDF.compute_proof(public_params=pp, input_param=xi)
        #         # Test with a fake proof (all elements set to 9)
        #     fake_proof = [9 for _ in proof]
            
        #         # Run the verification with a fake proof
        #     verification = PietrzakVDF.verify(public_params=pp, input_param=xi, output_param=out, proof=fake_proof)
        #         # Check that the verification returns False
        #     self.assertFalse(verification, f"Failed for input {xi} with fake proof")





    def test_fake_output(self):
        modulus = 21
        # x = 10000
        pp = PublicParams(delay=604, modulus=modulus)
        # x_list = [10, 100, 500, 2000, 10000]
        
        x_random_number = 10
        x_random_list = []
        for i in range(x_random_number):
            pp = PietrzakVDF.setup(security_param=256, delay=i)
            x = NumberTheory.generate_quadratic_residue(pp.modulus)
            x_random_list.append(x)
        
        print('\nTests with fake output, (output_param=11, 200, 1000, 5000)\n')
        print('Tests with these random input x : ')
        print(x_random_list)
        for xi in x_random_list:
            output, proof = PietrzakVDF.compute_proof(public_params=pp, input_param=xi)
            # Run the verification with a fake proof
            print('\nFake output = 11')
            verification = PietrzakVDF.verify(public_params=pp, input_param=xi, output_param=11, proof=proof)
            # Check that the verification returns False
            self.assertFalse(verification)
            
            print('Fake output = 200')
            verification = PietrzakVDF.verify(public_params=pp, input_param=xi, output_param=200, proof=proof)
            self.assertFalse(verification)

            print('Fake output = 1000')
            verification = PietrzakVDF.verify(public_params=pp, input_param=xi, output_param=1000, proof=proof)
            self.assertFalse(verification)
            
            print('Fake output = 5000')
            verification = PietrzakVDF.verify(public_params=pp, input_param=xi, output_param=5000, proof=proof)
            self.assertFalse(verification)

        

        # Add test cases here
        # Test with different input values and fake outputs



     
if __name__ == '__main__':
        unittest.main()

