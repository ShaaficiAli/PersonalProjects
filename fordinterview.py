import math

  
def prime_test(number):
    square_root = int(math.sqrt(number))
    for i in range(2,square_root+1):
        if i%square_root==0:
            return False
    return True
