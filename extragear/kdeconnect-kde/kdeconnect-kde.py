import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/kde/kdeconnect-kde.git'
        self.defaultTarget = 'master'
        self.description = "KDE Connect adds communication between KDE and your smartphone"
        self.displayName = "KDE Connect"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))

        self.defines["caption"] = self.binaryArchiveName(fileType=None).capitalize()
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.defines["appname"] = "kdeconnect-indicator"

        self.defines["nsis_include"] = f"!include {self.packageDir()}\\SnoreNotify.nsh"
        self.defines["sections"] = r"""
            !define MyApp_AppUserModelId  org.kde.kdeconnect.daemon
            !define SnoreToastExe "$INSTDIR\bin\SnoreToast.exe"

            Section "@{productname}"
                SectionIn 1
                !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
                    !insertmacro SnoreShortcut "$SMPROGRAMS\@{productname}.lnk" "$INSTDIR\bin\@{appname}.exe" "${MyApp_AppUserModelId}"
                    CreateShortCut "$SMPROGRAMS\Startup\@{productname}.lnk" "$INSTDIR\bin\@{appname}.exe"
                    CreateShortCut "$DESKTOP\@{productname}.lnk" "$INSTDIR\bin\@{appname}.exe"
                !insertmacro MUI_STARTMENU_WRITE_END
            SectionEnd
            """
        self.defines["un_sections"]=r"""
            Section "Un.Remove Shortcuts"
                Delete "$SMPROGRAMS\@{productname}.lnk"
                Delete "$SMPROGRAMS\Startup\@{productname}.lnk"
                Delete "$DESKTOP\@{productname}.lnk"
            SectionEnd
            """
        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # move everything to the location where Qt expects it
        pluginPath = os.path.join(archiveDir, "plugins")
        binPath = os.path.join(archiveDir, "bin")
        libPath = os.path.join(archiveDir, "lib")

        if CraftCore.compiler.isMacOS:
            # Move kdeconnect-cli and kdeconnectd to package
            defines = self.setDefaults(self.defines)
            appPath = self.getMacAppPath(defines)
            if not utils.copyFile(os.path.join(binPath, "dbus-daemon"), 
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False
            
            if not utils.copyFile(os.path.join(binPath, "kdeconnect-cli"), 
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False
            
            if not utils.copyFile(os.path.join(libPath, "libexec", "kdeconnectd"), 
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False
        
        return utils.mergeTree(os.path.join(archiveDir, "lib/qca-qt5"), 
            pluginPath if CraftCore.compiler.isMacOS else binPath)
