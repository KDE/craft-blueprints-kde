import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.3.8"]:
            self.targets[ver] = f"https://www.mirrorservice.org/sites/ftp.gnu.org/gnu/libidn/libidn2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libidn2-{ver}"
        self.targetDigests["2.3.8"] = (["f557911bf6171621e1f72ff35f5b1825bb35b52ed45325dcdee931e5d3c0787a"], CraftHash.HashAlgorithm.SHA256)
        self.description = "libidn internationalized domain names library"
        self.webpage = "https://www.gnu.org/software/libidn"
        self.releaseManagerId = 5597
        self.defaultTarget = "2.3.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/gtk-doc"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/libunistring"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.autoreconf = False  # fails on mac and windows
        self.subinfo.options.configure.args += ["--disable-gtk-doc", "--disable-doc", "--disable-gcc-warnings"]
