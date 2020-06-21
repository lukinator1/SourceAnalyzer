import hashlib
import re
import sys
import filetofingerprint
#import hashedgrams
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

#the boilerplate argument will make it so that fingerprints from that file are ignored
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

#the boilerplate argument will make it so that fingerprints from that file are ignored
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
            # should this be moved ino the 2 loops below as substr = get_substring(pos, k, student/base_txt)? from what it looks like
            # 2 of the same hashes can have slightly different substrings
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

# Takes in a list of multiple filenames, performs the comparison function and
# returns an array of filetofingerprint objects
# this is done by getting all the documents and putting all the hashes into a large
# dictionary containing the all the fingerprints with which files + fingerprints correspond to them
# the boilerplate argument takes in a list of boilerplate filenames, which is something the files
# will be allowed to be similar to/copy from
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
    if len(boilerplate) == 0:
        for file in files:
            f = open(file.filename, "r")
            txt = f.read()
            filetxts[file.filename] = txt
            file.fingerprintssetup = winnow_setup(txt, k, w)
            for fp in list(file.fingerprintssetup.keys()):
                allfingerprints[fp][file] = []
                #inconsistent with how it's done in line 178 but i think this may be the way you have to do it
                for pos in file.fingerprintssetup[fp]:
                    substr = get_substring(pos, k, txt)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)
    else:
        for file in files:
            f = open(file.filename, "r")
            txt = f.read()
            filetxts[file.filename] = txt
            file.fingerprintssetup = winnow_setup(txt, k, w)
            for fp in list(file.fingerprintssetup.keys()):
                if fp in bpfingerprints:  #todo: remove fp here?
                    continue
                allfingerprints[fp][file] = []
                # inconsistent with how it's done in line 178 but i think this may be the way you have to do it
                for pos in file.fingerprintssetup[fp]:
                    substr = get_substring(pos, k, txt)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)


    #fill the file's similarto dictionary with the necessary fingerprints
    for file in files:
        for fp in list(file.fingerprintssetup.keys()):
            commonfiles = allfingerprints.get(fp)
            if (commonfiles == None):
                continue
            elif len(commonfiles) > 1:
                for commonfile in commonfiles:
                    if file != commonfile: #put it into similarto if it's a different file
                        if commonfile in file.similarto: #fp blocks may be able to be determined here to be faster
                            file.similarto[commonfile].append((allfingerprints[fp][file], allfingerprints[fp][commonfile]))
                        else:
                            file.similarto[commonfile] = [(allfingerprints[fp][file], allfingerprints[fp][commonfile])]
                        """old version of this part
                        if similarfilename in file.similarto:
                            file.similarto[similarfilename].append({file.fingerprints[fp]: list(fpdata.values())[0]})
                        else:
                            file.similarto[similarfilename] = [{file.fingerprints[fp]: list(fpdata.values())[0]}]"""
    return files

