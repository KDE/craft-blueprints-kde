import info
from CraftOS.osutils import OsUtils
import datetime
import os
import subprocess


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionStrings = {}
        self.versionSemantic = {}

        ver = '3.1' # default version, TODO update on release
        self.svnTargets[ver] = f"git://anongit.kde.org/kexi|{ver}"
        self.versionStrings[ver] = '3.1.0 Preview' # TODO update on release
        self.versionSemantic[ver] = '3.1.0' # TODO update on release

        ver = 'master'
        self.svnTargets[ver] = f"git://anongit.kde.org/kexi|master"
        self.versionStrings[ver] = '3.2 Alpha' # TODO update on release
        self.versionSemantic[ver] = '3.1.90' # TODO update on release

        versions = [*self.svnTargets]
        self.defaultTarget = versions[0]
        self.description = "A visual database applications builder"
        self.webpage = "http://kexi-project.org"
        self.options.configure.args = " -DBUILD_EXAMPLES=ON"

    def registerOptions(self):
        self.options.dynamic.registerOption("desktop", True)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["win32libs/glib"] = "default" # mdb
        self.runtimeDependencies["win32libs/sqlite"] = "default" # migration
        self.runtimeDependencies["binary/mysql"] = "default" # migration
        #TODO self.runtimeDependencies["binary/postgresql"] = "default" # migration
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["kdesupport/kdewin"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["extragear/kdb"] = "default"
        self.runtimeDependencies["extragear/kproperty"] = "default"
        self.runtimeDependencies["extragear/kreport"] = "default"
        if self.options.dynamic.desktop:
            # Desktop only:
            self.runtimeDependencies["frameworks/tier1/breeze-icons"] = "default" # hard dependency for now
            self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
            self.runtimeDependencies["frameworks/tier3/kio"] = "default"
            self.runtimeDependencies["frameworks/tier3/ktexteditor"] = "default"
            self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
            self.runtimeDependencies["kde/plasma/breeze"] = "default" # hard dependency for now
            if OsUtils.isLinux():
                self.runtimeDependencies["frameworks/tier1/kcrash"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def stableVersion(self):
        """ Returns stable version for self.subinfo.versionSemantic[self.subinfo.buildTarget],
            that is x.y for stable releases and x.y+1 for unsable releases
        """
        buildTarget = self.subinfo.versionSemantic[self.subinfo.buildTarget].split('.')
        if int(buildTarget[2]) >= 90:
            return f"{buildTarget[0]}.{int(buildTarget[1]) + 1}"
        else:
            return f"{buildTarget[0]}.{buildTarget[1]}"

    def createPackage(self):
        self.defines["version_semantic"] = self.subinfo.versionSemantic[self.subinfo.buildTarget]
        ver = self.subinfo.versionStrings[self.subinfo.buildTarget]
        isAlpha = ver.endswith("Alpha")
        isPreview = "Preview" in ver
        if isAlpha or isPreview: # add git hash and date for Alphas/Previews
            gitHash = subprocess.check_output(
                ["git", "rev-parse", "--short", self.subinfo.buildTarget],
                cwd=self.sourceDir(), universal_newlines=True).strip()
            if isAlpha:
                date = subprocess.check_output(
                    ["git", "show", "--no-patch", "--format=%ci", self.subinfo.buildTarget],
                    cwd=self.sourceDir(), universal_newlines=True).strip().split(" ")[0]
            elif isPreview:
                date = str(datetime.date.today())
            ver = f"{ver} {date} ({gitHash})"
        self.defines["version"] = ver
        self.defines["productname"] = "KEXI"
        #default: self.defines["company"] = "KDE"
        self.defines["webpage"] = self.subinfo.webpage
        self.defines["executable"] = f"bin\\kexi-{self.stableVersion()}.exe"
        self.defines["icon"] = os.path.join(self.buildDir(), "src", "_source_var.ico")
        self.defines["license"] = os.path.join(self.sourceDir(), "COPYING.LIB")
        # user-friendly filename
        arch = '32' if CraftCore.compiler.isX86() else '64'
        filename = f"{self.defines['productname']}_{self.defines['version']}_Win{arch}.exe".replace(' ', '_')
        self.defines["setupname"] = os.path.join(self.packageDestinationDir(), filename)

        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        self.ignoredPackages.append("libs/d3dcompiler")
        self.ignoredPackages.append("libs/qt5/qttools")
        self.ignoredPackages.append("libs/qt5/qtscript")
        # no, needed by Qt5WebKit: self.ignoredPackages.append("libs/qt5/qtmultimedia")
        # no, needed by Qt5WebKit: self.ignoredPackages.append("libs/qt5/qtwebchannel")
        # no, needed by Qt5WebKit: self.ignoredPackages.append("qt-libs/phonon")

        self.ignoredPackages.append("frameworks/tier2/kpackage")
        self.ignoredPackages.append("frameworks/tier3/kdeclarative")
        self.ignoredPackages.append("frameworks/tier3/knewstuff")
        self.ignoredPackages.append("frameworks/tier3/kwallet") # pulled in by kio
        self.ignoredPackages.append("frameworks/tier3/plasma-framework")

        # TODO:  find a way to extend the default script
        self.scriptname = os.path.join(self.packageDir(), "NullsoftInstaller.nsi")
        utils.copyFile(os.path.join(self.packageDir(), "FileAssociation.nsh"),
                       self.workDir(), False) # needed in workdir

        for file in ["COPYING.DOC", "COPYING.LIB", "COPYING", "AUTHORS", "README.md", "README.PACKAGERS.md"]:
            utils.copyFile(os.path.join(self.sourceDir(), file),
                           os.path.join(self.installDir(), file), False)

        return TypePackager.createPackage(self)
