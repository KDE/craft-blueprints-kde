import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KCalcore library"
        self.patchToApply['17.04.1'] = [("kcalcore-fix-linking.diff", 1)]
        self.patchToApply['17.04.2'] = [("kcalcore-fix-linking.diff", 1)]
        self.patchToApply['17.12.0'] = [("0003-Remove-strings.h-include.patch", 1),
                                        ("0001-define-strncasecmp-and-strcasecmp-on-Windows.patch", 1),
                                        ("0003-Remove-unused-unistd.h-include.patch", 1),
                                        ("0002-Use-interface-lib-for-libical.patch", 1),
                                        ("0004-Fix-a-porting-bug-when-persing-timezones.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/libical"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
