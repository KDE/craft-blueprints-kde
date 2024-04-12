from Package.AutoToolsPackageBase import *
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        # Debian provides "proper" tarballs (i.e., ones that already contain a ./configure)
        # we cannot get those from the upstream repository or its Salsa mirror, unfortunately
        # for older/other versions, check out https://snapshot.debian.org/package/dpkg/, too
        for ver in ["1.21.22"]:
            self.targets[ver] = f"https://deb.debian.org/debian/pool/main/d/dpkg/dpkg_{ver}.tar.xz"
            self.targetInstSrc[ver] = f"dpkg-{ver}"

        self.targetDigests["1.21.22"] = (["5a1d15481bba79d7a4899fd55b4b6b18a987ca8d56ee8c43e9cab63b8a0a3545"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.21.22"

        self.patchToApply["1.21.22"] = [("dpkg-1.21.22-20230721.diff", 1), ("dpkg-1.21.22-20230726.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/gtk-doc"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
