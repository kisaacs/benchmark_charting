import re
import sys
from subprocess import Popen, PIPE
import diskcache

diskCacheFile = "test"
dataPointsKey = "data_points"

noOfThreads = 8
matrixSize = 200
blockSize = 4
chunkSize = 50

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


def create_dictionary_of_data_points():
    return {
        'threads': noOfThreads,
        'matrix': matrixSize,
        'block': blockSize,
        'chunk': chunkSize
    }


def prepare_the_db():
    db = load_database()
    if dataPointsKey not in db.cache:
        db.cache[dataPointsKey] = []
    temp_list = [create_dictionary_of_data_points()]
    db.cache[dataPointsKey] = temp_list
    print('cache created')
    db.cache.close()


def read_from_db():
    cd = load_database()
    print(cd.cache[dataPointsKey])


def print_parameters():
    print("=================================")
    print("No of threads: " + str(noOfThreads))
    print("Matrix size: " + str(matrixSize))
    print("block size: " + str(blockSize))
    print("Chunk size or num of blocks: " + str(chunkSize))
    print("=================================")


if __name__ == '__main__':
    # run_and_parse_blazemark()
    print("Usage: %s no_of_threads matrix_size block_size chunk_size" % sys.argv[0])
    if len(sys.argv) > 1:
        noOfThreads = int(sys.argv[1])
    if len(sys.argv) > 2:
        matrixSize = int(sys.argv[2])
    if len(sys.argv) > 3:
        blockSize = int(sys.argv[3])
    if len(sys.argv) > 4:
        chunkSize = int(sys.argv[4])

    print_parameters()

    prepare_the_db()
    read_from_db()
