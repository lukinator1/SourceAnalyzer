from backend.fingerprint import Fingerprint
from backend.winnowing import *


def compare_files_txt(student_file_loc, base_file_loc, k, w):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = text_winnow_setup(student_txt, k, w)
    num_std_fps = 0
    for val in student_fingerprints.values():
        for _ in val:
            num_std_fps += 1

    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = text_winnow_setup(base_txt, k, w)

    num_common_fps = 0
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            for _ in student_fingerprints[fp]:
                num_common_fps += 1

    similarity = num_common_fps / num_std_fps
    print(res := similarity * 100)
    return res, num_common_fps


def get_fps_txt(student_filename, base_filename, k, w, num_common_fps, ignore_count):
    student_file = open(student_filename, "r")
    student_txt = student_file.read()

    base_file = open(base_filename, "r")
    base_txt = base_file.read()

    if num_common_fps > ignore_count:
        student_fingerprints = compute_all(student_txt, k)
        base_fingerprints = compute_all(base_txt, k)
    else:
        student_fingerprints = text_winnow_setup(student_txt, k, w)
        base_fingerprints = text_winnow_setup(base_txt, k, w)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            for pos in student_fingerprints[fp]:
                substr = get_text_substring(pos, k, student_txt)
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = get_text_substring(pos, k, base_txt)
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    return student_common, base_common


def get_winnow_fps_txt(student_file_loc, base_file_loc, k, w):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = text_winnow_setup(student_txt, k, w)

    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = text_winnow_setup(base_txt, k, w)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            for pos in student_fingerprints[fp]:
                substr = get_text_substring(pos, k, student_txt)
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = get_text_substring(pos, k, base_txt)
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    return student_common, base_common


def get_all_fps_txt(student_file_loc, base_file_loc, k):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = compute_all(student_txt, k)

    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = compute_all(base_txt, k)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            for pos in student_fingerprints[fp]:
                substr = get_text_substring(pos, k, student_txt)
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = get_text_substring(pos, k, base_txt)
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    return student_common, base_common


def compare_files_py(student_filename, base_filename, k, w):
    with open(student_filename, "r") as student_source:
        vs = PyAnalyzer(student_source)
    student_fingerprints = winnow(vs.parsed_code, k, w)
    num_std_fps = 0
    for val in student_fingerprints.values():
        for _ in val:
            num_std_fps += 1
    # print(vs.parsed_code)
    # print(vs.code)

    with open(base_filename, "r") as base_source:
        vb = PyAnalyzer(base_source)
    base_fingerprints = winnow(vb.parsed_code, k, w)

    num_common_fps = 0
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            for _ in student_fingerprints[fp]:
                num_common_fps += 1

    similarity = num_common_fps / num_std_fps
    print(res := similarity * 100)
    return res, num_common_fps


def get_fps_py(student_filename, base_filename, k, w, num_common_fps, ignore_count):
    with open(student_filename, "r") as student_source:
        vs = PyAnalyzer(student_source)
    with open(base_filename, "r") as base_source:
        vb = PyAnalyzer(base_source)

    if num_common_fps > ignore_count:
        student_fingerprints = compute_all(vs.parsed_code, k)
        base_fingerprints = compute_all(vb.parsed_code, k)
    else:
        student_fingerprints = winnow(vs.parsed_code, k, w)
        base_fingerprints = winnow(vb.parsed_code, k, w)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            for pos in student_fingerprints[fp]:
                substr = vs.get_code_from_parsed(k, pos)
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = vb.get_code_from_parsed(k, pos)
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    return student_common, base_common


def get_winnow_fps_py(student_filename, base_filename, k, w):
    with open(student_filename, "r") as student_source:
        vs = PyAnalyzer(student_source)
    student_fingerprints = winnow(vs.parsed_code, k, w)

    with open(base_filename, "r") as base_source:
        vb = PyAnalyzer(base_source)
    base_fingerprints = winnow(vb.parsed_code, k, w)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            for pos in student_fingerprints[fp]:
                substr = vs.get_code_from_parsed(k, pos)
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = vb.get_code_from_parsed(k, pos)
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    """for std in student_common:
        print("W: " + str(std.global_pos) + "\n" + std.substring)"""

    return student_common, base_common


def get_all_fps_py(student_filename, base_filename, k):
    with open(student_filename, "r") as student_source:
        vs = PyAnalyzer(student_source)
    student_fingerprints = compute_all(vs.parsed_code, k)

    with open(base_filename, "r") as base_source:
        vb = PyAnalyzer(base_source)
    base_fingerprints = compute_all(vb.parsed_code, k)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            for pos in student_fingerprints[fp]:
                substr = vs.get_code_from_parsed(k, pos)
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = vb.get_code_from_parsed(k, pos)
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    return student_common, base_common


def main():
    compare_files_txt("test_files/test.txt", "test_files/test2.txt", 5, 4)
    get_winnow_fps_txt("test_files/test.txt", "test_files/test2.txt", 5, 4)
    get_all_fps_txt("test_files/test.txt", "test_files/test2.txt", 5)
    compare_files_py("test_files/test1.py", "test_files/test2.py", 10, 5)
    get_winnow_fps_py("test_files/test1.py", "test_files/test2.py", 10, 5)
    get_all_fps_py("test_files/test1.py", "test_files/test2.py", 20)


if __name__ == "__main__":
    main()
