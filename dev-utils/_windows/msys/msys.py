import io

import info
import shells

from CraftOS.osutils import OsUtils

from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "20180531"
        # don't set an actual version  instead of base. Msys must be manually updated so doing a craft update of msys wil break things.
        self.targets["base"] = f"http://repo.msys2.org/distrib/x86_64/msys2-base-x86_64-{ver}.tar.xz"
        self.targetDigests["base"] = (['8ef5b18c4c91f3f2394823f1981babdee78a945836b2625f091ec934b1a37d32'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64["base"] = (['4e799b5c3efcf9efcb84923656b7bcff16f75a666911abd6620ea8e5e1e9870c'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "base"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None
        self.runtimeDependencies["dev-utils/python3"] = None

    def msysInstallShim(self, installDir):
        return utils.createShim(os.path.join(installDir, "dev-utils", "bin", "msys.exe"),
                                os.path.join(installDir, "dev-utils", "bin", "python3.exe"),
                                args=os.path.join(CraftStandardDirs.craftBin(), "shells.py"))


from Package.BinaryPackageBase import *


class MsysPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.shell = shells.BashShell()

    def install(self):
        if CraftCore.compiler.isX64():
            utils.copyDir(os.path.join(self.sourceDir(), "msys64"), os.path.join(self.installDir(), "msys"))
        else:
            utils.copyDir(os.path.join(self.sourceDir(), "msys32"), os.path.join(self.installDir(), "msys"))
        return True

    def qmerge(self):
        if not self.subinfo.msysInstallShim(self.installDir()):
            return False
        return BinaryPackageBase.qmerge(self)

    def postQmerge(self):
        msysDir = os.path.join(CraftStandardDirs.craftRoot(), "msys")

        def autorebase():
            return (OsUtils.killProcess("*", msysDir) and
                    utils.system("autorebase.bat", cwd=msysDir))

        def queryForUpdate():
            out = io.BytesIO()
            if not self.shell.execute(".", "pacman", "-Sy --noconfirm --force"):
                raise Exception()
            self.shell.execute(".", "pacman", "-Qu --noconfirm", out=out, err=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        # start and restart msys before first use
        if not (self.shell.execute(".", "echo", "Firstrun") and
                autorebase() and
                self.shell.execute(".", "pacman-key", "--init") and
                self.shell.execute(".", "pacman-key", "--populate")):
            return False

        try:
            while queryForUpdate():
                if not (self.shell.execute(".", "pacman", "-Su --noconfirm --force --ask 20") and
                        autorebase()):
                    return False
        except Exception as e:
            print(e)
            return False
        return (self.shell.execute(".", "pacman", "-S base-devel --noconfirm --force --needed") and
                autorebase())


class VirtualPackage(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

    def install(self):
        if not VirtualPackageBase.install(self):
            return False
        return self.subinfo.msysInstallShim(self.installDir())


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        self.skipCondition = ("Paths", "Msys") not in CraftCore.settings
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=MsysPackage, classB=VirtualPackage)

        if not self.skipCondition:
            # override the install method
            def install():
                CraftCore.log.info(f"Using manually installed msys {CraftStandardDirs.msysDir()}")
                return self.baseClass.install(self)

            setattr(self, "install", install)
