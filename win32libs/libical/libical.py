import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.0.0", "3.0.1", "3.0.2"]:
            self.targets[ver] = f"https://github.com/libical/libical/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libical-{ver}"
            self.archiveNames[ver] = f"libical-{ver}.tar.gz"

        self.patchToApply["2.0.0"] = [("001-libical-2.0.0-search-snprintf.diff", 1)]
        self.targetDigests["2.0.0"] = (["20f4a98475052e1200d2691ba50b27969e4bedc6e50bffd5e2fa81f4ac90de9a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.0.1"] = (['6405964d596aac64fc82c03c4486387fd6a9c09b1f7af1ff251238e66b9e66e1'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.0.2"] = (['f9699be8521e1aea190a7c87802805d3388e0a3f59a9b9faedec490f596807a0'],  CraftHash.HashAlgorithm.SHA256)

        self.description = "Reference implementation of the icalendar data type and serialization format"
        self.webpage = "http://libical.github.io/libical/"
        self.defaultTarget = "3.0.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/winflexbison"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["win32libs/icu"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = f" -DUSE_BUILTIN_TZDATA=ON -DICAL_UNIX_NEWLINE=OFF -DICAL_GLIB=OFF -DSHARED_ONLY=ON -DICU_BASE={CraftCore.standardDirs.craftRoot()}"
