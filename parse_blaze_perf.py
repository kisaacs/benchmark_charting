import re
from subprocess import Popen, PIPE
import diskcache


def run_and_parse_blazemark():
    stepsLineParser = re.compile(r'\s+N=(\d+),\s+steps=\d+')
    blazeLineParser = re.compile(r'\s+Blaze\s+=\s+\d+\s+\((\d*\.?\d*)\)')

    # print("hello")
    cmd = ["/home/sayefsakin/blaze-3.8/blazemark/bin/complex1", "-only-blaze"]
    # cmd = ["ls", "-la"]
    proc = Popen(cmd, stdout=PIPE, universal_newlines=True)
    steps = 0
    print('Steps   Time(sec)')
    for line in proc.stdout.readlines():
        # print(line, end='')
        stepsLineMatch = stepsLineParser.match(line)
        blazeLineMatch = blazeLineParser.match(line)
        if stepsLineMatch is not None:
            steps = int(stepsLineMatch.group(1))
        elif blazeLineMatch is not None:
            tmf = blazeLineMatch.group(1)
            print('{:5d}'.format(steps), ' ', tmf)


def prepare_the_db():
    cc = diskcache.Index("test.diskCacheIndex")
    cc.cache['harami'] = 'nai'
    cc.cache['vaivai'] = 10
    cc.cache['nd'] = dict()
    cd = dict()
    cd['timesec'] = 100
    cd['speed'] = 23423
    cc.cache['nd'] = cd
    print('cache created')
    cc.cache.close()


def read_from_db():
    cd = diskcache.Index("test.diskCacheIndex")
    print(cd.cache['nd'])


if __name__ == '__main__':
    # run_and_parse_blazemark()

    prepare_the_db()
    read_from_db()
