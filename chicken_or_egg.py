
# Everything in Python is an object and has a type

def print_object_info(obj):
    print(f'{obj=}')
    print(f'{type(obj)=}')
    print(f'{isinstance(obj, type)=}')
    print(f'{isinstance(obj, object)=}')
    print(f'{obj.__class__=}')
    try:
        print(f'{obj.__bases__=}')
    except AttributeError :
        pass


# (1) The commonly used built-in class and object
for t in [dict, dict()]:  # other built-in classes such as int, float, ... are the same as dict
    print_object_info(t)
"""
obj=<class 'dict'>
type(obj)=<class 'type'>
isinstance(obj, type)=True
isinstance(obj, object)=True
obj.__class__=<class 'type'>
obj.__bases__=(<class 'object'>,)

obj={}
type(obj)=<class 'dict'>
isinstance(obj, type)=False
isinstance(obj, object)=True
obj.__class__=<class 'dict'>
"""
# we can see the class names (dict, int, float, ...) are objects of class "type", and its base class is "object"
# the instances of these classes ({}, 0, 0.0, ...) are objects of their own classes


# (2) Inherited classes of built-in classes
class DictInherited(dict):
    def __init__(self):
        super(DictInherited, self).__init__()


for t in [DictInherited, DictInherited()]:
    print_object_info(t)
"""
obj=<class '__main__.DictInherited'>
type(obj)=<class 'type'>
isinstance(obj, type)=True
isinstance(obj, object)=True
obj.__class__=<class 'type'>
obj.__bases__=(<class 'dict'>,)

obj={}
type(obj)=<class '__main__.DictInherited'>
isinstance(obj, type)=False
isinstance(obj, object)=True
obj.__class__=<class '__main__.DictInherited'>
"""
# The class name (DictInherited) is an object of "type",
# and its base class is "dict" (base class of "dict" is "object")
# the instance of DictInherited is object of its own class '__main__.DictInherited'


class DefaultInherited:
    def __init__(self):
        pass


print_object_info(DefaultInherited)

"""
obj=<class '__main__.DefaultInherited'>
type(obj)=<class 'type'>
isinstance(obj, type)=True
isinstance(obj, object)=True
obj.__class__=<class 'type'>
obj.__bases__=(<class 'object'>,)

"""
# The default base class of a new class is "object" if not specified


# (3) Type and object
# every Python object has the only ancestor "object" class
# every Python type has the only ancestor "type" metaclass
# this also works for "object" and "type" themselves:
# class "object" has type "type", and "type" is a class "object"

for t in [object, type, object()]:
    print_object_info(t)
"""
obj=<class 'object'>
type(obj)=<class 'type'>
isinstance(obj, type)=True
isinstance(obj, object)=True
obj.__class__=<class 'type'>
obj.__bases__=()

obj=<class 'type'>
type(obj)=<class 'type'>
isinstance(obj, type)=True
isinstance(obj, object)=True
obj.__class__=<class 'type'>
obj.__bases__=(<class 'object'>,)

obj=<object object at 0x000001E90B198490>
type(obj)=<class 'object'>
isinstance(obj, type)=False
isinstance(obj, object)=True
obj.__class__=<class 'object'>
"""

print(f'{isinstance(type, object), isinstance(object, type)=}')
print(f'{isinstance(object, object), isinstance(type, type)=}')
# It is like the old question: which comes first, chicken or egg?
# actually, "type" is metaclass, a factory class that makes "class"es
# (manufacture class objects and giving them class names)
# "object" is a class, the base of every class, it has type "type",
# and any class bases on it has type "type" to specify that this is a class
