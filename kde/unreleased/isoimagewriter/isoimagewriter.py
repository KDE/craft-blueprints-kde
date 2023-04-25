from Packager.AppImagePackager import AppImagePackager
import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets["master"] = "https://invent.kde.org/utilities/isoimagewriter.git"
        for ver in ["1.0.0"]:
            self.targets[ver] = "https://download.kde.org/stable/isoimagewriter/%s/isoimagewriter-%s.tar.xz" % (ver, ver)
            self.targetInstSrc[ver] = "isoimagewriter-%s" % ver
        self.defaultTarget = "1.0.0"

        self.displayName = "ISO Image Writer"
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
        # we need the system icon for the creation of the appimage
        self.buildDependencies["kde/frameworks/tier1/breeze-icons-system"] = None


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
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            utils.copyFile(
                "/home/appimage/Craft/BinaryFactory/linux-64-gcc/build/kde/frameworks/tier1/breeze-icons-system/image-RelWithDebInfo-5.105.0/home/appimage/Craft/BinaryFactory/linux-64-gcc/share/icons/breeze/devices/64/drive-removable-media.svg",
                "/home/appimage/Craft/BinaryFactory/linux-64-gcc/build/kde/unreleased/isoimagewriter/archive/usr/share/breeze/apps/64/drive-removable-media.svg"
            )

        return True

    def createPackage(self):
        self.defines["shortcuts"] = [{"name": "KDE ISO Image Writer", "target": "bin/isoimagewriter.exe", "description": self.subinfo.description}]
        self.defines["icon"] = os.path.join(self.packageDir(), "isoimagewriter.ico")
        return super().createPackage()
