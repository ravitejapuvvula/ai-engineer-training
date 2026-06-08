import asyncio
import time

def get_time_to_execute(id: str, duration: int):

    print("Task ID name :" , id)
    time.sleep(duration)
    print(f"Task {id} Completed")

async def execute_task(id: str, duration: int):

    print("Task ID name :" , id)
    await asyncio.sleep(duration)
    print(f"{id} Completed")
    return id

def sync_programming():

    start = time.time()

    get_time_to_execute('alpha',2)
    get_time_to_execute('beta',4)
    get_time_to_execute('gamma',5)

    end = time.time()

    print(f"Time to execute :  ", round(end-start))

async def asequential_main():
    start = time.time()

    task1 = asyncio.create_task(execute_task('alpha',2))
    task2 = asyncio.create_task(execute_task('beta',4))
    task3 = asyncio.create_task(execute_task('gamma',5))

    print(await task1, await task2, await task3)
    
    print("Total:", round(time.time() - start, 2), "seconds")

async def gather_main():

    start = time.time()

    task_names = ['alpha','beta','gamma']
    tasks = [execute_task(y,2) for y in task_names]
    results = await asyncio.gather(*tasks)

    print(results, "Total:", round(time.time() - start, 2), "seconds")

# Executing sync and async functions

asyncio.run(asequential_main())
asyncio.run(gather_main())
sync_programming()
