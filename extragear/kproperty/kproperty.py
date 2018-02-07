import info


class subinfo(info.infoclass):
    def setTargets(self):
        versions = ['3.1', 'master']
        for ver in versions:
            self.svnTargets[ver] = f"git://anongit.kde.org/kproperty|{ver}"
        self.defaultTarget = versions[0]
        self.description = "A property editing framework with editor widget"
        self.options.configure.args = " -DBUILD_EXAMPLES=ON"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/breeze-icons"] = "default" # hard dependency for now

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
