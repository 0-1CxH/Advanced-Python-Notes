import collections.abc

# There are two methods of making a Generator
# (1) Use a GenExpr
# (2) The return value of function with "yield" clause

upper_bound = 10

# (1) Generator expression
even_number_generator_expression = (x for x in range(upper_bound) if not x % 2)

# the following expression prints "generator object <genexpr> at ..."
print(even_number_generator_expression)
# the following assertion is True since it is a <genexpr> generator
assert isinstance(even_number_generator_expression, collections.abc.Generator) is True

print(list(even_number_generator_expression))


# (2) Retval of function with "yield"
def even_number_generator_function(limit):
    x = 0
    while x < limit:
        yield x
        x += 2


retval_of_gen_func = even_number_generator_function(upper_bound)
# the following expression prints "generator object even_number_generator_function at ..."
print(retval_of_gen_func)
# the following assertion is True since it is the retval of function with "yield"
assert isinstance(retval_of_gen_func, collections.abc.Generator) is True

print(list(retval_of_gen_func))
