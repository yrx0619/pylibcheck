# /usr/bin/python
# coding:utf8

import os
import threading
from Queue import Queue
import time
import argparse
import imp
import re

libQueue = Queue()


class Source(object):
    """
    This is source code class.
    """
    srcDir = ""
    outDir = ""

    def __init__(self, srcdir, outdir):
        super(Source, self).__init__()
        self.srcDir = srcdir
        self.outDir = outdir

    def _get_pyfile_list(self):
        fileList = []
        for parent, dirnames, filenames in os.walk(self.srcDir):
            for filename in filenames:
                absFilename = os.path.join(parent, filename)
                if absFilename.endswith(".py"):
                    fileList.append(absFilename)
        print fileList
        return fileList

    def analysis_pyfile(self, filename):
        libList = []
        with open(filename) as fd:
            # time.sleep(10)
            for line in fd.readlines():
                if line.startswith("import"):
                    lib = line.split()[1]
		    if "," in lib:
			libList = lib.split(",")
		    else:
			libList.append(lib)
		    for lib in libList:
			lib = re.sub('\s','',lib) 
		    	if "." in lib:
			    lib = lib.split(".")[0]
                    	libQueue.put(lib)
                elif line.startswith("from"):
                    lib = line.split()[1]
		    if "." in lib:
			lib = lib.split(".")[0]
                        libQueue.put(lib)

    def gen_requirement_file(self, liblist):
        with open(self.outDir + '/' + "requirement.txt", 'w') as fd:
            for lib in liblist:
                fd.write(lib+"\n")

    def _is_lib_in_local(self, lib, filelist):
        for f in filelist:
            if lib in f:
                return True
        return False

    def run(self):
        libList = []
        fileList = self._get_pyfile_list()
        workList = []
        # 每个文件一个线程进行查找导入的库文件。
        for i in range(len(fileList)-1):
            worker = threading.Thread(target=self.analysis_pyfile,
                                      args=(fileList[i],))
            workList.append(worker)
            worker.setDaemon(True)
            worker.start()

        for worker in workList:
            worker.join()

        while not libQueue.empty():
            lib = libQueue.get()
            if lib not in libList and not self._is_lib_in_local(lib, fileList):
                try:
                    imp.find_module(lib)
                except ImportError, e:
                    libList.append(lib)

        self.gen_requirement_file(libList)


def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default=os.getcwd(),
                        help="The path of source code", dest="dir")
    parser.add_argument("-o", "--output", default=os.getcwd(),
                        help="output path for requirement.txt", dest="output")

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = command_line()
    print args
    src = Source(args.dir, args.output)
    src.run()

