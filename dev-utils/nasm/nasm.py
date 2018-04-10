import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.13.03"]:
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/win{CraftCore.compiler.bits}/nasm-{ver}-win{CraftCore.compiler.bits}.zip"
            elif CraftCore.compiler.isMacOS:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/macosx/nasm-{ver}-macosx.zip"
            self.targetInstSrc[ver] = f"nasm-{ver}"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        if CraftCore.compiler.isWindows:
            self.targetDigestsX64['2.13.03'] = (['b3a1f896b53d07854884c2e0d6be7defba7ebd09b864bbb9e6d69ada1c3e989f'], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests['2.13.03'] = (['046ed0b14f8b874863dd43e0534ad47727b022194278f2f79df108c7357afcff'], CraftHash.HashAlgorithm.SHA256)

        self.description = "This is NASM - the famous Netwide Assembler"
        self.webpage = "https://www.nasm.us/"
        self.defaultTarget = "2.13.03"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
