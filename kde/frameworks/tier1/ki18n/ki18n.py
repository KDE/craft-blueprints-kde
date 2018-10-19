import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.45.0"] = [("0001-Don-t-need-to-run-previous-iterations-commands-again.patch", 1),
                ("0002-Keep-LibIntl-libraries-path.patch", 1)]
        for ver in ['master', '5.42.0', '5.43.0', '5.44.0', '5.46.0', '5.47.0', '5.48.0', '5.49.0']:
            self.patchToApply[ver] = [("0002-Keep-LibIntl-libraries-path.patch", 1)]
        self.description = "Ki18n"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/gettext"] = None
        self.buildDependencies["libs/qt5/qtdeclarative"] = None # only needed for unit tests
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        if CraftVersion(self.buildTarget) < CraftVersion("5.50.0"):
            self.runtimeDependencies["libs/qt5/qtscript"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/gettext"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
