
def plus_one_generator():
    while True:
        x = yield
        print(x)
        if x is None:
            x = 10
        print(x)
        yield x + 1


it = plus_one_generator()

it.send(None)
print(f'{next(it)}')

print(f'{next(it)}')
it.send(20)
print(f'{next(it)}')
print(f'{next(it)}')

# https://blog.csdn.net/mieleizhi0522/article/details/82142856?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164941604516780357267605%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164941604516780357267605&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-82142856.142^v7^pc_search_result_control_group,157^v4^control&utm_term=yield&spm=1018.2226.3001.4187