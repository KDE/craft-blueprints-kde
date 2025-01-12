import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/GammaRay.git"
        for ver in ["2.11.3", "3.0.0"]:
            self.targets[ver] = f"https://github.com/KDAB/GammaRay/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"GammaRay-{ver}"
            self.archiveNames[ver] = f"gammaray-{ver}.tar.gz"
        self.targetDigests["2.10.1"] = (
            ["ac37103e4e4bcda7a5f48cfc187a797501ab92e30f712aeb20571896e6bce087"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["3.0.0"] = (["27fb2412e9edae75de23df94cd8330ad1dd579837d47b491709c13d625e3ac68"], CraftHash.HashAlgorithm.SHA256)

        self.description = "GammaRay is a tool to poke around in a Qt-application and also to manipulate the application to some extent"
        self.webpage = "https://www.kdab.com/gammaray"
        self.displayName = "GammaRay"
        self.defaultTarget = "master"

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


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = ["-DGAMMARAY_INSTALL_QT_LAYOUT=ON", "-DGAMMARAY_BUILD_DOCS=OFF"]

        nultiBuild = CraftPackageObject.get("libs/qt/qtbase").subinfo.options.dynamic.buildReleaseAndDebug
        self.subinfo.options.configure.args += [f"-DGAMMARAY_MULTI_BUILD={nultiBuild.asOnOff}"]

        if self.subinfo.options.dynamic.gammarayProbeOnly:
            self.subinfo.options.configure.args += ["-DGAMMARAY_PROBE_ONLY_BUILD=ON"]
        if self.subinfo.options.dynamic.disableGammarayBuildCliInjector:
            self.subinfo.options.configure.args += ["-DGAMMARAY_BUILD_CLI_INJECTOR=OFF"]

    def createPackage(self):
        self.subinfo.options.package.movePluginsToBin = False
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\gammaray-launcher.exe"
        self.defines["license"] = self.sourceDir() / "LICENSE.GPL.txt"
        self.defines["icon"] = self.sourceDir() / "ui/resources/gammaray/GammaRay.ico"
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
