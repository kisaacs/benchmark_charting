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


def test_run():
    measurements = list()
    line_count = 0
    with open("outfile") as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            if line_count % 3 == 0:
                perfecto_time.append(line)
            if line_count % 3 == 1:
                obsoleto_time.append(line)
            if line_count % 3 == 2:
                coolio_time.append(line)
            line_count = line_count + 1


def test_run1():
    timeLineParser = re.compile(r'(\d+.\d+)user')
    # print("hello")
    cmd = ["/usr/bin/time", "-f", "'%R'", "ls", "-l"]
    proc = Popen(cmd, stdout=PIPE, universal_newlines=True)
    measure = proc.stdout.readlines()[1]
    print("nani")
    print(measure)
    print("hello")


def test_run2():
    timeLineParser = re.compile(r'(\d+.\d+)user')
    # print("hello")
    RUNS = 3
    program_list = ["./perfecto", "./obosoleto", "./coolio"]
    param_name_list = ["params1", "params2", "params3"]
    params = [[1, 2, 5],
              [4, 13, 55],
              [5, 51, 15]]
    cmd = ["/usr/bin/time", "-f", "'%R'"]
    a_list = []
    t_cmd = []
    measurements = dict()
    for i in range(RUNS):
        a_list.clear()
        for p in range(len(param_name_list)):
            a_list.append(param_name_list[p])
            a_list.append(str(params[p][i]))

        for program in program_list:
            t_cmd.clear()
            t_cmd.extend(cmd)
            t_cmd.append(program)
            t_cmd.extend(a_list)
            proc = Popen(t_cmd, stdout=PIPE, universal_newlines=True)

            measure = proc.stdout.readlines()[0]
            if program not in measurements:
                measurements[program] = list()
            measurements[program].append(measure)


def test_run3():
    # print("hello")
    RUNS = 3
    program_list = ["perfecto", "obosoleto", "coolio"]
    param_name_list = ["params1", "params2", "params3"]
    params_and_measures = dict()
    params_and_measures["params1"] = [1, 2, 5]
    params_and_measures["params2"] = [4, 13, 55]
    params_and_measures["params3"] = [5, 51, 15]

    cmd = ["/usr/bin/time", "-f", "'%R'"]
    a_list = []
    t_cmd = []
    for i in range(RUNS):
        a_list.clear()
        for p in range(len(param_name_list)):
            a_list.append(param_name_list[p])
            a_list.append(str(params_and_measures[param_name_list[p]][i]))

        for program in program_list:
            t_cmd.clear()
            t_cmd.extend(cmd)
            t_cmd.append("./" + program)
            t_cmd.extend(a_list)
            proc = Popen(t_cmd, stdout=PIPE, universal_newlines=True)

            measure = proc.stdout.readlines()[0]
            if program not in params_and_measures:
                params_and_measures[program] = list()
            params_and_measures[program].append(measure)

    target = open('outfiles', 'a')
    target.write(str(params))
    target.close()


def test_run4():
    params_and_measures = eval(open('outfiles', 'r').read())
    print("hello")


def test():
    number_list = range(-5, 5)
    less_than_zero = list(filter(lambda (i, x): x < 0, enumerate(number_list)))
    print(less_than_zero)


if __name__ == '__main__':
    # run_and_parse_blazemark()
    # print("Usage: %s key value ..." % sys.argv[0])
    #
    # params.clear()
    # with open('params.json') as f:
    #     params = json.load(f)
    #
    # print_parameters()
    #
    # prepare_the_db()
    # read_from_db()
    # test_run3()
    # test_run4()
    test()
