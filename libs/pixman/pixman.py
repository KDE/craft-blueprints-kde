import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.40.0", "0.42.2", "0.46.4"]:
            self.targets[ver] = "http://cairographics.org/releases/pixman-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "pixman-" + ver
        self.description = "Image processing and manipulation library"
        self.targetDigests["0.40.0"] = (["6d200dec3740d9ec4ec8d1180e25779c00bc749f94278c8b9021f5534db223fc"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.42.2"] = (["ea1480efada2fd948bc75366f7c349e1c96d3297d09a3fe62626e38e234a625e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.46.4"] = (["d09c44ebc3bd5bee7021c79f922fe8fb2fb57f7320f55e97ff9914d2346a591c"], CraftHash.HashAlgorithm.SHA256)

        # https://gitlab.freedesktop.org/pixman/pixman/-/commit/bd4e7a9b9e672105bda35ff736c977adbf719c6c
        self.patchToApply["0.40.0"] = [("bd4e7a9b9e672105bda35ff736c977adbf719c6c.diff", 1)]

        self.defaultTarget = "0.42.4"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isMacOS:
            # disable neon on arm64 https://gitlab.freedesktop.org/pixman/pixman/-/issues/59
            self.subinfo.options.configure.args += ["-Da64-neon=disabled"]
