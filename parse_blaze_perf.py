import json
import re
import sys
from subprocess import Popen, PIPE
import diskcache

diskCacheFile = "test"
dataPointsKey = "data_points"
params = dict()


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


def load_database():
    return diskcache.Index(diskCacheFile + ".diskCacheIndex")


def prepare_the_db():
    db = load_database()
    if dataPointsKey not in db.cache:
        db.cache[dataPointsKey] = []
    temp_list = [params]
    db.cache[dataPointsKey] = temp_list
    print('cache created')
    db.cache.close()


def read_from_db():
    cd = load_database()
    print(cd.cache[dataPointsKey])


def print_parameters():
    print("=================================")
    print(params)
    print("=================================")


if __name__ == '__main__':
    # run_and_parse_blazemark()
    print("Usage: %s key value ..." % sys.argv[0])

    params.clear()
    with open('params.json') as f:
        params = json.load(f)

    print_parameters()

    prepare_the_db()
    read_from_db()
