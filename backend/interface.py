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
        return get_all_fps_txt(student_filename, base_filename, k)
    else:
        return get_winnow_fps_txt(student_filename, base_filename, k, w)


def get_winnow_fps_txt(student_filename, base_filename, k, w):
    student_file = open(student_filename, "r")
    student_txt = student_file.read()
    student_fingerprints = text_winnow_setup(student_txt, k, w)

    base_file = open(base_filename, "r")
    base_txt = base_file.read()
    base_fingerprints = text_winnow_setup(base_txt, k, w)

    common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            substrings1 = {}
            substrings2 = {}
            for pos in student_fingerprints[fp]:
                substr = get_text_substring(pos, k, student_txt)
                if substr in substrings1:
                    substrings1[substr] = substrings1[substr] + [pos]
                else:
                    substrings1[substr] = [pos]
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = get_text_substring(pos, k, base_txt)
                if substr in substrings2:
                    substrings2[substr] = substrings2[substr] + [pos]
                else:
                    substrings2[substr] = [pos]
            for substr in substrings1:
                if substr in substrings2:
                    positions = [substrings1[substr], substrings2[substr]]
                    sfp = Fingerprint(fp, positions, substr)
                    common.append(sfp)

    return common


def get_all_fps_txt(student_filename, base_filename, k):
    student_file = open(student_filename, "r")
    student_txt = student_file.read()
    student_fingerprints = compute_all(student_txt, k)

    base_file = open(base_filename, "r")
    base_txt = base_file.read()
    base_fingerprints = compute_all(base_txt, k)

    common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            substrings1 = {}
            substrings2 = {}
            for pos in student_fingerprints[fp]:
                substr = get_text_substring(pos, k, student_txt)
                if substr in substrings1:
                    substrings1[substr] = substrings1[substr] + [pos]
                else:
                    substrings1[substr] = [pos]
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = get_text_substring(pos, k, base_txt)
                if substr in substrings2:
                    substrings2[substr] = substrings2[substr] + [pos]
                else:
                    substrings2[substr] = [pos]
            for substr in substrings1:
                if substr in substrings2:
                    positions = [substrings1[substr], substrings2[substr]]
                    sfp = Fingerprint(fp, positions, substr)
                    common.append(sfp)

    return common


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
        get_all_fps_py(student_filename, base_filename, k)
    else:
        get_winnow_fps_py(student_filename, base_filename, k, w)


def get_winnow_fps_py(student_filename, base_filename, k, w):
    with open(student_filename, "r") as student_source:
        vs = PyAnalyzer(student_source)
    student_fingerprints = winnow(vs.parsed_code, k, w)

    with open(base_filename, "r") as base_source:
        vb = PyAnalyzer(base_source)
    base_fingerprints = winnow(vb.parsed_code, k, w)

    common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            substrings1 = {}
            substrings2 = {}
            for pos in student_fingerprints[fp]:
                substr = vs.get_code_from_parsed(k, pos)
                if substr in substrings1:
                    substrings1[substr] = substrings1[substr] + [pos]
                else:
                    substrings1[substr] = [pos]
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = vb.get_code_from_parsed(k, pos)
                if substr in substrings2:
                    substrings2[substr] = substrings2[substr] + [pos]
                else:
                    substrings2[substr] = [pos]
            for substr in substrings1:
                if substr in substrings2:
                    positions = [substrings1[substr], substrings2[substr]]
                    sfp = Fingerprint(fp, positions, substr)
                    common.append(sfp)

    return common


def get_all_fps_py(student_filename, base_filename, k):
    with open(student_filename, "r") as student_source:
        vs = PyAnalyzer(student_source)
    student_fingerprints = compute_all(vs.parsed_code, k)

    with open(base_filename, "r") as base_source:
        vb = PyAnalyzer(base_source)
    base_fingerprints = compute_all(vb.parsed_code, k)

    common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            # for each position add an object
            substrings1 = {}
            substrings2 = {}
            for pos in student_fingerprints[fp]:
                substr = vs.get_code_from_parsed(k, pos)
                if substr in substrings1:
                    substrings1[substr] = substrings1[substr] + [pos]
                else:
                    substrings1[substr] = [pos]
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = vb.get_code_from_parsed(k, pos)
                if substr in substrings2:
                    substrings2[substr] = substrings2[substr] + [pos]
                else:
                    substrings2[substr] = [pos]
            for substr in substrings1:
                if substr in substrings2:
                    positions = [substrings1[substr], substrings2[substr]]
                    sfp = Fingerprint(fp, positions, substr)
                    common.append(sfp)

    return common


def main():
    compare_files_txt("test_files/test.txt", "test_files/test2.txt", 5, 4)
    get_winnow_fps_txt("test_files/test.txt", "test_files/test2.txt", 5, 4)
    get_all_fps_txt("test_files/test.txt", "test_files/test2.txt", 5)
    compare_files_py("test_files/test1.py", "test_files/test2.py", 10, 5)
    get_winnow_fps_py("test_files/test1.py", "test_files/test2.py", 10, 5)
    get_all_fps_py("test_files/test1.py", "test_files/test2.py", 20)


if __name__ == "__main__":
    main()
