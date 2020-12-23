import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        #Warning: Craft by default takes the display name to also be the product name. 
        self.displayName = 'KDiff3'
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
        
        self.defines["executable"] = r"bin\kdiff3.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kdiff3.ico")
        #self.defines["display_name"] = r"KDiff3"
        
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        #Only attempt to install shell extention in standalone mode 
        if not isinstance(self, AppxPackager):
            if self.subinfo.buildTarget == "1.8":
                self.defines["version"] = "1.8.5"
            
            self.defines["registry_hook"]=(r"""
        !define DIFF_EXT_CLSID "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
        !define DIFF_EXT_ID "Diff-ext for KDiff3"
        !define DIFF_EXT_DLL "kdiff3ext.dll"
        
        SetRegView 64
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}" "" "${DIFF_EXT_ID}"
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "" "$INSTDIR\bin\kf5\${DIFF_EXT_DLL}"
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "ThreadingModel" "Apartment"
        WriteRegStr SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}" "${DIFF_EXT_ID}"
        WriteRegStr SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        WriteRegStr SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        SetRegView 32

        WriteRegStr HKCU  "${regkey}\diff-ext" "" ""
        WriteRegStr HKCU "${regkey}\diff-ext" "InstallDir" "$INSTDIR\bin"
        WriteRegStr HKCU "${regkey}\diff-ext" "diffcommand" "$INSTDIR\bin\kdiff3.exe"
                """)
            self.defines["un_sections"] = r"""
                    Section "Un.Cleanup Regsistry"
                        SetRegView 64
                        DeleteRegKey SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}"
                        DeleteRegKey SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
                        DeleteRegKey SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
                        DeleteRegKey SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
                        DeleteRegValue SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}"
                        SetRegView 32
                        ;remove old diff-ext settings
                        DeleteRegKey HKCU  "Software\KDiff3"
                        ;Maybe left behind due to a bug in previous installers.
                        DeleteRegKey SHCTX  "Software\KDE\KDiff3"
                        DeleteRegKey /ifempty SHCTX  "Software\KDE\"
                    SectionEnd
                    """
        else:
	        #Windows app store has special requirements for the version format
            #Craft attempts to alter the second and third number so we have to adjust to craft's logic as well.
            self.defines["version"] = "1.0.85"
                        
            self.defines["un_sections"] = r"""
            Section "Un.Cleanup Regsistry"
                ;Maybe left behind due to a bug in previous installers.
                DeleteRegKey SHCTX  "Software\KDE\KDiff3"
                DeleteRegKey /ifempty SHCTX  "Software\KDE\"
            SectionEnd
            """

        return TypePackager.createPackage(self)
