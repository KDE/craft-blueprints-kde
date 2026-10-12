import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "The Swiss Army knife of sound processing tools"

        for ver in ["14.4.2"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/sox/sox/{ver}/sox-{ver}.tar.bz2"
            self.targetInstSrc[ver] = "sox-" + ver
            self.patchToApply[ver] = [("mingw-sox-install.patch", 1), ("sox-14.4.2-20250822.diff", 1)]

        self.targetDigests["14.4.2"] = (["81a6956d4330e75b5827316e44ae381e6f1e8928003c6aa45896da9041ea149c"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["07de8a7"] = "https://git.code.sf.net/p/sox/code#commit=07de8a77a862e6800b95a8d3a61c6b4e41362755"
        self.patchToApply["07de8a7"] = [("0001-ucrt-no-rewind-pipe.patch", 1)]

        if CraftCore.compiler.compiler.isMinGW:
            self.defaultTarget = "07de8a7"
        else:
            self.defaultTarget = "14.4.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/libsndfile"] = None
        self.runtimeDependencies["dev-utils/libtool"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
