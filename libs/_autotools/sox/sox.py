import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["14.4.2"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/sox/sox/{ver}/sox-{ver}.tar.bz2"
            self.targetInstSrc[ver] = "sox-" + ver
            self.patchToApply[ver] = [("mingw-sox-install.patch", 1)]
        self.targetDigests["14.4.2"] = (["81a6956d4330e75b5827316e44ae381e6f1e8928003c6aa45896da9041ea149c"], CraftHash.HashAlgorithm.SHA256)
        self.description = "The Swiss Army knife of sound processing tools"
        self.defaultTarget = "14.4.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/libsndfile"] = None
        self.runtimeDependencies["dev-utils/libtool"] = None


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
