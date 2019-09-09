import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/snoretoast|master'
        for ver in ["0.5.2", "0.6.0", "0.7.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/src/snoretoast-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"snoretoast-{ver}"
        self.targetDigests["0.5.2"] = (["e25ad5e21c2c748e234a2b114373bbb115dec09ad15abc7ee1bb6387046472a0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.6.0"] =  (['56b93c1f3aa06a9b170802385492c058fb4834608b1a3c0e773aa1bb5b3ec7ec'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.7.0"] =  (['f02e5a226b70d48339fc56fac80953c268b477e394e8bd41e089fbf9576254be'], CraftHash.HashAlgorithm.SHA256)
        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://phabricator.kde.org/source/snoretoast/"
        self.displayName = "SnoreToast"
        self.defaultTarget = "0.7.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)