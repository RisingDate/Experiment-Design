import time
from datetime import datetime


def fun1(data):
    print(data)
    time.sleep(2)


def run():
    cnt = 0
    while True:
        cnt += 1
        fun1(cnt)


if __name__ == '__main__':
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    run()
