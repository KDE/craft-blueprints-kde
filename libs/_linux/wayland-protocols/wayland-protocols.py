import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.31"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/wayland/wayland-protocols/-/releases/{ver}/downloads/wayland-protocols-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"wayland-protocols-{ver}"
        self.targetDigests["1.31"] = (["a07fa722ed87676ec020d867714bc9a2f24c464da73912f39706eeef5219e238"], CraftHash.HashAlgorithm.SHA256)

        self.description = "wayland-protocols contains Wayland protocols that add functionality not available in the Wayland core protocol."

        self.defaultTarget = "1.31"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-Dtests=false"]

    def install(self):
        if not super().install():
            return False
        pkgConfigSrc = self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()) / "pkgconfig"
        pkgConfigDest = self.installDir() / "lib/pkgconfig"
        if pkgConfigSrc.exists():
            return utils.createDir(pkgConfigDest.parent) and utils.moveFile(pkgConfigSrc, pkgConfigDest)
        return True
