
# itertools (sug36)

# (1) enumerate
import itertools
from itertools import zip_longest

some_list = ["address", "base64", "cron"]
# when iterating through an iterator, the C-style code is:
for ind in range(len(some_list)):
    print(ind, some_list[ind])
# the pythonic code is using enumerate:
for ind, val in enumerate(some_list):
    print(ind, val)


# (2) zip / zip_longest
other_list = ["directory", "expression", "feature"]
# when iterating through two iterators, the C-style code is:
for ind in range(len(some_list)):
    print(some_list[ind], other_list[ind])
# the pythonic code is using zip
for elem1, elem2 in zip(some_list, other_list):
    print(elem1, elem2)

# if the two iterators are not the same length, the zip stops when the shorter one ends
longer_list = ["generation", "host", "ingestion", "junction"]
for elem1, elem2 in zip(some_list, longer_list):
    print(elem1, elem2)
# use zip_longest to iterate over the longer iterator, the vacant element are filled with given "fillvalue"
for elem1, elem2 in zip_longest(some_list, longer_list, fillvalue='NULL'):
    print(elem1, elem2)


# (3) "itertools"
# itertools provides many tools for pythonic iterating
# do not use for...extend... to concat iterators, use itertools.chain:
for _ in itertools.chain([1,2,3], [4,5,6]):
    print(_)


