import info
from Packager.CollectionPackagerBase import PackagerLists


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Codevis is a software to visualize large software architectures."
        self.displayName = "Codevis"
        self.webpage = "http://invent.kde.org/sdk/codevis"
        self.svnTargets["master"] = "http://invent.kde.org/sdk/codevis.git"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/runtime"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/llvm"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/boost/boost-headers"] = None
        self.runtimeDependencies["libs/catch2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["lib/python"] = None

        # try to use Breeze style as Windows style has severe issues for e.g. scaling
        self.runtimeDependencies["kde/plasma/breeze"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DUSE_QT_WEBENGINE=OFF ", "-DCOMPILE_TESTS=OFF "]

    def createPackage(self):
        self.defines["executable"] = "bin\\codevis_desktop.exe"

        # we have multiple codevis executables, we need to copy all of them.
        self.addExecutableFilter(r"bin/(?!((codevis*)|kbuildsycoca5|update-mime-database|kioslave)).*")

        self.defines["shortcuts"] = [{"name": "Codevis", "target": "bin/codevis_desktop.exe", "description": self.subinfo.description}]

        self.defines["file_types"] = [".lks"]
        self.defines["alias"] = "codevis"

        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")
        self.ignoredPackages.append("kde/frameworks/kemoticons")

        return TypePackager.createPackage(self)
