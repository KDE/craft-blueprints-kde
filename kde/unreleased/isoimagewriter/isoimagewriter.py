import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets['master'] = 'https://invent.kde.org/utilities/isoimagewriter.git'
        self.defaultTarget = "master"

        self.displayName = "KDE ISO Image Writer"
        self.description = "A tool to write ISO images to USB flash drives"

    def setDependencies(self):
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isWindows:
            manifest = os.path.join(self.sourceDir(), "res", "isoimagewriter.manifest")
            app = os.path.join(self.installDir(), "bin", "isoimagewriter.exe")
            return utils.embedManifest(app, manifest)
