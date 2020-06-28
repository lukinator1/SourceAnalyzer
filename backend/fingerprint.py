

class Fingerprint:

    def __init__(self, fp_hash, global_pos, substring):
        self.__fp_hash = fp_hash
        self.__global_pos = global_pos
        self.__substring = substring

    @property
    def fp_hash(self):
        return self.__fp_hash

    @property
    def global_pos(self):
        return self.__global_pos

    @property
    def substring(self):
        return self.__substring


