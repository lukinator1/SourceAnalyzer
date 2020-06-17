# A filetofingerprint object has a filename, a unique fileid, a dictionary of fingerprints [hash:locationinfile],
# and a similarto dictionary [similarfilename:[originalfilelocation:similarfilelocation]]
class filetofingerprint():
    def __init__(self, filename, fileid, fingerprints, similarto):
        self.filename = filename
        self.fileid = fileid
        self.fingerprints = fingerprints
        self.similarto = similarto