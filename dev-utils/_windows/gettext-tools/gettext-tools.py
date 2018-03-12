import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets[
            '0.18.1.1_1'] = 'http://downloads.sourceforge.net/sourceforge/kde-windows/gettext-tools-0.18.1.1_1-bin.tar.bz2'
        self.targetDigestUrls[
            '0.18.1.1_1'] = 'http://downloads.sourceforge.net/sourceforge/kde-windows/gettext-tools-0.18.1.1_1-bin.tar.bz2.sha1'
        self.targetInstallPath['0.18.1.1_1'] = "dev-utils"
        self.defaultTarget = '0.18.1.1_1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
