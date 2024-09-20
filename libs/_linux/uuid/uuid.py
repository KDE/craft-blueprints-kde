import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.37"
        minor_ver = "2.37.2"
        self.targets[minor_ver] = f"https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v{ver}/util-linux-{minor_ver}.tar.xz"
        self.targetInstSrc[minor_ver] = f"util-linux-{minor_ver}"
        self.targetDigests[minor_ver] = (["6a0764c1aae7fb607ef8a6dd2c0f6c47d5e5fd27aa08820abaad9ec14e28e9d9"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = minor_ver

    def setDependencies(self):
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["dev-utils/gtk-doc"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-all-programs", "--enable-libuuid"]
