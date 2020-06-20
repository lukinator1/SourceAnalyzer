# A filetofingerprint object has a filename, a unique fileid, a dictionary of fingerprints as [hash:locationinfile],
# and a similarto dictionary as [similarfileobject:[([originalfingerprintobjects],[similarfingerprintobjects])]
class filetofingerprint():
    def __init__(self, filename, fileid, fingerprints, similarto):
        self.filename = filename
        self.fileid = fileid
        self.fingerprints = fingerprints
        self.similarto = similarto