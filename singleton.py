import threading
from functools import wraps


class CommonClass:
    # this part runs for once
    print(f'Entering CommonClass creating process')
    class_static_property = 1
    print(f'Class static property assigned {class_static_property=}\n')

    def __new__(cls, *args, **kwargs):
        # this part runs each time a new object is going to be created
        print(f'Entering {cls} __new__() method')
        print(f'{super()=}')
        new_obj = super().__new__(cls)
        print(f'Return new object {new_obj}')
        return new_obj

    def __init__(self, value):
        # this part runs each time a new object is going to be initialized
        print(f'Entering {self} __init__() method')
        super(CommonClass, self).__init__()
        self.object_property = value
        print(f'Object property assigned {self.object_property=}')
        print(f'Return initialized object {self}')


# When running this script, even without any reference of CommonClass
# the CommonClass is created and the static properties are initialized.
print(f"{__name__=}\n")
assert 'CommonClass' in dir()
assert 'class_static_property' in dir(CommonClass)

# The usual way to instantiate a class is to use <class_name>(init value), such as:
usual_instantiate = CommonClass(0)
print('\n')

# Actually, this process is two-stepped
# the first step is to call __new__ on the class
# it allocates memory/identity for the new object
step_instantiate = CommonClass.__new__(CommonClass)
# the class properties are not assigned for now
assert 'object_property' not in dir(step_instantiate)
print('\n')
# the second step is to call __init__ on the new object that __new__ returns
# it assigns values to properties of this object instance
step_instantiate.__init__(0)
assert 'object_property' in dir(step_instantiate)
print('\n')
# when using the <class_name>(init value), it automatically calls __new__ followed by __init__
# so that the arg list of __new__ and __init__ should be compatible in the case

print("*"*20)


# The Singleton design pattern modifies __new__ method to intercept the construction of new object of this class
# since the static properties of the class only initialized for once and all objects of the class has public
# class static properties, the only object of a Singleton class can be stored in the static memory
class SingletonClass(CommonClass):
    print(f'Entering SingletonClass creating process')
    _singleton_object = None
    print(f'Class static property assigned {_singleton_object=}\n')

    def __new__(cls, *args, **kwargs):
        print(f'Entering {cls} __new__() method')
        print(f'{super()=}')
        if not cls._singleton_object:
            cls._singleton_object = super().__new__(cls)
            print("singleton object is constructed")
        print(f'Return singleton object {cls._singleton_object}')
        return cls._singleton_object

    def __init__(self, value):
        print(f'Entering {self} __init__() method')
        super().__init__(value)
        print(f'Return initialized object {self}')


# Also, the static properties are initialized for SingletonClass before reference
print(f"{__name__=}\n")
assert 'SingletonClass' in dir()
assert '_singleton_object' in dir(SingletonClass)

singleton_instance_1 = SingletonClass.__new__(SingletonClass)
print('\n')
"""
Entering <class '__main__.SingletonClass'> __new__() method
super()=<super: <class 'SingletonClass'>, <SingletonClass object>>
Entering <class '__main__.SingletonClass'> __new__() method
super()=<super: <class 'CommonClass'>, <SingletonClass object>>
Return new object <__main__.SingletonClass object at 0x0000021B83206E20>
singleton object is constructed
Return singleton object <__main__.SingletonClass object at 0x0000021B83206E20>
"""
singleton_instance_1.__init__(0)
print('\n')
"""
Entering <__main__.SingletonClass object at 0x0000021B83206E20> __init__() method
Entering <__main__.SingletonClass object at 0x0000021B83206E20> __init__() method
Object property assigned self.object_property=0
Return initialized object <__main__.SingletonClass object at 0x0000021B83206E20>
singleton object is initialized
Return initialized object <__main__.SingletonClass object at 0x0000021B83206E20>
"""

singleton_instance_2 = SingletonClass.__new__(SingletonClass)
# when calling SingletonClass.__new__ for the second time,
# it does not enter the object construction of its base class
# instead, it returns the same object as singleton_instance_1 (the same memory address)
print('\n')
"""
Entering <class '__main__.SingletonClass'> __new__() method
super()=<super: <class 'SingletonClass'>, <SingletonClass object>>
Return singleton object <__main__.SingletonClass object at 0x000001A0C0176E20>
"""

singleton_instance_2.__init__(5)
# when calling __init__ for the second time, it does not enter the object initialization
# instead, it returns the same object as singleton_instance_1 (the same memory address)
print('\n')
"""
Entering <__main__.SingletonClass object at 0x0000023E438A6E20> __init__() method
Entering <__main__.SingletonClass object at 0x0000023E438A6E20> __init__() method
Object property assigned self.object_property=5
Return initialized object <__main__.SingletonClass object at 0x0000023E438A6E20>
Return initialized object <__main__.SingletonClass object at 0x0000023E438A6E20>
"""

# the two singleton instances are exactly the same
# (use "is" to make sure it shares the same memory address)
assert singleton_instance_1.object_property == 5
assert singleton_instance_1 is singleton_instance_2


# The above SingletonClass that bases on the CommonClass can be changed to decorator
def singleton_decorator(cls):
    _singleton_object = None

    @wraps
    def get_new_object(*args, **kwargs):
        with threading.Lock():  # lock acquired to ensure thread safety
            nonlocal _singleton_object
            if not _singleton_object:
                _singleton_object = cls.__new__(cls, *args, **kwargs)
        return _singleton_object

    return get_new_object


@singleton_decorator
class DecoratedCommonClass:
    def __init__(self):
        print(f"object address {hash(self)}")
        pass


assert DecoratedCommonClass() is DecoratedCommonClass()
