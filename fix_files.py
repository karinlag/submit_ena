import sys, os, os.path

def createlinklist(filedirectory, newlocation, outputfile):
    filelist = []
    for infile in os.listdir(filedirectory):
        if infile.endswith(".gz"):
            filelist.append(os.path.join(filedirectory, infile))

    correctnames = []
    for gzfile in filelist:
        # find if R1 or R2:
        readtype = "R1"
        if "_R2_" in gzfile: readtype = "R2"
        justfilename = os.path.basename(gzfile)
        truncated = justfilename.split("_" + readtype + "_")[0]
        goodname = truncated + "." + readtype + ".fastq.gz"
        correctnames.append((gzfile,goodname))

    symlinkfile = open(outputfile, "w")
    for filepair in correctnames:
        command = "ln -s " + filepair[0] + " " + os.path.join(newlocation, filepair[1]) + "\n"
        symlinkfile.write(command)
    symlinkfile.close()



if __name__=="__main__":
    filedirectory = sys.argv[1]
    newlocation = sys.argv[2]
    outputfile = sys.argv[3]
    createlinklist(filedirectory, newlocation, outputfile)
