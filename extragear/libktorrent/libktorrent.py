import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/libktorrent'
        for ver in ['1.3.1']:
            self.targets[ver] = "http://ktorrent.org/downloads/4." + ver[2:] + "/libktorrent-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "libktorrent-" + ver
            self.patchToApply[ver] = [("libktorrent-1.3.1-20130607.diff", 1)]
        self.patchToApply['master'] = [("libktorrent-1.3.1-20130607.diff", 1)]

        self.description = "A BitTorrent protocol implementation."
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["kdesupport/qca"] = "default"
        self.runtimeDependencies["libs/mpir"] = "default"
        self.runtimeDependencies["libs/gpgme"] = "default"
        self.runtimeDependencies["libs/gcrypt"] = "default"
        self.buildDependencies["dev-utils-win/gettext-tools"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
