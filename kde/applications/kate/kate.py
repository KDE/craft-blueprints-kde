import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Kate"
        self.description = "the KDE text editor"

    def registerOptions(self):
        self.options.dynamic.registerOption("fullPlasma", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kactivities"] = "default"
        if self.options.dynamic.fullPlasma:
            self.runtimeDependencies["kde/frameworks/tier3/plasma-framework"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = "default"
        if OsUtils.isUnix():
            self.runtimeDependencies["kde/applications/konsole"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["shortcuts"] = [{"name" : "Kate", "target":"bin/kate.exe", "description" : self.subinfo.description}]
        self.defines["icon"] = os.path.join(self.packageDir(), "kate.ico")
        self.defines["registy_hook"] = ("""WriteRegStr @{HKCR} "*\\shell\\EditWithKate" "" "Edit with Kate"\n"""
                                        """WriteRegStr @{HKCR} "*\\shell\\EditWithKate\\command" "" '"$INSTDIR\\bin\\kate.exe" "%V"'\n""")


        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        return TypePackager.createPackage(self)
