import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['4.1.36'] = "http://www.siegward-jaekel.de/mc.zip"
        self.defaultTarget = '4.1.36'
        self.targetInstallPath["4.1.36"] = os.path.join("dev-utils", "bin")
        self.targetDigests['4.1.36'] = 'cce65f21d52da1d21c6b60ca8defe7888a235b2f'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        f = open(os.path.join(self.installDir(), 'mcedit.bat'), "wb")
        f.write("mc -e %1")
        f.close()
        # mc is also a program in visual studio,
        # so make the real mc reachable from mcc too...
        utils.copyFile(os.path.join(self.installDir(), "mc.exe"),
                       os.path.join(self.installDir(), "mcc.exe"))
        return True
