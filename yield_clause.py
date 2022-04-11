# (1) Retval of "yield"
# the default retval of "yield" is None
# use send method of generator to change the retval of "yield"

def cipher_generator(mod: int):
    offset = 0
    while True:
        plaintext = yield offset
        assert isinstance(plaintext, int)
        if not plaintext:
            continue
        else:
            print(f'cipher={plaintext + offset}')
        offset = (offset + 1) % mod


g = cipher_generator(5)
print(f'{g.send(None)=}')  # must send None to a just-started generator
# when sending None to the generator, the generator started and goes to the first "yield"
# (actually, call g.send(None) is equal to call g.__next__())
# in this case, go to  "yield offset", and it returns the offset 0
# Note that: "plaintext" is not assigned with value for now since the generator pauses at the "yield" part

print(f'{g.send(42)=}')
# 42 is sent to the generator, and received by the "yield",
# then "plaintext = yield" assign 42 to "plaintext"
# the loop goes until next "yield" is encountered

for pt in [4, 7, 23, 48, 15]:
    g.send(pt)


# (2) "yield from"
# Replace recursive: yield from an iterator and send back to caller
# Proxy/delegating generator: yield from a child generator, generate and send back to caller

# (2.1) Replace recursive
# now, there is a task to make this nested iterator flattened
nested_iter = [[1, [2, 3], [4, [5]]],[[6, [7, 8], [9, [10]]]]]


# if a general function is deployed, it would be like:
def flatten_classical(it):
    ret = []

    def flatten_classical_sub_function(main_iter):
        if isinstance(main_iter, int):
            ret.append(main_iter)
            return
        for sub_iter in main_iter:
            flatten_classical_sub_function(sub_iter)

    flatten_classical_sub_function(it)
    return ret


print(flatten_classical(nested_iter))


# use "yield from" to replace the recursive part above
def flatten(it):
    if isinstance(it, int):
        yield it
    else:
        for sub_it in it:
            yield from flatten(sub_it)


print([_ for _ in flatten(nested_iter)])

# in fact, recursive like BFS/DFS can use "yield from"


# (2.2) Proxy/delegating generator
# Ref: https://www.cnblogs.com/wongbingming/p/9085268.html

nums = [10, 20, 30, 40, 50]


def average_gen():
    total = 0
    count = 0
    while True:
        recv = yield total/count if count else 0
        if not recv:
            break
        total += recv
        count += 1
    return count


def average_proxy_gen():
    while True:
        ret = yield from average_gen()
        print(f'{ret=}')


ave = average_proxy_gen()
assert ave.send(None) == 0  # send a None to proxy and make it run to "yield from average_gen()"
# now average_gen() starts and runs to "yield total/count if count else 0", so a 0 is generated
for num in nums:
    print(f'{ave.send(num)=}')  # send current num to average_gen() THROUGH proxy,
    # the generated average is also send back THROUGH proxy
ave.send(None)  # send a None to stop average_gen(), it "return count" to proxy,
# and received by "ret = yield", now "ret" is assigned with the retval ("count" in average_gen())


# TODO: ----APPENDIX---------------------------------------
# asyncio, yield from
