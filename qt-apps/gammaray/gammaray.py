import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/GammaRay.git"
        for ver in ["2.7.0", "2.9.0", "2.9.1", "2.10.0", "2.11.0", "2.11.1", "2.11.3"]:
            self.targets[ver] = f"https://github.com/KDAB/GammaRay/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"GammaRay-{ver}"
            self.archiveNames[ver] = f"gammaray-{ver}.tar.gz"
        self.targetDigests["2.7.0"] = (
            ["74251d9de4bfa31994431c7a493e5de17d0b90853557a245bf3f7f4e0227fd14"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2.9.0"] = (
            ["f86159c77cff4aaf22feed6fb2ee012028df179f54e0e441642115f93ffc41b5"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2.10.0"] = (
            ["d9a816eb8f1ac1ae227d280d84ef23aee83e99fadc5269ef53d53d0aad5496d2"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2.10.1"] = (
            ["ac37103e4e4bcda7a5f48cfc187a797501ab92e30f712aeb20571896e6bce087"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.description = "GammaRay is a tool to poke around in a Qt-application and also to manipulate the application to some extent"
        self.webpage = "http://www.kdab.com/gammaray"
        self.displayName = "GammaRay"
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.defaultTarget = "master"
        else:
            self.defaultTarget = "2.11.3"

    def registerOptions(self):
        self.options.dynamic.registerOption("gammarayProbeOnly", False)
        self.options.dynamic.registerOption("disableGammarayBuildCliInjector", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["qt-apps/kdstatemachineeditor"] = None
        self.runtimeDependencies["libs/openssl"] = None
        probes = CraftPackageObject.get("kdab/gammaray-binary-probes")
        if probes and probes.isInstalled:
            self.runtimeDependencies["kdab/gammaray-binary-probes"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ["-DGAMMARAY_INSTALL_QT_LAYOUT=ON", "-DGAMMARAY_BUILD_DOCS=OFF"]

        nultiBuild = CraftPackageObject.get("libs/qt/qtbase").subinfo.options.dynamic.buildReleaseAndDebug
        self.subinfo.options.configure.args += [f"-DGAMMARAY_MULTI_BUILD={'ON' if nultiBuild else 'OFF'}"]

        if self.subinfo.options.dynamic.gammarayProbeOnly:
            self.subinfo.options.configure.args += ["-DGAMMARAY_PROBE_ONLY_BUILD=ON"]
        if self.subinfo.options.dynamic.disableGammarayBuildCliInjector:
            self.subinfo.options.configure.args += ["-DGAMMARAY_BUILD_CLI_INJECTOR=OFF"]

    def createPackage(self):
        self.subinfo.options.package.movePluginsToBin = False
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\gammaray-launcher.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "LICENSE.GPL.txt")
        self.defines["icon"] = os.path.join(self.sourceDir(), "ui", "resources", "gammaray", "GammaRay.ico")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return TypePackager.createPackage(self)
