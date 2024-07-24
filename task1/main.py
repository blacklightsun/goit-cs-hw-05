import sys
import time
import asyncio
from aiopathlib import AsyncPath
from aioshutil import copy2

async def copy_files(path_to, child):
    path_ext = path_to / child.suffix[1:]
    await path_ext.mkdir(parents=True, exist_ok=True)
    await copy2(child, path_ext)

async def read_folder(folder_from, folder_to='dist') -> None:

    path_to = AsyncPath(folder_to)
    path_from = AsyncPath(folder_from)


    try:
        for child in path_from.iterdir():
            if await child.is_dir():
                await read_folder(child, path_to)
            elif await child.is_file():
                await copy_files(path_to, child)

    except OSError as e:
        print("Помилка операцій з файлом чи папкою")
        with open('log.txt', 'a') as log:
            log.write(f'There is problem with {child}. Error message is:\n{e}\n')


try:
    start_time = time.time()
    asyncio.run(read_folder(*sys.argv[1:3]))
except:
    print('\nПомилка! Не вказаний шлях до папки з файлами. Спробуйте ще раз.\n')

print('час виконання:', time.time() - start_time)