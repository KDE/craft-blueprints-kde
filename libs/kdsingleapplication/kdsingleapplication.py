import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.2.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSingleApplication/releases/download/v{ver}/kdsingleapplication-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDSingleApplication-{ver}"
        self.svnTargets["master"] = "https://github.com/KDAB/KDSingleApplication.git"

        self.targetDigests["1.2.0"] = (["ff4ae6a4620beed1cdb3e6a9b78a17d7d1dae7139c3d4746d4856b7547d42c38"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.2.0"

        self.description = "KDSingleApplication is a helper class for single-instance policy applications written by KDAB."
        self.webpage = "https://github.com/KDAB/KDSingleApplication"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += ["-DKDSingleApplication_TESTS=ON"]

        self.subinfo.options.configure.args += ["-DKDSingleApplication_QT6=ON"]
