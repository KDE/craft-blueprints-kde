import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "z image library: scaling, colorspace conversion, and dithering library"

        for ver in ["3.0.5"]:
            # We need to use git tags because the GitHub release archives to not contain the submodules
            self.svnTargets[ver] = f"https://github.com/sekrit-twc/zimg.git||release-{ver}"

        self.svnTargets["master"] = "https://github.com/sekrit-twc/zimg.git"
        self.defaultTarget = "3.0.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # if self.package.isInstalled: # this is causing rebuild every time
        #     PackageBase.unmerge(self) # else build picks old incompatible includes

    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True