#gets the most important matches, as determined by the number of blocks of consecutive fingerprints
#changing blocksize determines how many consecutive fingerprints there have to be before being considered
#a block, changing offset determines the distance that's allowed between each print for it to be considered
#within the same block
def get_most_important_matches(f1, f2): #todo: originality threshold to determine when most important match is searched for, precision on which part of a smaller block is in a greater block
    blocksize = 8  # blocksize blocksize should probably never be set to a number <=1 with the way this works, but there's probably no reason to do so
    offset = 0
    f1_fingerprints = []
    f2_fingerprints = {}
    f2_fpshandle = []
    #for file in files:
    for fptuple in f1.similarto[f2]: #order the fingerprint's individually by location
        f2_fingerprints[fptuple[1][0].fp_hash] = fptuple[1]
        for f1_fp in fptuple[0]:
            f1_fingerprints.append(f1_fp)
        #for f2_fp in fptuple[1]:
        #   f2_fpshandle.append(f2_fp)
    f1_fingerprints.sort(key = lambda fps: fps.global_pos)
    #f2_fpshandle.sort(key = lambda fps: fps.global_pos)
    blockcounter = 0
    most_important_match_locations = []
    f1_blocks = {}
    fp2lastpos = []
    for fp in range(len(f1_fingerprints) - 1): #find if consecutive
        okay = False
        print("Iteration", blockcounter)
        if blockcounter == 0: #start of a new block
            start = f1_fingerprints[fp]
            f2start = f2_fingerprints[f1_fingerprints[fp].fp_hash].copy()
            print("F1: start", start.global_pos, end = ", ")
            for s in f2start:
                print("F2: start", s.global_pos, end = " ")
            print("")
            fp2lastpos = f2_fingerprints[f1_fingerprints[fp].fp_hash]
        blockcounter +=1
        if ((f1_fingerprints[fp].global_pos + len(f1_fingerprints[fp].substring) + offset) >= f1_fingerprints[fp + 1].global_pos): #f1 fingerprint is consecutive
            print("check")
            for f2matchpos in fp2lastpos: #check all potential positions
                if f2matchpos.global_pos == -1:
                    continue
                i = 0
                for fp2 in f2_fingerprints[f1_fingerprints[fp].fp_hash]: #check if consecutive in f2, 1st position
                    print (f2matchpos.global_pos, fp2.global_pos)
                    if fp2.global_pos == f2matchpos.global_pos:
                        for fp2prime in f2_fingerprints[f1_fingerprints[fp + 1].fp_hash]: #check if consecutive in f2, second position
                            print (fp2prime.global_pos, f2matchpos.global_pos)
                            if fp2prime.global_pos < f2matchpos.global_pos: #only check locations which can be consecutive
                                continue
                            elif (f2matchpos.global_pos + len(f2matchpos.substring) + offset) >= fp2prime.global_pos: #get last consecutive occurence
                                okay = True
                                fp2lastpos[i] = fp2prime
                            elif blockcounter < blocksize:
                                fp2lastpos[i] = Fingerprint(-1, -1, "") #error code
                i += 1
        if okay == False:   #end of block
            print("blockend", blockcounter, blocksize)
            if blockcounter >= blocksize:
                end = f1_fingerprints[fp]
                templist = []
                for pos in range(len(fp2lastpos)):
                    if fp2lastpos[pos].global_pos == -1:
                        continue
                    templist.append((f2start[pos], fp2lastpos[pos]))
                most_important_match_locations.append(((start, end), templist))
            blockcounter = 0
    if blockcounter >= blocksize: #1 more block check to see if the last one was end of a block
        end = f1_fingerprints[len(f1_fingerprints) - 1]
        #most_important_match_locations[(start, end)] = []
        templist = []
        for pos in range(len(fp2lastpos)):
            if fp2lastpos[pos].global_pos == -1:
                continue
            templist.append((f2start[pos], fp2lastpos[pos]))
        most_important_match_locations.append(((start, end), templist))
    for mostimportant in most_important_match_locations:
        print("F1: ")
        print(mostimportant[0][0].substring + "(" + str(mostimportant[0][0].global_pos) + ") - " + mostimportant[0][1].substring + "(" + str(mostimportant[0][1].global_pos) + ")")
        print("F2: ")
        for f2matchblock in mostimportant[1]:
            print(f2matchblock[0].substring + "("+ str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ", end = "+ ")
        print("")

""""
#version for 2 files
def get_most_important_matches(f1, f2):
    blocksize = 5  # blocksize blocksize should probably never be set to a number <=1 with the way this works, but there's probably no reason to do so
    offset = 5
    f1_fingerprints = []
    f2_fingerprints = []
    for fptuple in f1.similarto[f2]: #order the fingerprint's individually by location
        for f1_fp in fptuple[0]:
            f1_fingerprints.append(f1_fp)
        for f2_fp in fptuple[1]:
            f2_fingerprints.append(f2_fp)
    f1_fingerprints.sort(key = lambda fps: fps.global_pos)
    for fp in f1_fingerprints:
        print(fp.global_pos)
    blockcounter = 0
    most_important_match_locations = [{}]
    f1_blocks = {}
    for fp in range(len(f1_fingerprints) - 1):
        if (f1_fingerprints[fp].global_pos + len(f1_fingerprints[fp].substring) + offset) >= (f1_fingerprints[fp+ 1]).global_pos: #see if fits within block size
            print((f1_fingerprints[fp].global_pos + len(f1_fingerprints[fp].substring) + offset), (f1_fingerprints[fp+ 1]).global_pos)
            if blockcounter == 0:
                start = f1_fingerprints[fp]
            blockcounter += 1
        else: #newblock
            blockcounter += 1
            if blockcounter >= blocksize:
                end = f1_fingerprints[fp]
                f1_blocks[start] = end
            blockcounter = 0
    if blockcounter >= blocksize: #1 more block check to see if the last one was end of a block
        end = f1_fingerprints[len(f1_fingerprints) - 1]
        f1_blocks[start] = end
    for mostimportant in f1_blocks:
        print(mostimportant.substring + "(" + str(mostimportant.global_pos) + "), " + f1_blocks[mostimportant].substring + "(" +str(f1_blocks[mostimportant].global_pos) + ")")
"""

#version that gets it from 2 fingerprint lists instead of filetofingerprint objects, not finished but can be made if necessary
"""def get_most_important_matches(f1_fingerprints, f2_fingerprints):
    offset = 30
    blocksize = 5
    blockcounter = 0
    blockend = False
    counting = False
    most_important_match_locations = [{}]
    f1_blocks = {}
    for fp in range(len(f1_fingerprints) - 1):
        if (f1_fingerprints[fp].global_pos + len(fp.substring) + offset) >= (f1_fingerprints[fp+ 1]).global_pos: #see if fits within block size
            if blockcounter == 0:
                start = f1_fingerprints[fp]
            blockcounter += 1
        else: #newblock
            blockcounter += 1
            if blockcounter >= blocksize:
                end = f1_fingerprints[fp]
                f1_blocks.append[(start, end)]
            blockcounter = 0"""

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
                    # cifbreak
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
            print("")


def main():
    # songtest1 + songtest2 are songs with lyrics written slightly differently/remixed so could be considered copyright
    # texttest1 is an announcement from the class, texttest2 is a description of a game from a store page
    # c++ test is a file from programming 2 project 2, java test is from
    # programming 1 project 1 (neither of these 2 copied)
    print("Single document tests:")
    get_common_fingerprints("songtest1.txt", "songtest2.txt", 5, 4, "")
    compare_files("songtest1.txt", "songtest2.txt", 5, 4, "")
    compare_files("songtest1.txt", "texttest1.txt", 5, 4, "")
    compare_files("javatest1.java", "c++test1.cpp", 5, 4, "")
    compare_files("texttest1.txt", "texttest2.txt", 5, 4, "")
    print("")

    print("Multi-document tests: ")
    #multidocumenttest = ["songtest1.txt", "songtest2.txt", "javatest1.java", "c++test1.cpp", "texttest2.txt"]
    multidocumenttest = ["songtest1.txt", "songtest2.txt", "javatest1.java"]
    filetofingerprintobjects = compare_multiple_documents(multidocumenttest, 5, 4, [])
    print_prototype_test(filetofingerprintobjects, [])
    print("")

    print("Boilerplate tests: ")
    compare_files("songtest1.txt", "songtest2.txt", 5, 4, "songtest1.txt")
    boilerplate = ["songtest1.txt", "texttest2.txt"]
    boilerplatetest = ["songtest1.txt", "songtest2.txt","c++test1.cpp", "javatest1.java"]
    #filetofingerprintobjects = compare_multiple_documents(boilerplatetest, 5, 4, boilerplate)
    #print_prototype_test(filetofingerprintobjects, boilerplate)

    print("Most important matches:")
    get_most_important_matches(filetofingerprintobjects[0], filetofingerprintobjects[1])


if __name__ == "__main__":
    main()
