import info
from Package.CMakePackageBase import *
from Packager.AppxPackager import AppxPackager
from Packager.NullsoftInstallerPackager import NullsoftInstallerPackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

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
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kpeople"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
        self.runtimeDependencies["kde/pim/kpeoplevcard"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        # try to use Breeze style as Windows style has severe issues for e.g. scaling
        self.runtimeDependencies["kde/plasma/breeze"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMacOS:
            # Add APPLE_IN_APP_BUNDLE flag to enable private DBus, when packing by Craft
            self.subinfo.options.configure.args += " -DAPPLE_IN_APP_BUNDLE=ON"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))
        self.addExecutableFilter(r"bin/(?!(kdeconnect-app|kdeconnect-indicator|kdeconnect-cli|kdeconnectd|kdeconnect-sms|kdeconnect-handler|dbus-daemon|kcmshell5|kbuildsycoca5|update-mime-database|kioslave|SnoreToast).*)")
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))

        self.defines["caption"] = self.binaryArchiveName(fileType=None).capitalize()
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.defines["appname"] = "kdeconnect-indicator"
        self.defines["AppUserModelID"] = "kdeconnect.daemon"
        self.defines["executable"] = r"bin/kdeconnect-app.exe"

        if isinstance(self, NullsoftInstallerPackager):
            self.defines["sections"] = r"""
                Section "@{productname}"
                    SectionIn 1
                    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
                        !insertmacro SnoreShortcut "$SMPROGRAMS\\@{productname}.lnk" "$INSTDIR\\bin\\kdeconnect-app.exe" "@{AppUserModelID}"
                        CreateShortCut "$SMPROGRAMS\\Startup\\@{productname}.lnk" "$INSTDIR\\bin\\@{appname}.exe"
                        CreateShortCut "$DESKTOP\\@{productname}.lnk" "$INSTDIR\\bin\\kdeconnect-app.exe"
                        CreateShortCut "$SENDTO\\Send to remote device via @{productname}.lnk" "$INSTDIR\\bin\\kdeconnect-handler.exe"  "" "$INSTDIR\\bin\\@{appname}.exe" 0
                        CreateShortCut "$SENDTO\\Open on remote device via @{productname}.lnk" "$INSTDIR\\bin\\kdeconnect-handler.exe"  "--open" "$INSTDIR\\bin\\@{appname}.exe" 0
                    !insertmacro MUI_STARTMENU_WRITE_END
                SectionEnd
                """
            self.defines["un_sections"]=r"""
                Section "Un.Remove Shortcuts"
                    Delete "$SMPROGRAMS\\@{productname}.lnk"
                    Delete "$SMPROGRAMS\\Startup\\@{productname}.lnk"
                    Delete "$DESKTOP\\@{productname}.lnk"
                    Delete "$SENDTO\\Send to remote device via @{productname}.lnk"
                    Delete "$SENDTO\\Open on remote device via @{productname}.lnk"
                SectionEnd
                """
        elif isinstance(self, AppxPackager):
            self.defines["startup_task"] = r"bin/@{appname}.exe"

            self.defines["additional_capabilities"] = r"""
            <uap7:Capability Name="globalMediaControl" />
            """
            self.defines["additional_xmlns"] = r"""
            xmlns:uap7="http://schemas.microsoft.com/appx/manifest/uap/windows10/7"
            xmlns:desktop2="http://schemas.microsoft.com/appx/manifest/desktop/windows10/2"
            """

            self.defines["desktop_extensions"] = r"""
            <desktop2:Extension Category="windows.firewallRules">
            <desktop2:FirewallRules Executable="bin/kdeconnectd.exe">
                <desktop2:Rule Direction="in" IPProtocol="TCP" LocalPortMax="1764" LocalPortMin="1714" Profile="all"/>
                <desktop2:Rule Direction="in" IPProtocol="UDP" LocalPortMax="1764" LocalPortMin="1714" Profile="all"/>
                <desktop2:Rule Direction="out" IPProtocol="TCP" LocalPortMax="1764" LocalPortMin="1714" Profile="all"/>
                <desktop2:Rule Direction="out" IPProtocol="UDP" LocalPortMax="1764" LocalPortMin="1714" Profile="all"/>
            </desktop2:FirewallRules>
            </desktop2:Extension>
            """

            self.defines["alias_executable"] = r"bin/kdeconnect-cli.exe"
            self.defines["alias"] = r"kdeconnect-cli"

            self.defines["file_types"] = ["*", ".txt"]
            self.defines["shortcuts"] = [{"name" : self.subinfo.displayName , "target" : f"bin/kdeconnect-app{CraftCore.compiler.executableSuffix}", "description" : self.subinfo.description}]
            self.defines["icon_png"] = os.path.join(self.packageDir(), ".assets", "Square150x150Logo.scale-100.png")
            self.defines["icon_png_44"] = os.path.join(self.packageDir(), ".assets", "Square44x44Logo.scale-100.png")
            self.defines["icon_png_310x150"] = os.path.join(self.packageDir(), ".assets", "Wide310x150Logo.scale-100.png")
            self.defines["icon_png_310x310"] = os.path.join(self.packageDir(), ".assets", "Square310x310Logo.scale-100.png")

        self.ignoredPackages.append("binary/mysql")
        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # move everything to the location where Qt expects it
        pluginPath = os.path.join(archiveDir, "plugins")
        binPath = os.path.join(archiveDir, "bin")

        if CraftCore.compiler.isMacOS:
            # Move kdeconnect, kdeconnect-sms to the package
            defines = self.setDefaults(self.defines)
            appPath = self.getMacAppPath(defines)
            if not utils.copyFile(os.path.join(archiveDir, "Applications", "KDE", "kdeconnect-app.app", "Contents", "MacOS", "kdeconnect-app"),
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False

            if not utils.copyFile(os.path.join(archiveDir, "Applications", "KDE", "kdeconnect-sms.app", "Contents", "MacOS", "kdeconnect-sms"),
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False

            if not utils.copyFile(os.path.join(archiveDir, "Applications", "KDE", "kdeconnect-handler.app", "Contents", "MacOS", "kdeconnect-handler"),
                os.path.join(appPath, "Contents", "MacOS"), linkOnly=False):
                return False

        return utils.mergeTree(os.path.join(archiveDir, "lib/qca-qt5"),
            pluginPath if CraftCore.compiler.isMacOS else binPath)
