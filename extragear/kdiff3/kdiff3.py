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
        #Only attempt to install shell extention in standalone mode 
        if not isinstance(self, AppxPackager):
            self.self.defines["registry_hook"]=("""!define DIFF_EXT6\n4_CLSID "{34471FFB-4002-438b-8952-E4588D0C0FE9}"\n
                StrCpy $DIFF_EXT_DLL "kdiff3ext.dll"\n
                StrCpy $DIFF_EXT_ID "diff-ext-for-kdiff3"\n
                \n
                WriteRegStr SHCTX "Software\Classes\CLSID\$DIFF_EXT_CLSID" "" "$DIFF_EXT_ID"\n
                WriteRegStr SHCTX "Software\Classes\CLSID\$DIFF_EXT_CLSID\InProcServer32" "" "$INSTDIR\bin\$DIFF_EXT_DLL"\n
                WriteRegStr SHCTX "Software\Classes\CLSID\$DIFF_EXT_CLSID\InProcServer32" "ThreadingModel" "Apartment"\n
                WriteRegStr SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\$DIFF_EXT_ID" "" "$DIFF_EXT_CLSID"\n
                WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "$DIFF_EXT_CLSID" "$DIFF_EXT_ID"\n
                WriteRegStr SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\$DIFF_EXT_ID" "" "$DIFF_EXT_CLSID"\n
                WriteRegStr SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\$DIFF_EXT_ID" "" "$DIFF_EXT_CLSID"\n
                \n
                WriteRegStr HKCU  "Software\KDiff3\diff-ext" "" ""\n
                WriteRegStr SHCTX "Software\KDiff3\diff-ext" "InstallDir" "$INSTDIR"\n
                WriteRegStr SHCTX "Software\KDiff3\diff-ext" "diffcommand" "$INSTDIR\kdiff3.exe"\n
            """)
        
        # remove old version if it exists may not work for pre-1.8 due to changes in the build system
        self.defines["preInstallHook"] = r"""
                Exec "$INSTDIR\Uninstall.exe"
                """

        return TypePackager.createPackage(self)
