import os
import info
from Packager.AppxPackager import *
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        # Warning: Craft by default takes the display name to also be the product name.
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
class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
    
    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))
        
        self.defines["executable"] = r"bin\kdiff3.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kdiff3.ico")
        
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        # Only attempt to install shell extention in standalone mode
        if not isinstance(self, AppxPackager):
            self.defines["version"] = self.subinfo.buildTarget
            
            self.defines["registry_hook"] = r"""
        !define DIFF_EXT_CLSID "{34471FFB-4002-438b-8952-E4588D0C0FE9}"
        !define DIFF_EXT_ID "Diff-ext for KDiff3"
        !define DIFF_EXT_DLL "kdiff3ext.dll"
        
        SetRegView 64
        ;remove old diff-ext settings
        DeleteRegKey HKCU  "Software\KDiff3"

        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}" "" "${DIFF_EXT_ID}"
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "" "$INSTDIR\bin\${DIFF_EXT_DLL}"
        WriteRegStr SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}\InProcServer32" "ThreadingModel" "Apartment"
        WriteRegStr SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        WriteRegStr SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}" "${DIFF_EXT_ID}"
        WriteRegStr SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"
        WriteRegStr SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}" "" "${DIFF_EXT_CLSID}"

        SetRegView 32

        ;remove old diff-ext settings
        DeleteRegKey HKCU  "Software\KDiff3"
        ;Maybe left behind due to a bug in previous installers.
        DeleteRegKey SHCTX  "Software\KDE\KDiff3"
        DeleteRegKey /ifempty SHCTX  "Software\KDE\"
        
        WriteRegStr HKCU  "${regkey}\diff-ext" "" ""
        WriteRegStr HKCU "${regkey}\diff-ext" "InstallDir" "$INSTDIR\bin"
        WriteRegStr HKCU "${regkey}\diff-ext" "diffcommand" "$INSTDIR\bin\kdiff3.exe"
        ;NSIS Does not seem to support translated text.
        MessageBox MB_OK|MB_ICONEXCLAMATION "A reboot may be needed to complete install if upgrading from pre-1.8."
        
                """
            self.defines["un_sections"] = r"""
                    Section "Un.Cleanup Stray Files"
                        RMDir /r /rebootok  $INSTDIR\bin
                        RMDir /REBOOTOK $INSTDIR
                    SectionEnd""" + r"""
                    
                    Section "Un.Cleanup Regsistry"
                        SetRegView 64
                        DeleteRegKey SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}"
                        DeleteRegKey SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
                        DeleteRegKey SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
                        DeleteRegKey SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
                        DeleteRegValue SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}"
                        DeleteRegValue SHCTX "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\" "$INSTDIR\bin\kdiff3.exe"

                        SetRegView 32
                        ;remove old diff-ext settings
                        DeleteRegKey HKCU  "Software\KDiff3"
                        ;Maybe left behind due to a bug in previous installers.
                        DeleteRegKey SHCTX  "Software\KDE\KDiff3"
                        DeleteRegKey /ifempty SHCTX  "Software\KDE\"
                    SectionEnd
                    """
        else:
            self.defines["un_sections"] = r"""
        Section "Un.Cleanup Regsistry"
        ;Maybe left behind due to a bug in previous installers.
        DeleteRegKey SHCTX  "Software\KDE\KDiff3"
        DeleteRegKey /ifempty SHCTX  "Software\KDE\"
        SectionEnd
        """

        return TypePackager.createPackage(self)
