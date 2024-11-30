import time
import threading
from collections import defaultdict


start_time = time.time()

keywords = ['this', 'down', 'not']


def search_files(files):
    results = defaultdict(list)
    for file in files:
        with open(file, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file)
    return results


def divide_files(files, num_threads):
    chunk_size = len(files) // num_threads
    chunks = [files[i:i+chunk_size] for i in range(0, len(files), chunk_size)]
    return chunks


def thread_function(files, results):
    thread_results = search_files(files)
    for keyword, file_list in thread_results.items():
        results[keyword].extend(file_list)


files = ['data/file_{}.txt'.format(i) for i in range(1, 1001)]
num_threads = 4
file_chunks = divide_files(files, num_threads)

results = defaultdict(list)

threads = []
for chunk in file_chunks:
    thread = threading.Thread(target=thread_function, args=(chunk, results))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(dict(results))

end_time = time.time() - start_time
print('Time taken:', end_time)
