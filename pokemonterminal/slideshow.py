import atexit
import multiprocessing
import random
import sys

from .platform import PlatformNamedEvent

def __print_fork(pid, length, delay):
    print(f"Starting slideshow with {length} Pokemons and a delay of {delay} minutes.")
    print(f"Forked process to background with PID {pid}.")
    print("You can stop it with 'pokemon -c'. (add '-w' if this is a wallpaper slideshow)")

def __mac_exit_listener(event):
    event.wait()

def __get_sleeper_and_listener(event):
    if sys.platform == 'darwin':
        from threading import Thread
        t = Thread(target=__mac_exit_listener, args=(event, ))
        t.start()
        sleeper = lambda delay: t.join(delay)
        listener = lambda: t.is_alive()
    else:
        import time
        sleeper = lambda delay: event.wait(delay)
        listener = lambda: not event.is_set()

    return sleeper, listener

def __slideshow_worker(filtered, delay, changer_func, event_name):
    with PlatformNamedEvent(event_name) as e:
        sleeper, listener = __get_sleeper_and_listener(e)
        random.shuffle(filtered)
        queque = iter(filtered)
        while listener():
            next_pkmn = next(queque, None)
            if next_pkmn is None:
                random.shuffle(filtered)
                queque = iter(filtered)
                continue
            changer_func(next_pkmn.get_path())
            sleeper(delay * 60)

def start(filtered, delay, changer_func, event_name):
    p = multiprocessing.Process(target=__slideshow_worker, args=(filtered, delay, changer_func, event_name, ), daemon=True)
    p.start()
    __print_fork(p.pid, len(filtered), delay)
    # HACK remove multiprocessing's exit handler to prevent it killing our child.
    atexit.unregister(multiprocessing.util._exit_function)
    sys.exit(0)

def stop(event_name):
    with PlatformNamedEvent(event_name) as e:
        e.set()
