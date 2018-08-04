import atexit
import multiprocessing
import random
import sys
from threading import Thread

from .platform import PlatformNamedEvent


def __print_fork(pid, length, delay):
    print(f"Starting slideshow with {length} Pokemons and a delay of {delay} minutes.")
    print(f"Forked process to background with PID {pid}.")
    print("You can stop it with 'pokemon -c'. (add '-w' if this is a wallpaper slideshow)")


def __event_listener(event):
    event.wait()


def __get_listener_thread(event):
    t = Thread(target=__event_listener, args=(event,), daemon=True)
    t.start()
    return t


def __slideshow_worker(filtered, delay, changer_func, event_name):
    with PlatformNamedEvent(event_name) as e:
        t = __get_listener_thread(e)
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


def start(filtered, delay, changer_func, event_name):
    p = multiprocessing.Process(target=__slideshow_worker, args=(filtered, delay, changer_func, event_name,),
                                daemon=True)
    p.start()
    __print_fork(p.pid, len(filtered), delay)
    # HACK remove multiprocessing's exit handler to prevent it killing our child.
    atexit.unregister(multiprocessing.util._exit_function)
    sys.exit(0)


def stop(event_name):
    with PlatformNamedEvent(event_name) as e:
        e.signal()
