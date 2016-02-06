#!/usr/bin/env python3
from subprocess import Popen, PIPE
import click
from queue import Queue, Empty, Full
from threading import Thread, Lock

#lot of refernce from http://www.troyfawkes.com/learn-python-multithreading-queues-basics/
#verbatim from http://stackoverflow.com/questions/3185261/python-threading-and-queues-for-infinite-data-input-stream

#dependency vda-dump from SRA toolkit

class jointRead:
    def __init__(self, inputStream):
        self.readName = inputStream[0]
        self.nt = inputStream[1]
        self.quality = inputStream[3]

def dump_mate(queue,
              threadId,
              mate1,
              mate2,
              mutex):
    while True:
        try:
            readObject = queue.get(block=True, timeout=1)
            midIndex = int(len(readObject.nt)/2)
            mutex.acquire()
            mate1.write(readObject.readName + "/2\n" + readObject.nt[:midIndex] + "\n" + '+'+readObject.readName[1:] + "/2\n" + readObject.quality[:midIndex] + "\n")
            mate2.write(readObject.readName + "/2\n" + readObject.nt[midIndex:] + "\n" + '+'+readObject.readName[1:] + "/2\n" + readObject.quality[midIndex:] + "\n")
            mutex.release()
            queue.task_done()
        except Empty:
            print ("Exiting thread {}".format(threadId))
            break


def fill_queue(queue, filename):
    p = Popen(["vdb-dump", "-f", "fastq", filename], stdout=PIPE, bufsize=1, universal_newlines=True)
    count = 0
    stream = []
    for line in p.stdout:
        count += 1
        stream.append(line.strip())
        if count == 4:
            count = 0
            queue.put(jointRead(stream))
            stream = []
    print ("exiting filling queue")

@click.command()
@click.option('--sra', help='SRA file path. fastq will be in the same path with _1 & _2')
def main(sra):
    readsQueue = Queue(maxsize=0)
    noOfThreads = 2
    mutex = Lock()

    with open(sra+"_1.fq", 'w') as m1, open(sra+"_2.fq", 'w') as m2:
        threads = [Thread(target=dump_mate, args=(readsQueue,i, m1, m2, mutex)) for i in range(noOfThreads)]
        threads.insert(0,Thread(target=fill_queue,args=(readsQueue, sra)))

        for t in threads:
            t.daemon = True
            t.start()

        for t in threads:
            t.join()
    print("Mate creation Done!! Enjoy")
if __name__=="__main__":
    main()
