import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/peruse|master'
        self.defaultTarget = 'master'
        self.description = "Peruse Comic Book Viewer and Creator"
        self.webpage = "http://peruse.kde.org"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/breeze-icons"] = "default"
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kirigami"] = "default"
        self.runtimeDependencies["frameworks/tier2/kfilemetadata"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdeclarative"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/kdenetwork/kio-extras"] = "default"
        self.runtimeDependencies["kde/applications/okular"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        self.defines["productname"] = "Peruse Comic Book Viewer"
        self.defines["executable"] = "bin\\peruse.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "peruse.ico")
        self.defines["extrashortcuts"] = 'CreateShortCut "${startmenu}\\Peruse Creator.lnk" "$INSTDIR\\bin\\perusecreator.exe" "" "$INSTDIR\\bin\\perusecreator.exe"\n'
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        utils.moveFile(os.path.join(archiveDir, "etc", "xdg", "peruse.knsrc"),
                       os.path.join(binPath, "data", "peruse.knsrc"))

        utils.rmtree(os.path.join(self.archiveDir(), "lib"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils-wins"))

        return True
