import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3.52"] = 'https://download.sysinternals.com/files/ProcessMonitor.zip'
        self.defaultTarget = '3.52'
        self.targetDigests["3.52"] =  (['3a0ce29f1654468a470d8b4e0f5f163a428ddab7bf0ea37b0cef504362cb94dd'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstallPath['3.52'] = os.path.join("dev-utils", "bin")


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
