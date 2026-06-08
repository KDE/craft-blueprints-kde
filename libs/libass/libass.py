import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.17.4"]:
            self.targets[ver] = f"https://github.com/libass/libass/releases/download/{ver}/libass-{ver}.tar.gz"
            self.targetInstSrc[ver] = "libass-" + ver
        self.targetDigests["0.17.4"] = (["a886b3b80867f437bc55cff3280a652bfa0d37b43d2aff39ddf3c4f288b8c5a8"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Portable subtitle renderer"
        self.defaultTarget = "0.17.4"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/fribidi"] = None
        self.runtimeDependencies["libs/harfbuzz"] = None


# If you are packaging libass for distribution, Autotools is recommended; when packaging for Windows Meson should work equally well.
# See https://github.com/libass/libass#building
if CraftCore.compiler.isWindows:

    class Package(MesonPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.args += [f"-Dfontconfig={self.subinfo.options.isActive('libs/fontconfig').asEnabledDisabled}"]

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            if CraftCore.compiler.isAndroid:
                self.subinfo.options.configure.args += ["--disable-require-system-font-provider"]
