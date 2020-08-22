import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Compares and merges 2 or 3 files or directories"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))
        
        self.defines["executable"] = "bin\\kdiff3.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kdiff3.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        #Only attempt to install shell extention in standalone mode 
        if 0 and not isinstance(self, AppxPackager):
            self.defines["registry_hook"]=("""                
                WriteRegStr SHCTX "Software\Classes\CLSID\{34471FFB-4002-438b-8952-E4588D0C0FE9}" "" "kdiff3ext"
                WriteRegStr SHCTX "Software\Classes\CLSID\{34471FFB-4002-438b-8952-E4588D0C0FE9}\InProcServer32" "" "$INSTDIR\bin\kdiff3ext.dll"
                WriteRegStr SHCTX "Software\Classes\CLSID\{34471FFB-4002-438b-8952-E4588D0C0FE9}\InProcServer32" "ThreadingModel" "Apartment"
                WriteRegStr SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\kdiff3ext" "" "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
                WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "{34471FFB-4002-438b-8952-E4588D0C0FE9}" "kdiff3ext"
                WriteRegStr SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\kdiff3ext" "" "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
                WriteRegStr SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\kdiff3ext" "" "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
                
                WriteRegStr HKCU  "Software\KDiff3\diff-ext" "" ""
                WriteRegStr SHCTX "Software\KDiff3\diff-ext" "InstallDir" "$INSTDIR"
                WriteRegStr SHCTX "Software\KDiff3\diff-ext" "diffcommand" "$INSTDIR\kdiff3.exe"
            """)
        
        # remove old version if it exists may not work for pre-1.8 due to changes in the build system
        #self.defines["preInstallHook"] = r"""
        #        Exec "$INSTDIR\Uninstall.exe"
        #        """

        return TypePackager.createPackage(self)
