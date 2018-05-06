import info

from Package.BinaryPackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):

    def setTargets(self):
        for ver in ["2.13.03", "2.14"]:
            if CraftCore.compiler.isMSVC():
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/win{CraftCore.compiler.bits}/nasm-{ver}-win{CraftCore.compiler.bits}.zip"
            else:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/stable/nasm-{ver}.tar.bz2"

            self.targetInstSrc[ver] = f"nasm-{ver}"
            if CraftCore.compiler.isMSVC():
                self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
            else:
                self.targetInstallPath[ver] = "dev-utils"

        if CraftCore.compiler.isMSVC():
            self.targetDigestsX64['2.13.03'] = (['b3a1f896b53d07854884c2e0d6be7defba7ebd09b864bbb9e6d69ada1c3e989f'], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests['2.13.03'] = (['046ed0b14f8b874863dd43e0534ad47727b022194278f2f79df108c7357afcff'], CraftHash.HashAlgorithm.SHA256)
            self.targetDigestsX64['2.14'] = (['eb63653ed3fc8f3a3bb082f2ed7a04a9b676a6b1994095467f0ac79213d1152f'], CraftHash.HashAlgorithm.SHA256)

        self.description = "This is NASM - the famous Netwide Assembler"
        self.webpage = "https://www.nasm.us/"
        self.defaultTarget = "2.14"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None

if CraftCore.compiler.isMSVC():
    class Package(BinaryPackageBase):
        def __init__(self):
            BinaryPackageBase.__init__(self)
else:
    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)

