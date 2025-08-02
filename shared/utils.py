import datetime

def time_in_window(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.datetime.now().time()
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time
