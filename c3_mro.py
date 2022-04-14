# In the circumstances of multiple inheritances, when calling a method (visiting an attribute) in a child class,
# from which parent class the method is called (attribute is visited)?
# This is the "method resolution order"(MRO) problem

# in older versions (python <=2.2), the MRO policy is depth-first-search(DFS),
# but this is going to cause the problem in the "diamond inheritance" circumstance

# the new policy for MRO is C3 in later versions, C3 linearization algorithm follows:
# - Inheritance graph determines the structure of method resolution order.
# - User have to visit the super class only after the method of the local classes are visited.
# - Monotonicity
# (ref: https://www.geeksforgeeks.org/method-resolution-order-in-python-inheritance/)

"""
C3 algorithm:
    MRO(cls) = [cls] + merge(*(MRO(b) for b in cls.__bases__), cls.__bases__)
    merge() function: for multiple lists of input, check the first element of the list, if the element either
                    appears in the first place in ALL other lists or it does not exist in other lists, add this element
                    to result list, add remove the element from all the lists; repeat until all the lists are empty
"""

class L1A(object): pass
class L1B(object): pass
class L1C(object): pass
class L2A(L1A, L1B): pass
class L2B(L1B, L1C): pass
class L2C(L1B, L1C): pass
class L3A(L1A, L2C, L1B): pass
class L3B(L1A, L2B, L1C): pass
class L4(L3A, L3B, L2A): pass


# use __mro__ to check the method resolution order of super classes of L4
for cls in L4.__bases__:
    print([x.__name__ for x in cls.__mro__])
"""
L3A MRO list:
['L3A', 'L1A', 'L2C', 'L1B', 'L1C', 'object']
L3B MRO list:
['L3B', 'L1A', 'L2B', 'L1B', 'L1C', 'object']
L2A MRO list:
['L2A', 'L1A', 'L1B', 'object']
"""

# run C3 algorithm to get L4.__mro__ from mro of its bases
"""
MRO(L4) =  ['L4']' + merge(MRO(L3A), MRO(L3B), MRO(L2A)), [L3A, L3B, L2A])
      =  ['L4'] + merge(
            ['L3A', 'L1A', 'L2C', 'L1B', 'L1C', 'object'],
            ['L3B', 'L1A', 'L2B', 'L1B', 'L1C', 'object'],
            ['L2A', 'L1A', 'L1B', 'object'],
            ['L3A', 'L3B', 'L2A'])
      = ['L4', 'L3A', ] + merge(
            ['L1A', 'L2C', 'L1B', 'L1C', 'object'],
            ['L3B', 'L1A', 'L2B', 'L1B', 'L1C', 'object'],
            ['L2A', 'L1A', 'L1B', 'object'],
            ['L3B', 'L2A'])
      = ['L4', 'L3A', 'L3B'] + merge(
            ['L1A', 'L2C', 'L1B', 'L1C', 'object'],
            ['L1A', 'L2B', 'L1B', 'L1C', 'object'],
            ['L2A', 'L1A', 'L1B', 'object'],
            ['L2A'])
      = ['L4', 'L3A', 'L3B', 'L2A'] + merge(
            ['L1A', 'L2C', 'L1B', 'L1C', 'object'],
            ['L1A', 'L2B', 'L1B', 'L1C', 'object'],
            ['L1A', 'L1B', 'object'],
            [])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A'] + merge(
            ['L2C', 'L1B', 'L1C', 'object'],
            ['L2B', 'L1B', 'L1C', 'object'],
            ['L1B', 'object'],[])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C'] + merge(
            ['L1B', 'L1C', 'object'],
            ['L2B', 'L1B', 'L1C', 'object'],
            ['L1B', 'object'],[])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C', 'L2B'] + merge(
            ['L1B', 'L1C', 'object'],
            ['L1B', 'L1C', 'object'],
            ['L1B', 'object'],[])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C', 'L2B', 'L1B'] + merge(
            ['L1C', 'object'],
            ['L1C', 'object'],
            ['object'],[])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C', 'L2B', 'L1B', 'L1C'] + merge(
            ['object'],
            ['object'],
            ['object'],[])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C', 'L2B', 'L1B', 'L1C', 'object'] + merge([],[],[],[])
      = ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C', 'L2B', 'L1B', 'L1C', 'object']
"""

assert [x.__name__ for x in L4.__mro__] == ['L4', 'L3A', 'L3B', 'L2A', 'L1A', 'L2C', 'L2B', 'L1B', 'L1C', 'object']

print(L4.__mro__)
"""
L4 MRO list:
(<class '__main__.L4'>, <class '__main__.L3A'>, <class '__main__.L3B'>, <class '__main__.L2A'>, <class '__main__.L1A'>, 
<class '__main__.L2C'>, <class '__main__.L2B'>, <class '__main__.L1B'>, <class '__main__.L1C'>, <class 'object'>)
"""

try:
    class E1(L2C, L3A): pass
    # class E1 cannot be constructed since the MRO fails on getting the order
    """
    L2C MRO list:
    (<class '__main__.L2C'>, <class '__main__.L1B'>, <class '__main__.L1C'>, <class 'object'>)
    L3A MRO list:
    (<class '__main__.L3A'>, <class '__main__.L1A'>, <class '__main__.L2C'>, <class '__main__.L1B'>, 
    <class '__main__.L1C'>, <class 'object'>)
    Use C3:
    MRO(E1) = ['E1'] + merge(MRO(L2C), MRO(L3A), ['L2C', 'L3A'])
            = ['E1'] + merge(
                ['L2C', 'L1B', 'L1C', 'object'],
                ['L3A', 'L1A', 'L2C', 'L1B', 'L1C', 'object'],
                ['L2C', 'L3A']
            )
    Cannot go further since L2C and L3A appears in other list but not on the first place in all other lists 
    """
except TypeError as e:
    print(e)
