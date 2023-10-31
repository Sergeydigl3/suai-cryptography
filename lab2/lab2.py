class Twofish:
    def __init__(self, key):
        self.original_key = key
        self.key = key

    def encrypt(self, plaintext):
        return plaintext

    def decrypt(self, ciphertext):
        return ciphertext

    def expand_key(self):
        return self.key

    def _f_function(self, R0, R1, round_key):
        T0 = self._g_function(R0)
        T1 = self._g_function(R1)  # (ЦСЛ(R1, 8))
        F0 = (T0 + T1 + round_key) % 2 ** 32
        F1 = (T0 + 2 * T1 + round_key) % 2 ** 32
        return F0, F1

    def _g_function(self, x):
        return x

    def __str__(self):
        return "Twofish"
