from unittest import TestCase as TC
import mutate
import bitstring


class MockRandom(object):
    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value

    def randrange(self, stop):
        return self.value


class TestModule(TC):
    def test_mutate_integer(self):
        value = 0
        mutate.random_generator = MockRandom(0)
        mutated_value0 = mutate.mutate_value(value)

        mutate.random_generator = MockRandom(0.99)
        mutated_value1 = mutate.mutate_value(value)

        self.assertSetEqual({mutated_value0, mutated_value1},
                {value + 1, value - 1})

    def test_mutate_bitstring(self):
        value = bitstring.Bitstring("00")
        mutated_value = mutate.mutate_value(value)
        self.assertNotEqual(value, mutated_value)

        mutate.random_generator = MockRandom(1)
        mutated_value_ = mutate.mutate_value(value)
        self.assertEqual(bitstring.Bitstring("01"), mutated_value_)

    def test_mutate_value_raises(self):
        with self.assertRaises(TypeError):
            mutate.mutate_value("unknown")