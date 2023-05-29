import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "z image library"
        self.svnTargets["20220622"] = "https://github.com/sekrit-twc/zimg.git||51c3c7f750c2af61955377faad56e3ba1b03589f"
        self.defaultTarget = "20220622"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # if self.package.isInstalled: # this is causing rebuild every time
        #     PackageBase.unmerge(self) # else build picks old incompatible includes

    def install(self):
        old = self.subinfo.options.make.supportsMultijob
        self.subinfo.options.make.supportsMultijob = False
        if not super().install():
            return False
        self.subinfo.options.make.supportsMultijob = old
        return True
