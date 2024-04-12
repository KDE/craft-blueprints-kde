from Package.AutoToolsPackageBase import *
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.18.1"]:
            self.targets[ver] = f"https://ftp.osuosl.org/pub/rpm/releases/rpm-{'.'.join(ver.split('.')[:2])}.x/rpm-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"rpm-{ver}"
            self.targetInstallPath[ver] = "dev-utils/rpm/"

        self.targetDigests["4.18.1"] = (["37f3b42c0966941e2ad3f10fde3639824a6591d07197ba8fd0869ca0779e1f56"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["4.18.1"] = 2

        self.defaultTarget = "4.18.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/gtk-doc"] = None
        self.runtimeDependencies["libs/nss"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/lua"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--with-crypto=libgcrypt", "--disable-static", "--enable-shared"]
        # on centos it does not automagically link intl so make it explicit
        self.subinfo.options.configure.ldflags += " -lintl"

    def postInstall(self):
        for x in ["rpmbuild", "rpmsign"]:
            if not utils.createShim(
                os.path.join(self.imageDir(), "dev-utils", "bin", x),
                os.path.join(self.imageDir(), "dev-utils", "rpm", f"bin/{x}"),
                env={
                    "RPM_CONFIGDIR": CraftCore.standardDirs.craftRoot() / "dev-utils/rpm/lib/rpm",
                    "LD_LIBRARY_PATH": CraftCore.standardDirs.craftRoot() / "lib",
                },
            ):
                return False
        return True
