import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/snoretoast|master'
        for ver in ["0.5.2"]:
            self.targets[ver] = "https://download.kde.org/stable/snoretoast/0.5.2/src/snoretoast-0.5.2.tar.xz"
            self.targetInstSrc[ver] = "snoretoast-0.5.2"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["0.5.2"] = (["e25ad5e21c2c748e234a2b114373bbb115dec09ad15abc7ee1bb6387046472a0"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://phabricator.kde.org/source/snoretoast/"
        self.displayName = "SnoreToast"
        self.defaultTarget = "0.5.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)