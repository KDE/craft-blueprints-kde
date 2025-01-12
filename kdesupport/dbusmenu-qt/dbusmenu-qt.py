import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/doxygen"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        # self.runtimeDependencies["kdesupport/qjson"] = None

    def setTargets(self):
        # Dbusmenu-qt moved to bazaar in launchpad
        # check https://launchpad.net/libdbusmenu-qt for the trunk sources

        for ver in ["0.9.2", "0.6.4"]:
            self.targets[ver] = f"https://launchpad.net/libdbusmenu-qt/trunk/{ver}/+download/libdbusmenu-qt-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libdbusmenu-qt-{ver}"
        self.targets["qt5"] = "http://winkde.org/~pvonreth/other/tars/libdbusmenu-qt-qt5.tar.gz"
        self.targetInstSrc["qt5"] = "libdbusmenu-qt-qt5"
        self.description = "a Qt implementation of the DBusMenu spec"

        self.patchToApply["0.9.2"] = [("dbusmenu-qt-0.9.2.diff", 1)]
        self.defaultTarget = "qt5"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}"]
