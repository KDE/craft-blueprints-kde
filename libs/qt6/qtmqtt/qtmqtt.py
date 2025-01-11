import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets["master"] = "https://github.com/qt/qtmqtt.git"
        for ver in self.targets.keys():
            self.targets[ver] = f"https://github.com/qt/qtmqtt/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"qtmqtt-{ver}.tar.gz"
            self.targetInstSrc[ver] = "qtmqtt-%s" % ver
            # TODO
            self.targetDigestUrls = ([""], CraftHash.HashAlgorithm.SHA256)

        self.targetDigests["6.8.0"] = (["20be92715136ece60030be712091ef56d0ca6620e1bcac4e029e48becc4b75dc"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.7.3"] = (["7001991f19e6407e88a0b77c64eb4a5bd2a9f2147d3c04671ab5b9929befe842"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.7.2"] = (["b9bf8c8a0ca3fd491ebe6afb70b8888ced6c97c32f0d6d00b31585a2f882ea62"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.7.1"] = (["b10d4856f4efe912b607a516126ed3cb9ee143c357e2f1a344f266b312486cdd"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.7.0"] = (["fbc691b9090267ba5aa445f60f60cfce5996abda195c400fde56569eaacfcc78"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.6.2"] = (["a4571dc197a925d13cc3be71b01fa2c0eda55042f50dde0626c545de64465f62"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.5.3"] = (["8d3c9f01a482790504ed90f0c40f61039018df6a09af27851d56fa94c4e272c2"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
