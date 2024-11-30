import time
import multiprocessing
from collections import defaultdict


start_time = time.time()

keywords = ['bilders', 'raciality']


def search_files(files):
    results = defaultdict(list)
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file)
    return results


def divide_files(files, num_processes):
    chunk_size = len(files) // num_processes
    chunks = [files[i:i+chunk_size] for i in range(0, len(files), chunk_size)]
    return chunks


def process_function(files, queue):
    results = search_files(files)
    queue.put(results)


if __name__ == '__main__':
    files = ['data/file_{}.txt'.format(i) for i in range(1, 1001)]
    num_processes = 4
    file_chunks = divide_files(files, num_processes)

    queue = multiprocessing.Queue()
    processes = []

    for chunk in file_chunks:
        process = multiprocessing.Process(target=process_function, args=(chunk, queue))
        process.start()
        processes.append(process)

    results = defaultdict(list)

    for process in processes:
        process.join()

    while not queue.empty():
        result = queue.get()
        for keyword, file_list in result.items():
            results[keyword].extend(file_list)

    print(dict(results))

    end_time = time.time() - start_time
    print('Time taken:', end_time)
