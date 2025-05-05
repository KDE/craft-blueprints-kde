import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.17"]:
            self.targets[ver] = f"https://github.com/mm2/Little-CMS/releases/download/lcms{ver}/lcms2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lcms2-{ver}"
        self.targetDigests["2.17"] = (["d11af569e42a1baa1650d20ad61d12e41af4fead4aa7964a01f93b08b53ab074"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.17"] = [("lcms2-2.17-ability_to_disable_so.version_libs.patch", 1)]
        self.description = "A free, open source, CMM engine. It provides fast transforms between ICC profiles."
        self.defaultTarget = "2.17"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-Djpeg=disabled",
            "-Dtiff=disabled",
        ]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-Dversionedlibs=false"]
