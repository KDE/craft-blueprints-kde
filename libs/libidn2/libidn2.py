import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.3.7"]:
            self.targets[ver] = f"https://www.mirrorservice.org/sites/ftp.gnu.org/gnu/libidn/libidn2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libidn2-{ver}"
        self.targetDigests["2.3.7"] = (["4c21a791b610b9519b9d0e12b8097bf2f359b12f8dd92647611a929e6bfd7d64"], CraftHash.HashAlgorithm.SHA256)
        self.description = "libidn internationalized domain names library"
        self.webpage = "https://www.gnu.org/software/libidn"
        self.defaultTarget = "2.3.7"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/gtk-doc"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/libunistring"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.autoreconf = not CraftCore.compiler.isWindows  # something form gtk-doc isn't found
        self.subinfo.options.configure.args += ["--disable-gtk-doc", "--disable-doc", "--disable-gcc-warnings"]
