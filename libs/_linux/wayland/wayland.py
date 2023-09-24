import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.22.0"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/wayland/wayland/-/releases/{ver}/downloads/wayland-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"wayland-{ver}"
        self.targetDigests["1.22.0"] = (["1540af1ea698a471c2d8e9d288332c7e0fd360c8f1d12936ebb7e7cbc2425842"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Core Wayland window system code and protocol"

        self.defaultTarget = "1.22.0"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-Ddocumentation=false"]

    def install(self):
        if not super().install():
            return False
        pkgConfigSrc = self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()) / "pkgconfig"
        pkgConfigDest = self.installDir() / "lib/pkgconfig"
        if pkgConfigSrc.exists():
            return utils.createDir(pkgConfigDest.parent) and utils.moveFile(pkgConfigSrc, pkgConfigDest)
        return True
