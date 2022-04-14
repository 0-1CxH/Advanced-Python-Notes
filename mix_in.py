
# The mixin design pattern uses multiple inheritance to flexibly add new features to the base classes

class Animal:
    def live(self): return

"""
Need to implement:
  - Duck that can live, swim, run
  - Eagle that can live, fly and peck
  - Goose that live, swim, run, fly and peck
"""
"""
If use the classical and traditional single inheritance / TEMPLATE method design pattern,
    - Duck: inherited from Animal, and implemented run(), swim()
        class Duck(Animal):
            def run(self): return
            def swim(self): return
    - Eagle: inherited from Animal, and implemented fly(), peck()
        class Eagle(Animal):
            def fly(self): return
            def peck(self): return
    - Goose: inherited from Animal, and implemented run(), swim(), peck(), fly()
        although run() and swim() are implemented in Duck, we cannot directly inherit Duck
        although peck() and fly() are implemented in Eagle, we cannot directly inherit Eagle, too
        class Goose(Animal):
            def run(self): return
            def fly(self): return
            def swim(self): return
            def peck(self): return
        it is clear that the implementation of some methods are repeated
"""


# use MIXIN design pattern to first implement the mixin classes :
class FlyingMixin:
    def fly(self): return


class SwimmingMixin:
    def swim(self): return


class RunningMixin:
    def run(self): return


class PeckingMixin:
    def peck(self): return


# then implement the animals using base class Animal and mixin classes:
class Duck(Animal, RunningMixin, SwimmingMixin): pass
class Eagle(Animal, FlyingMixin, PeckingMixin): pass
class Goose(Animal, RunningMixin, SwimmingMixin, FlyingMixin, PeckingMixin): pass


"""
If here comes more classes to implement:
    - Chicken that can live, run and peck
    - Seagull that can live, swim and fly
Use TEMPLATE design pattern to repeat the implementations of the same methods again in these new classes;
while use MIXIN design pattern to simply combining the mixin classes:
"""
class Chicken(Animal, RunningMixin, PeckingMixin): pass
class Seagull(Animal, SwimmingMixin, FlyingMixin): pass
