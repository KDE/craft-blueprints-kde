import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["11.2.0"]:
            self.targets[ver] = f"https://github.com/harfbuzz/harfbuzz/archive/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"harfbuzz-{ver}"
        self.targetDigests["11.2.0"] = (["16c0204704f3ebeed057aba100fe7db18d71035505cb10e595ea33d346457fc8"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Text shaping library"
        self.defaultTarget = "11.2.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/freetype"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/cairo"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-Ddocs=disabled",
            "-Dbenchmark=disabled",
            "-Dglib=disabled",
            "-Dgobject=disabled",
            "-Dfreetype=enabled",
            f"-Dicu={self.subinfo.options.isActive('libs/icu').asEnabledDisabled}",
            f"-Dcairo={CraftCore.compiler.isAndroid.inverted.asEnabledDisabled}",
        ]
