import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux
        )

    def setTargets(self):
        for ver in ["16.15.1"]:
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://nodejs.org/dist/v{ver}/node-v{ver}-win-x64.zip"
                self.targetInstSrc[ver] = f"node-v{ver}-win-x64"
            elif CraftCore.compiler.isMacOS:
                if CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64:
                    self.targets[ver] = f"https://nodejs.org/dist/v{ver}/node-v{ver}-darwin-x64.tar.gz"
                    self.targetInstSrc[ver] = f"node-v{ver}-darwin-x64"
                else:
                    self.targets[ver] = f"https://nodejs.org/dist/v{ver}/node-v{ver}-darwin-arm64.tar.gz"
                    self.targetInstSrc[ver] = f"node-v{ver}-darwin-arm64"
            elif CraftCore.compiler.isLinux:
                self.targets[ver] = f"https://nodejs.org/dist/v{ver}/node-v{ver}-linux-x64.tar.xz"
                self.targetInstSrc[ver] = f"node-v{ver}-linux-x64"

            self.targetInstallPath[ver] = os.path.join("dev-utils", "nodejs")
            self.targetDigestUrls[ver] = (f"https://nodejs.org/dist/v{ver}/SHASUMS256.txt.asc", CraftHash.HashAlgorithm.SHA256)

        self.description = "Node.js® is a JavaScript runtime built on Chrome's V8 JavaScript engine."
        self.webpage = "https://nodejs.org"

        self.patchLevel["16.15.1"] = 1

        self.defaultTarget = "16.15.1"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        sourceBinary = self.installDir()
        if not CraftCore.compiler.isWindows:
            sourceBinary /= "bin"
        sourceBinary /= f"node{CraftCore.compiler.executableSuffix}"
        targetBinary = self.imageDir() / f"dev-utils/bin/node{CraftCore.compiler.executableSuffix}"

        return utils.createShim(targetBinary, sourceBinary)

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
