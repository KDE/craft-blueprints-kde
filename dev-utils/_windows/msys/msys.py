import io

import info
import shells

from CraftOS.osutils import OsUtils

from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        #as updates are applied with msys and not by craft don't ever change the name of the target, its a bad idea...
        self.targets["base"] = f"https://github.com/msys2/msys2-installer/releases/download/2020-05-22/msys2-base-x86_64-20200522.tar.xz"
        self.targetInstSrc["base"] = "msys64"
        self.targetInstallPath["base"] = "msys"
        self.targetDigests["base"] =  (['deec23a772774d874b557bcc5dfb2a8a115224fb6a919f19062af108b6bf4735'], CraftHash.HashAlgorithm.SHA256)

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
        useOverwrite = CraftCore.cache.checkCommandOutputFor(os.path.join(msysDir, "usr/bin", "pacman.exe"), "--overwrite", "-Sh")

        # force was replace by overwrite
        overwrite = "--overwrite='*'" if useOverwrite else "--force"

        def stopProcesses():
            return OsUtils.killProcess("*", msysDir)

        def queryForUpdate():
            out = io.BytesIO()
            if not shell.execute(".", "pacman", f"-Sy --noconfirm {overwrite}"):
                raise Exception()
            shell.execute(".", "pacman", "-Qu --noconfirm", stdout=out, stderr=subprocess.PIPE)
            out = out.getvalue()
            return out != b""

        # start and restart msys before first use
        if not (shell.execute(".", "echo", "Init update") and
                stopProcesses() and
                shell.execute(".", "pacman-key", "--init") and
                shell.execute(".", "pacman-key", "--populate")):
            return False

        try:
            # max 10 tries
            for _ in range(10):
                if not queryForUpdate():
                    break
                # might return 1 on core updates...
                shell.execute(".", "pacman", f"-Su --noconfirm {overwrite} --ask 20")
                if not stopProcesses():
                    return False
        except Exception as e:
            CraftCore.log.error(e, exc_info=e)
            return False
        if not (shell.execute(".", "pacman", f"-S base-devel msys/binutils --noconfirm {overwrite} --needed") and
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
