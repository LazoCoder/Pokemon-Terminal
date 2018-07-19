#!/usr/bin/env python3.6
import atexit
import random
import sys

from threading import Thread

def __print_fork(pid, length, delay):
    print(f"Starting slideshow with {length} Pokemons and a delay of {delay} minutes.")
    print(f"Forked process to background with PID {pid}. You can stop it with 'pokemon -c'.")

def __exit_listener():
    raise Exception('TODO: listen for exit')

def __slideshow_worker(filtered, delay, changer_func):
    t = Thread(target=__exit_listener)
    t.start()
    random.shuffle(filtered)
    queque = iter(filtered)
    while t.is_alive():
        next_pkmn = next(queque, None)
        if next_pkmn is None:
            random.shuffle(filtered)
            queque = iter(filtered)
            continue
        changer_func(next_pkmn.get_path())
        t.join(delay * 60)

def start(filtered, delay, changer_func):
    if sys.platform == 'win32':
        import multiprocessing
        p = multiprocessing.Process(target=__slideshow_worker, args=(filtered, delay, changer_func, ), daemon=True)
        p.start()
        __print_fork(p.pid, len(filtered), delay)
        # HACK remove multiprocessing's exit handler to prevent it killing our child.
        atexit.unregister(multiprocessing.util._exit_function)
        sys.exit(0)
    else:
        import os
        pid = os.fork()
    if pid > 0:
        __print_fork(pid, len(filtered), delay)
        sys.exit(0)
    __slideshow_worker(filtered, delay, changer_func)