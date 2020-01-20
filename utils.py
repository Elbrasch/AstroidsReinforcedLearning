import datetime
import time
import config

GLOBAL_TICKS = 0
__time_per_frame = datetime.timedelta(seconds=1) / config.fps


def tick_time(last):
    if config.use_ticks:
        global GLOBAL_TICKS
        GLOBAL_TICKS += 1
    else:
        now = datetime.datetime.now()
        delta = now - last
        to_sleep = __time_per_frame - delta
        if to_sleep.total_seconds() > 0:
            time.sleep(to_sleep.total_seconds())
            return datetime.datetime.now()
        else:
            return last + __time_per_frame


def get_now():
    if config.use_ticks:
        return GLOBAL_TICKS
    else:
        return datetime.datetime.now()


def it_is_time(last, delta):
    if config.use_ticks:
        return last + delta.total_seconds() * config.fps <= GLOBAL_TICKS
    else:
        return last + delta <= datetime.datetime.now()
