import hashlib
import re
import sys
import filetofingerprint
import hashedgrams
from fingerprint import Fingerprint
import collections

# Setup the winnowing function by removing all common characters and retrieving the k-gram hashes
def winnow_setup(text, k, w):
    # text to lowercase and remove all non-alphanumerics for text
    text = text.lower()
    # text = re.sub(r'\W+', '', text) this is for plain text
    text = re.sub(r'\s+', '', text)
    # retrieve the k-gram hashes
    hashes = compute_hash(text, k)
    # return the output of the winnow function
    return winnow(w, hashes)

# Algorithm taken from 'Winnowing: Local Algorithms for Document Fingerprinting'
def winnow(w, hashes):
    recorded = {}
    h2 = hashes.copy()
    # create the window of size 4
    h = [sys.maxsize for i in range(0, w)]
    r = 0
    minimum = 0
    global_pos = 0
    # loop through the hashes to find the minimum hash in every window
    for i in range(0, len(hashes)):
        r = (r + 1) % w
        h[r] = h2.pop(0)
        # if the minimum is the current index, check entire window for the minimum
        if minimum == r:
            for ind in scan_left_ind(r, w):
                if h[ind] < h[minimum]:
                    minimum = ind
            recorded = record(recorded, h[minimum], global_pos, w)
        else:  # check if the current index is the new minimum
            if h[r] < h[minimum]:
                minimum = r
                recorded = record(recorded, h[minimum], global_pos, w)
        global_pos += 1
    return recorded

# record the current hash and the its positioning
def record(recorded, minimum, global_pos, w):
    # determine if there is another hash in the same window already
    if global_pos < w and len(recorded) > 0:
        for rec in recorded.copy():
            # if there is, determine the true minimum and record it
            if minimum < rec:
                recorded.pop(rec)
                recorded[minimum] = [global_pos]
    else:
        if minimum in recorded:
            recorded[minimum] = recorded[minimum] + [global_pos]
        else:
            recorded[minimum] = [global_pos]
    return recorded

def scan_left_ind(r, w):
    inds = []
    step = (r - 1) % w
    for i in range(0, w):
        inds.append(step)
        step = (step - 1 + w) % w
    return inds

# compute the k-gram hashes through a rolling hash function
def compute_hash(s, k):
    # setup the compute hash function
    ints = compute_ints(s)
    p = 31
    m = 10 ** 9 + 9
    # compute the p_pow values
    p_pow = compute_p_pow(k, p, m)
    final_pow = p_pow[k - 1]
    # compute the initial hash value
    hashes = [sum([num * power % m for num, power in zip(ints[0:k], p_pow)])]
    for i in range(0, len(s) - k):
        # compute the next hash value through the previous one
        hashes.append(int((hashes[i] - ints[i]) / p % m + (ints[k + i] * final_pow) % m))
    return hashes

# return the modified int value for the characters in the text
def compute_ints(s):
    ints = []
    for ch in s:
        ints.append(ord(ch) - ord('a') + 1)
    return ints

# compute the p_pow values
def compute_p_pow(k, p, m):
    p_pow = [1]
    for i in range(1, k):
        p_pow.append((p_pow[i-1] * p) % m)
    return p_pow

def get_substring(pos, k, text):
    i = 0
    spaces_pos = []
    newlines_pos = []
    for ch in text:
        if ch == ' ':
            spaces_pos.append(i)
        if ch == '\n':
            newlines_pos.append(i)
        i += 1
    for space_pos in spaces_pos + newlines_pos:
        if space_pos <= pos:
            pos += 1
        if pos < space_pos <= pos + k:
            k += 1
    return text[pos:pos+k]

def compare_files(student_file_loc, base_file_loc, k, w, boilerplate_file_loc):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = winnow_setup(student_txt, k, w)
    num_std_fps = 0
    for val in student_fingerprints.values():
        for _ in val:
            num_std_fps += 1
    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = winnow_setup(base_txt, k, w)
    boilerplate_fingerprints = {}
    if (boilerplate_file_loc != ""):
        boilerplate_file = open(boilerplate_file_loc, "r")
        boilerplate_txt = boilerplate_file.read()
        boilerplate_fingerprints = winnow_setup(boilerplate_txt, k, w)

    common = []
    num_common_fps = 0
    for fp in list(student_fingerprints.keys()):
        if fp in list(boilerplate_fingerprints.keys()):
            continue
        elif fp in list(base_fingerprints.keys()):
            common.append(fp)
            for _ in student_fingerprints[fp]:
                num_common_fps += 1

    similarity = num_common_fps / num_std_fps
    plagiarized = "plagiarized" if similarity >= 0.25 else "not plagiarized"
    if (boilerplate_file_loc == ""):
        print("No boilerplate being used. ")
    else:
        print("Boilerplate file " + boilerplate_file_loc + " being used.")
    print("The student file is {:.2%} similar to the base file.\n".format(similarity) + "" 
          "The student file was likely {}.".format(plagiarized))
    print("It's similar by", num_common_fps)
    print("")

