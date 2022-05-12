
# Walrus operator (:=) is a new feature in Python 3.8
# This operator gives the C-style assignment operator that assigns value to the variable
# before it gives the whole expression a value
# e.g. in C/C++, we can use "if (x = some_func())>=0" to assign ret value of some_func() to x
# and decide if x is no less than 0 in the same line of code, since the expressions in C/C++ has values and side effects
# the side effect of "x = some_func()" is: "assign ret value of some_func() to x",
# and the value of the expression is the same as "x"
# In python we only have side effects in assignment operators, and it is illegal to write things like y=(x=0), which is
# commonly used in C/C++,
# but with walrus operator, this feature is available.
y = (x := 0)
assert x == 0 and y == 0
# the "x:=0" can now be used like it is in C/C++, and the value of it is equal to the left value of the walrus operator
# here are some changes to old python code:

# (1) reading files
# before walrus
with open("some.file", "r") as f:
    while True:
        line = f.readline()
        if not line:
            break
        # processing the line content
        continue

# after walrus
with open("some.file", "r") as f:
    while line := f.readline():
        # processing the line content
        continue


# (2) get value and decide
stock = {'wood': 10, 'steel': 20}


def build(material):

    if number_of_stock := stock.get(material):
        display = f'{material}: {number_of_stock}'
        if number_of_stock <= 10:
            return f'level_1 product, ' + display
        else:
            return f'level_2 product, ' + display
    else:
        return f'no product'


print([build(_) for _ in ['wood', 'steel', 'coal']])

