import collections.abc


class NaturalNumbers:
    """
    This class follow the iterator protocol:
    - implemented __iter__ that returns an iterator, so that iter() can be used on it
    - implemented __next__ that returns the next state in iteration
    """

    def __init__(self, max_iter_times=1000):
        self.internal_state = -1
        self.max_iter_times = max_iter_times

    def __iter__(self):
        return self

    def __next__(self):
        self.internal_state += 1
        if self.internal_state >= self.max_iter_times:
            raise StopIteration
        return self.internal_state


# use collections.abc.Iterator to check whether class NaturalNumbers follows the iterator protocol
# the following assertion is True, so that the class follows the iterator protocol
assert isinstance(NaturalNumbers(), collections.abc.Iterator) is True


iter_times = 5
# use a "for" clause to iterate through NaturalNumberGenerator
nn1 = NaturalNumbers(iter_times)
for value in nn1:
    print(value)

# the nature of "for" is:
# (1) call iter() on the object (equals to call object's __iter__() method)
# (2) call next() on the object (equals to call object's __next__() method)

# now, do not use "for", use the iterator protocol to achieve the same result
nn2 = NaturalNumbers(iter_times)
nn2_iterator = nn2.__iter__()
while True:
    try:
        value = nn2_iterator.__next__()
        print(value)
    except StopIteration:
        break


# ----APPENDIX----------------------------------------------------------
# Note: this part shall be viewed after viewing the "two_generators" chapter
class NaturalNumberGenerator:
    """
    This is the same thing as NaturalNumbers,
    but the __iter__ method is using yield, which means this is a generator.
    Note that: The Generators is a subset of Iterators
    """

    def __init__(self, max_iter_times=1000):
        self.internal_state = -1
        self.max_iter_times = max_iter_times

    def __iter__(self):
        while True:
            self.internal_state += 1
            if self.internal_state < self.max_iter_times:
                yield self.internal_state
            else:
                break


# the class NaturalNumberGenerator does not follow iterator protocol
# since it does not implement __next__ method
assert isinstance(NaturalNumberGenerator(), collections.abc.Iterator) is False
# but the return value of its __iter__ function is a Generator (hence also an Iterator)
# since function with "yield" returns a generator
assert isinstance(NaturalNumberGenerator().__iter__(), collections.abc.Iterator) is True
assert isinstance(NaturalNumberGenerator().__iter__(), collections.abc.Generator) is True


nng = NaturalNumberGenerator(5)
print([_ for _ in nng])
