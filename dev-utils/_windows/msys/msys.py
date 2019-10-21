import io

import info
import shells

from CraftOS.osutils import OsUtils

from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "20181211"
        # don't set an actual version  instead of base. Msys must be manually updated so doing a craft update of msys wil break things.
        self.targets["base"] = f"http://repo.msys2.org/distrib/x86_64/msys2-base-x86_64-{ver}.tar.xz"
        self.targetInstSrc["base"] = "msys64"
        self.targetInstallPath["base"] = "msys"
        self.targetDigests["base"] = (['5cab863861bc9d414b4df2cbe0b1bf8b560eb9a19aa637afabd6f436b572f2e3'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "base"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None
        self.runtimeDependencies["dev-utils/python3"] = None

    def msysInstallShim(self, installDir):
        return utils.createShim(os.path.join(installDir, "dev-utils", "bin", "msys.exe"),
                                os.path.join(installDir, "dev-utils", "bin", "python3.exe"),
                                args=[os.path.join(CraftStandardDirs.craftBin(), "shells.py")])

    def updateMsys(self):
        msysDir = CraftCore.settings.get("Paths", "Msys", os.path.join(CraftStandardDirs.craftRoot(), "msys"))
        shell = shells.BashShell()

        def stopProcesses():
            return OsUtils.killProcess("*", msysDir)

        def queryForUpdate():
            out = io.BytesIO()
            if not shell.execute(".", "pacman", "-Sy --noconfirm --force"):
                raise Exception()
            shell.execute(".", "pacman", "-Qu --noconfirm", stdout=out, stderr=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        # start and restart msys before first use
        if not (shell.execute(".", "echo", "Firstrun") and
                stopProcesses() and
                shell.execute(".", "pacman-key", "--init") and
                shell.execute(".", "pacman-key", "--populate")):
            return False

        try:
            while queryForUpdate():
                if not (shell.execute(".", "pacman", "-Su --noconfirm --force --ask 20") and
                        stopProcesses()):
                    return False
        except Exception as e:
            CraftCore.log.error(e, exc_info=e)
            return False
        if not (shell.execute(".", "pacman", "-S base-devel msys/binutils --noconfirm --force --needed") and
                stopProcesses()):
            return False
        return utils.system("autorebase.bat", cwd=msysDir)


from Package.BinaryPackageBase import *


class MsysPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return self.subinfo.msysInstallShim(self.imageDir())

    def postQmerge(self):
        return self.subinfo.updateMsys()

class VirtualPackage(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

    def install(self):
        if not VirtualPackageBase.install(self):
            return False
        return self.subinfo.msysInstallShim(self.imageDir()) and self.subinfo.updateMsys()

    def qmerge(self):
        if self.package.isInstalled:
            return True
        return super().qmerge()

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        useExternalMsys = ("Paths", "Msys") not in CraftCore.settings
        self.skipCondition = useExternalMsys and not CraftPackageObject.get("dev-utils/msys").isInstalled
        MaybeVirtualPackageBase.__init__(self, condition=self.skipCondition, classA=MsysPackage, classB=VirtualPackage)
        if not useExternalMsys:
            # override the install method
            def install():
                CraftCore.log.info(f"Using manually installed msys {CraftStandardDirs.msysDir()}")
                return self.baseClass.install(self)

            setattr(self, "install", install)
