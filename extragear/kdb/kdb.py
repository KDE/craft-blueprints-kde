import info


class subinfo(info.infoclass):
    def setTargets(self):
        versions = ['3.1', 'master']
        for ver in versions:
            self.svnTargets[ver] = f"git://anongit.kde.org/kdb|{ver}"
        self.defaultTarget = versions[0]
        self.description = "A database connectivity and creation framework"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-utils-win/python2"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/icu"] = "default"
        self.runtimeDependencies["libs/sqlite"] = "default"
        self.runtimeDependencies["binary/mysql"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def compile(self):
        # Prepend Craft's lib dir to LIB path so find_package(ICU) finds our files.
        # Otherwise it is possible that find_package(ICU) finds some random private
        # copies such as those coming with MSVS.
        env = {"LIB" : f"{os.path.join(CraftStandardDirs.craftRoot(), 'lib')};{os.environ['LIB']}"}
        with utils.ScopedEnv(env):
            return CMakePackageBase.compile(self)
