#!/usr/bin/env python3.6
import os
import random
import sys
import time

from threading import Thread

def __print_fork(pid, length, delay):
    print(f"Starting slideshow with {length} Pokemons and a delay of {delay} minutes.")
    print(f"Forked process to background with PID {pid}. You can stop it with 'pokemon -c'.")

def __exit_listener():
    raise Exception('TODO')

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
    if os.name == 'nt':
        raise Exception('TODO')
    else:
        pid = os.fork()
    if pid > 0:
        __print_fork(pid, len(filtered), delay)
        sys.exit(0)
    __slideshow_worker(filtered, delay, changer_func)