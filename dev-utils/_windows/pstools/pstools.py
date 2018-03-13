import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.44'] = 'http://download.sysinternals.com/Files/PsTools.zip'
        self.defaultTarget = '2.44'
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath['2.44'] = os.path.join("dev-utils", "bin")


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
