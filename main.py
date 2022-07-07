"""
TODO:
    maybe it should take an object with methods instead of just a generator? the methods could be higher-level then, like auto-computing more values. well maybe we'd still want an underlying generator protocol
"""

class Real:
    @staticmethod
    def _bitsFromInt(x):
        assert isinstance(x, int)

        exponent = 0
        bits = []
        while x:
            exponent += 1
            bits.append(x & 1)
            x >>= 1

        bits.append(exponent)
        bits.reverse()
        return iter(bits)

    @staticmethod
    def _bitsFromDiv(lhs, rhs):
        print(lhs, rhs)
        assert 0, (lhs, rhs)

    def __init__(self, generator_func):
        if isinstance(generator_func, int):
            i = generator_func
            generator_func = lambda: Real._bitsFromInt(i)

        self.generator_func = generator_func
        self.generator = None
        self.exponent = None
        self.bits = None

    class BitIterator:
        def __init__(self, real):
            self.real = real
            self.ngiven = 0

    def __iter__(self):
        return BitIterator(self)

    def ensureNBits(self, n):
        if self.exponent is None:
            self.generator = self.generator_func()
            self.exponent = self.generator.__next__()
            self.bits = []

        while len(self.bits) < n:
            try:
                self.bits.append(self.generator.__next__())
            except StopIteration:
                self.bits.append(0)

    def __str__(self):
        self.ensureNBits(54)
        return "%d %s" % (self.exponent, self.bits)

    @staticmethod
    def asReal(obj):
        if isinstance(obj, Real):
            return obj
        return Real(obj)

    def __truediv__(self, rhs):
        rhs = Real.asReal(rhs)
        return Real(Real._bitsFromDiv(self, rhs))

def main():
    one = Real(1)
    print(one)
    one_third = one / 3
    print("%f" % one_third)

if __name__ == "__main__":
    main()
