from functools import wraps
import logging
import time


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, errors=(Exception, )):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param errors: обрабатываемые ошибки
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempt_number: int = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except errors:
                    attempt_number += 1
                    logging.exception(f"Attempt {attempt_number} failed with exception.")

                    sleep_time: int = start_sleep_time * factor ** attempt_number
                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time

                    time.sleep(sleep_time)

        return inner

    return func_wrapper