def get_common_fingerprints(student_file_loc, base_file_loc, k, w, boilerplate_file_loc):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = winnow_setup(student_txt, k, w)

    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = winnow_setup(base_txt, k, w)

    boilerplate_fingerprints = {}
    if (boilerplate_file_loc != ""):
        boilerplate_file = open(boilerplate_file_loc, "r")
        boilerplate_txt = boilerplate_file.read()
        boilerplate_fingerprints = winnow_setup(boilerplate_txt, k, w)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(boilerplate_fingerprints.keys()):
            continue
        elif fp in list(base_fingerprints.keys()):
            substr = get_substring(student_fingerprints[fp][0], k, student_txt)
            # for each position add an object
            for pos in student_fingerprints[fp]:
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)
    return student_common, base_common

# Wraps a list of filenames into filetofingerprint objects
def wrap_filenames(filenames):
    files = []
    filecount = 0
    for fnames in filenames:
        file = filetofingerprint.filetofingerprint(fnames, filecount, {}, {})
        files.append(file)
        filecount += 1
    return files

# Takes in a list of multiple filenames, performs the comparison function and
# returns an array of filetofingerprint objects
# this is done by getting all the documents and putting all the hashes into a large
# dictionary containing the all the fingerprints with which files + fingerprints correspond to them

"""def compare_multiple_documents(filenames, k, w, boilerplate):
    filetxts = {}
    files = wrap_filenames(filenames)
    allfingerprints = collections.defaultdict(dict)
    if len(boilerplate) == 0:
        for file in files:
            f = open(file.filename, "r")
            txt = f.read()
            filetxts[file.filename] = txt
            file.fingerprints = winnow_setup(txt, k, w)
            for fp in list(file.fingerprints.keys()):
                substr = get_substring(file.fingerprints[fp][0], k, txt)
                for pos in file.fingerprints[fp]:
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file.filename].append(newfp)
            old version of this part
            for fp in list(file.fingerprints.keys()):
                if fp in list(allfingerprints.keys()):
                    allfingerprints[fp].append({file.filename: file.fingerprints[fp]})
                else:
                    allfingerprints[fp] = [{file.filename: file.fingerprints[fp]}]
    else:
        bpfingerprints = {}
        for bpfile in boilerplate:
            bp = open(bpfile, "r")
            bptxt = bp.read()
            if len(bpfingerprints) == 0:
                bpfingerprints = winnow_setup(bptxt, k, w)
            else:
                bpfingerprints.update(winnow_setup(bptxt, k, w))
        for file in files:
            f = open(file.filename, "r")
            txt = f.read()
            filetxts[file.filename] = txt
            file.fingerprints = winnow_setup(txt, k, w)
            for fp in list(file.fingerprints.keys()):
                if fp in bpfingerprints: #remove fp here?
                    continue
                substr = get_substring(file.fingerprints[fp][0], k, txt)
                for pos in file.fingerprints[fp]:
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file.filename].append(newfp)
    return allfingerprints
"""
def compare_multiple_documents(filenames, k, w, boilerplate):
    filetxts = {}
    files = wrap_filenames(filenames)
    allfingerprints = collections.defaultdict(dict)
    bpfingerprints = {}
    for bpfile in boilerplate:
        bp = open(bpfile, "r")
        bptxt = bp.read()
        if len(bpfingerprints) == 0:
            bpfingerprints = winnow_setup(bptxt, k, w)
        else:
            bpfingerprints.update(winnow_setup(bptxt, k, w))

    #put all fingerprints into large fp dictionary
    for file in files:
        f = open(file.filename, "r")
        txt = f.read()
        filetxts[file.filename] = txt
        file.fingerprints = winnow_setup(txt, k, w)
        for fp in list(file.fingerprints.keys()):
            if fp in bpfingerprints: #remove fp here?
                continue
            allfingerprints[fp][file] = []
            #substr = get_substring(file.fingerprints[fp][0], k, txt) i moved this down into line 272 + replaced it with pos because I think each of the substrings can be different
            #although the fp is the same, it may (or may not) also be a problem at line 176
            for pos in file.fingerprints[fp]:
                substr = get_substring(pos, k, txt)
                newfp = Fingerprint(fp, pos, substr)
                allfingerprints[fp][file].append(newfp)

    #fill the file's similarto dictionary with the necessary fingerprints
    for file in files:
        for fp in list(file.fingerprints.keys()):
            commonfiles = allfingerprints.get(fp)
            if (commonfiles == None):
                continue
            elif len(commonfiles) > 1:
                for commonfile in commonfiles:
                    if file != commonfile: #put it into similarto if it's a different file
                        if commonfile in file.similarto:
                            file.similarto[commonfile].append((allfingerprints[fp][file], allfingerprints[fp][commonfile]))
                        else:
                            file.similarto[commonfile] = [(allfingerprints[fp][file], allfingerprints[fp][commonfile])]
                        """old version of this part
                        if similarfilename in file.similarto:
                            file.similarto[similarfilename].append({file.fingerprints[fp]: list(fpdata.values())[0]})
                        else:
                            file.similarto[similarfilename] = [{file.fingerprints[fp]: list(fpdata.values())[0]}]"""
    return files

