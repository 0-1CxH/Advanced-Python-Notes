import asyncio
import random
import time


async def dummy_io_operation():
    sleep_time = random.randint(0, 5)
    time.sleep(sleep_time)
    return sleep_time


async def run_many_dummy_io(n):
    tasks = []
    for i in range(n):
        one_dummy_io = dummy_io_operation()
        tasks.append(one_dummy_io)

    await asyncio.gather(*tasks)

start_time = time.time()
result = asyncio.run(run_many_dummy_io(10))
stop_time = time.time()
print(stop_time-start_time)
print(result)
