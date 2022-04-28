import math


# (1) descriptor protocol
# A descriptor can be used in a class and be used like a variable
# An object that follows the descriptor protocol can be treated like descriptor
# which means that this object should implement __get__, and can also implement __set__ and __delete__ optionally
class Radius:
    def __init__(self, val=0):
        self._val = val

    def __get__(self, instance, owner):
        return self._val

    def __set__(self, instance, val):
        if val < 0:
            raise ValueError("Radius should be non-negative value")
        self._val = val

    def __delete__(self, instance):
        del self._val


# note that the descriptor defined by the above way can only be used as class variable but not instance variable
class UseRadius:
    circle_radius = Radius()


ud1 = UseRadius()
print(ud1.circle_radius)
assert UseRadius.__dict__['circle_radius'].__get__(ud1, UseRadius) == ud1.circle_radius
# when visiting ud1.circle_radius, it is actually visiting UseRadius.circle_radius
# by UseRadius.__dict__['circle_radius'].__get__(ud1, UseRadius)
ud1.circle_radius = 1
# when changing ud1.circle_radius to new_value, it is actually changing UseRadius.circle_radius
# by UseRadius.__dict__['circle_radius'].__set__(ud1, new_value)
print(ud1.circle_radius)
UseRadius.__dict__['circle_radius'].__set__(ud1, 2)
print(ud1.circle_radius)
# the __set__ method can be used to intercept the modification of assignment
# therefore it can be used to check for input
try:
    ud1.circle_radius = -1
except Exception as e:
    print(e)
# all the instances of UseRadius shares the memory space of the class
# changing descriptor of one instance will also change descriptor of other instances
ud2 = UseRadius()
print(ud2.circle_radius)
ud2.circle_radius = 3
print(ud1.circle_radius)
print("-"*20)


# (2) property decorator
# an easier way to make a descriptor is to use property decorator
class Circle:
    def __init__(self, val=0):
        self._val = val

    @property
    def radius(self):
        return self._val

    @radius.setter
    def radius(self, val):
        if val < 0:
            raise ValueError("Radius should be non-negative value")
        self._val = val

    def get_area(self):
        return math.pi * self.radius ** 2


# this works the same way as the classes above, @property makes radius a descriptor of the instance
circle_instance = Circle()
circle_instance.radius = 2
print(circle_instance.radius, circle_instance.get_area())
try:
    circle_instance.radius = -1
except Exception as e:
    print(e)
# note that the descriptor is owned by the instance rather than class, so instances do not interfere with others
circle_instance_2 = Circle(3)
print(circle_instance_2.radius, circle_instance_2.get_area())
print("-"*20)


# (3) how does @property builds descriptor
# actually,
# the property decorator makes a descriptor by setting the methods to be __get__, __set__ or __delete__ in the
# descriptor protocol, if we look at the source code of "property", we can see the syntax of "property" is
# property(fget=None, fset=None, fdel=None, doc=None) (ref:https://www.geeksforgeeks.org/descriptor-in-python/)
# the thing that property decorator really does is to
# (1) bind the arguments to descriptor protocol functions: fget to __get__, fset to __set__, fdel to __delete__
# (2) set a property object in the class that supports lazy calculation
class CircleVersion2:
    def __init__(self, val=0):
        self._val = val

    def get_radius(self):
        return self._val

    def set_radius(self, val):
        if val < 0:
            raise ValueError("Radius should be non-negative value")
        self._val = val

    def get_area(self):
        return math.pi * self.radius ** 2

    radius = property(get_radius, set_radius, None)


circle_v2_instance = CircleVersion2()
circle_v2_instance.radius = 1
print(circle_v2_instance.radius, circle_v2_instance.get_area())
# the "property" object is lazy evaluation, so, even the radius is in __dict__ of class, its real value is
# obtained when we visit it in object, and evaluated based on the value of instance
circle_v2_instance_2 = CircleVersion2()
print(circle_v2_instance_2.get_area())
# the property object is dynamic, it is "property" type in the class, and changes to its dynamic type in instance
assert isinstance(CircleVersion2.radius, property)
assert not isinstance(CircleVersion2.radius, int)
assert not isinstance(circle_v2_instance.radius, property)
assert isinstance(circle_v2_instance.radius, int)
print("-"*20)


# (4) lazy evaluation
class Dividing:
    def __init__(self, den_, div_):
        self.denominator = den_
        self.divider = div_

    @property
    def result(self):
        return self.denominator/self.divider


div_instance = Dividing(5, 2)
# the "result" is still property object until ww get it by __get__
print(Dividing.__dict__['result'])
print(div_instance.result)
div_instance = Dividing(5, 0)
# the "result" = denominator/divider is not valid but there is no error raised since the evaluation is lazy