#not finished
def get_most_important_matches(f1_fingerprints, f2_fingerprints):
    distance = 30
    blockcounter = 0
    most_important_match_locations = [{}]
    f1_blocks = [{}]
    for fp in range(len(f1_fingerprints) - 1):
        if (f1_fingerprints[fp].global_pos + len(fp.substring) + distance) >= (f1_fingerprints[fp+ 1]).global_pos:
            if blockcounter == 0:
                start =  f1_fingerprints[fp]
                #f1_block.append({f1_fingerprints[fp]:-1})
            blockcounter += 1
        else:
            if blockcounter >= 5:
                end = f1_fingerprints[fp]
                f1_blocks.append[{start:end}]
            blockcounter = 0

# Printing debug results for prototype, accepts filetofingerprint object
def print_prototype_test(files, boilerplate):
    print("Testing files ", end="")
    for i in range(len(files)):
        if i != (len(files) - 1):
            print(files[i].filename + ", ", end="")
        else:
            print(files[i].filename + ".")
    print("")
    if len(boilerplate) == 0:
        print("No boilerplate.", end = "")
    else:
        print("The boilerplate is: ", end = "")
        for i in range(len(boilerplate)):
            if i != (len(boilerplate) - 1):
                print(boilerplate[i] + ", ", end="")
            else:
                print(boilerplate[i] + ".", end = "")
    print("")
    print("")
    for file in files:
        if (len(file.similarto) == 0):
            print("File " + str(file.fileid) + ", " + file.filename + ", is similar to nothing.")
            continue
        print("File " + str(file.fileid) + ", " + file.filename + ", is similar to ", end="")
        for sim in file.similarto:
            print(sim.filename, "by", len(file.similarto[sim]), "fingerprints")
            print("They're similar at (loc(position), loc(position) for each of the 2 documents):")
            l = 0  # this l will probably get taken out, it's only to keep too many results from printing
            fpcount = 0
            for simfps in file.similarto[sim]:
                if (l == 9):
                    print("etc....")
                    #break
                for fps in simfps[0]:
                    substr = fps.substring.split('\n')
                    substr = "\\n".join(substr)
                    print(str(fps.global_pos) + "(" + substr + ")", end = " ")
                print(", ", end = "")
                for fps in simfps[1]:
                    substr = fps.substring.split('\n')
                    substr = "\\n".join(substr)
                    print(str(fps.global_pos) + "(" + substr + ")", end = " ")
                print("")
                l += 1
            print(sim.filename, "by", len(file.similarto[sim]), "fingerprints")


def main():
    # songtest1 + songtest2 are songs with lyrics written slightly differently/remixed so could be considered copyright
    # texttest1 is an announcement from the class, texttest2 is a description of a game from a store page
    # c++ test is a file from programming 2 project 2, java test is from
    # programming 1 project 1 (neither of these 2 copied)
    print("Single document tests:")
    get_common_fingerprints("songtest1.txt", "songtest2.txt", 5, 4, "")
    compare_files("songtest1.txt", "songtest2.txt", 5, 4, "")
    compare_files("songtest1.txt", "songtest2.txt", 5, 4, "songtest1.txt")
    compare_files("songtest1.txt", "texttest1.txt", 5, 4, "")
    compare_files("javatest1.java", "c++test1.cpp", 5, 4, "")
    compare_files("texttest1.txt", "texttest2.txt", 5, 4, "")
    print("")

    print("Multi-document tests: ")
    multidocumenttest = ["songtest1.txt", "songtest2.txt"]
    print_prototype_test(compare_multiple_documents(multidocumenttest, 10, 4, []), [])
    print("")

    print("Boilerplate test: ")
    boilerplate = ["songtest1.txt", "texttest2.txt"]
    boilerplatetest = ["songtest1.txt", "songtest2.txt","c++test1.cpp"]
    print_prototype_test(compare_multiple_documents(boilerplatetest, 10, 4, boilerplate), boilerplate)


if __name__ == "__main__":
    main()
