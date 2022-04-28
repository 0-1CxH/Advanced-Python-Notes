

class Pine:
    pine_class_variable = "PINE"

    def __init__(self):
        super(Pine, self).__init__()
        self.pine_instance_variable = "pine"


class Apple:
    apple_class_variable = "APPLE"

    def __init__(self):
        super(Apple, self).__init__()
        self.apple_instance_variable = "apple"


class Tree:
    def __init__(self):
        self.tree_value = "Tree"

    def get_tree_value(self):
        return self.tree_value

    def set_tree_value(self, value):
        self.tree_value = value + "Tree"

    export = property(get_tree_value, set_tree_value, None)


class Pineapple(Pine, Apple):
    pineapple_class_variable = \
        Pine.pine_class_variable + Apple.apple_class_variable

    tree_descriptor = Tree.export

    def __init__(self):
        super(Pineapple, self).__init__()
        self.pineapple_instance_variable = \
            self.pine_instance_variable + self.apple_instance_variable
        self.tree_descriptor = self.pineapple_instance_variable

    def __getattr__(self, item):
        print("Inside Pineapple.__getattr__()")
        if item == "caught_by_attr":
            return f"Value({item})"
        else:
            raise AttributeError("Invalid Item to Get")


# (1) __getattribute__ and __getattr__
# dir(obj) gets all the attributes that obj has.
# (1.1)when we use obj.attr ("." operator) to get attr of obj, __getattribute__ is called at first
# at this step, obj.attr is actually obj.__getattribute__("attr")
pineapple_instance = Pineapple()
assert pineapple_instance.tree_descriptor \
       == pineapple_instance.__getattribute__("tree_descriptor")
assert pineapple_instance.pineapple_instance_variable \
       == pineapple_instance.__getattribute__("pineapple_instance_variable")

# Now,
# let's get inside obj.__getattribute__("attr")
# (1.2)first, we try to find it in obj.__dict__ (the instance dict), the clause is obj.__dict__['attr'],
assert 'pineapple_instance_variable' in pineapple_instance.__dict__
assert not isinstance(pineapple_instance.__dict__['pineapple_instance_variable'], property)  # if not descriptor
assert pineapple_instance.__getattribute__("pineapple_instance_variable") \
       == pineapple_instance.__dict__['pineapple_instance_variable']  # return the value in dict directly


# (1.3)second, of there is no 'attr' in obj.__dict__ (the instance dict), find it in type(obj).__dict__ (the class dict)
assert 'pineapple_class_variable' not in pineapple_instance.__dict__
assert not isinstance(type(pineapple_instance).__dict__['pineapple_class_variable'], property)  # if not descriptor
assert pineapple_instance.__getattribute__("pineapple_class_variable") \
       == type(pineapple_instance).__dict__['pineapple_class_variable']  # return the value in dict directly
assert 'tree_descriptor' not in pineapple_instance.__dict__
assert isinstance(type(pineapple_instance).__dict__['tree_descriptor'], property)  # if it is a descriptor
assert pineapple_instance.__getattribute__("tree_descriptor") \
       == type(pineapple_instance).__dict__['tree_descriptor'].__get__(pineapple_instance, type(pineapple_instance))
# return __get__ method of it: type(obj).__dict__['attr'].__get__(obj, type(obj))
# note: content about descriptor is in "descriptor protocol" chapter


# (1.4)third, if 'attr' neither in instance dict nor class dict, try to find in its super classes in MRO sequence
# (ref: https://deepsource.io/blog/demystifying-python-descriptor-protocol/)
# note: see "C3 MRO" chapter to get more info about MRO
print(Pineapple.__mro__)
assert pineapple_instance.__getattribute__("apple_class_variable") \
       == Apple.__dict__['apple_class_variable']
assert pineapple_instance.__getattribute__("pine_class_variable") \
       == Pine.__dict__['pine_class_variable']

# (1.5) last, if 'attr' not in all the super classes, the __getattribute__ in (1.1) raises AttributeError and
# __getattr__ method is called by the "." operator, in this step, try to use obj.__getattr__('attr')
# if the __getattr__ still fails to get the result, it raises AttributeError again
try:
    pineapple_instance.__getattribute__("caught_by_attr")
except Exception as e:
    print(e)
assert pineapple_instance.caught_by_attr == pineapple_instance.__getattr__("caught_by_attr")
try:
    pineapple_instance.__getattr__("any_random_attr")
except Exception as e:
    print(e)

print("-"*20)

# (2) the dir() composition
# dir(instance) = dir(type(instance)) + instance.__dict__
assert set(dir(pineapple_instance)) - set(dir(type(pineapple_instance))) \
       == set(pineapple_instance.__dict__.keys())
print(pineapple_instance.__dict__)
# dir(direct_subclass_of_object) - dir(object) = direct_subclass_of_object.__dict__ - {'__doc__', '__init__'}
assert set(dir(Apple)) - set(dir(object)) == set(Apple.__dict__.keys())-{'__doc__', '__init__'}
assert set(dir(Pine)) - set(dir(object)) == set(Pine.__dict__.keys())-{'__doc__', '__init__'}
# dir(indirect_subclass_of_object) - union_of_dir(indirect_subclass_of_object.__bases__)
# =  type(instance).__dict__ - {'__init__', '__module__', '__doc__'}
print(
    set(dir(type(pineapple_instance))) - (set().union(dir(Pine)).union(dir(Apple)).union(dir(object))),
    set(type(pineapple_instance).__dict__.keys()),
)

