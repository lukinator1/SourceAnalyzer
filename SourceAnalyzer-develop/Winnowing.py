import hashlib
import re
import sys
import filetofingerprint

def winnow_setup(text, k, w):
    text = text.lower()
    text = re.sub(r'\W+', '', text)
    grams = []
    for i in range(0, len(text)-k+1):
        grams.append(text[i:i+k])
    hashes = []
    for gram in grams:
        hashes.append(int(hashlib.md5(gram.encode('UTF-8')).hexdigest(), 16))
    return winnow(w, hashes)

# Algorithm taken from 'Winnowing: Local Algorithms for Document Fingerprinting'
def winnow(w, hashes):
    recorded = {}
    h2 = hashes.copy()
    h = [sys.maxsize for i in range(0, w)]
    r = 0 #right end of window
    minimum = 0 #index of minimum hash
    global_pos = 0
    for i in range(0, len(hashes)-1):
        r = (r + 1) % w
        h[r] = h2.pop(0)
        if minimum == r:
            for ind in scan_left_ind(r, w):
                if h[ind] < h[minimum]:
                    minimum = ind
            recorded = record(recorded, h[minimum], global_pos, w)
        else:
            if h[r] < h[minimum]:
                minimum = r
                recorded = record(recorded, h[minimum], global_pos, w)
        global_pos += 1
    return recorded

def record(recorded, minimum, global_pos, w):
    if global_pos < w and len(recorded) > 0:
        for rec in recorded:
            if minimum <= rec:
                recorded.pop(rec)
                recorded[minimum] = global_pos
    else:
        recorded[minimum] = global_pos
    return recorded

def scan_left_ind(r, w):
    inds = []
    step = (r - 1) % w
    for i in range(0,w):
        inds.append(step)
        step = (step - 1 + w) % w
    return inds

def compare_documents(file1, file2):
    f = open(file1, "r")
    txt = f.read()
    fingerprints1 = winnow_setup(txt, 10, 4)

    f2 = open(file2, "r")
    txt2 = f2.read()
    fingerprints2 = winnow_setup(txt2, 10, 4)

    common = []
    for fp in list(fingerprints1.keys()):
        if fp in list(fingerprints2.keys()):
            common.append(fp)
    print("The documents " + file1 + " and " + file2 + "have %d fingerprint(s) in common." % len(common))

#Wraps a list of filenames into filetofingerprint objects
def wrap_filenames(filenames):
    files = []
    filecount = 0
    for fnames in filenames:
        file = filetofingerprint.filetofingerprint(fnames, filecount, [], {})
        files.append(file)
        filecount += 1
    return files

#Takes in a list of multiple filenames, performs the comparison function and
#returns an array of filetofingerprint objects
def compare_multiple_documents(filenames, k, w):
    files = wrap_filenames(filenames)
    allfingerprints = {}
    for file in files:
        f = open(file.filename, "r")
        txt = f.read()
        file.fingerprints = winnow_setup(txt, k, k)
        for fp in list(file.fingerprints.keys()):
            if fp in list(allfingerprints.keys()):
                allfingerprints[fp].append({file.filename:file.fingerprints[fp]})
            else:
                allfingerprints[fp] = [{file.filename:file.fingerprints[fp]}]

    for file in files:
        for fp in list(file.fingerprints.keys()):
            if len(allfingerprints[fp]) > 1:
                for fpdata in allfingerprints[fp]:
                    if list(fpdata.keys())[0] != file.filename:
                        if list(fpdata.keys())[0] in file.similarto:
                            file.similarto[list(fpdata.keys())[0]].append({file.fingerprints[fp]:list(fpdata.values())[0]})
                        else:
                            file.similarto[list(fpdata.keys())[0]] = [{file.fingerprints[fp]:list(fpdata.values())[0]}]
    return files

#Printing debug results for prototype, accepts filetofingerprint object
def print_prototype_test(files):
    print("Testing files ", end = "")
    for i in range(len(files)):
        if i != (len(files) - 1):
            print(files[i].filename + ", ", end="")
        else:
            print(files[i].filename)
    print("")
    for file in files:
        if (len(file.similarto) == 0):
            print("File " + str(file.fileid) + ", " + file.filename + ", is similar to nothing.")
            continue
        print("File " + str(file.fileid) + ", " + file.filename + ", is similar to ", end = "")
        for sim in file.similarto:
            print(sim, "by", len(file.similarto[sim]), "fingerprints")
            print("The locations they're similar to are (by original, similar document): [assuming the winnowing function returns a dictionary with file location as the value]")
            i = 0 #this i will probably get taken out, it's only to keep too many results from printing
            for simfps in file.similarto[sim]:
                if (i == 9):
                    print("etc....")
                    break
                print(str(list(simfps.keys())[0]) + ", " + str(list(simfps.values())[0]))
                i += 1

def main():
    #songtest1 + songtest2 are songs with lyrics written slightly differently/remixed so could be considered copyright
    #texttest1 is an announcement from the class, c++ test is a file from programming 2 project 2, java test is from
    #programming 1 project 1 (neither of these 2 copied)
    print("Single document tests:")
    compare_documents("songtest1.txt", "songtest2.txt")
    compare_documents("songtest1.txt", "texttest1.txt")
    compare_documents("songtest1.txt", "c++test1.cpp")
    compare_documents("songtest2.txt", "texttest1.txt")
    compare_documents("songtest2.txt", "c++test1.cpp")
    compare_documents("texttest1.txt", "c++test1.cpp")
    print("")

    print("Multi-document tests: ")
    multidocumenttest = ["songtest1.txt", "songtest2.txt", "texttest1.txt", "c++test1.cpp", "javatest1.java"]
    print_prototype_test(compare_multiple_documents(multidocumenttest, 10, 4))
    
if __name__ == "__main__":
    main()
