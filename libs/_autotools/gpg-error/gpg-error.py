import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["1.43"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgpg-error-{ver}"
        self.targetDigests['1.43'] = (['a9ab83ca7acc442a5bd846a75b920285ff79bdb4e3d34aa382be88ed2c3aebaf'], CraftHash.HashAlgorithm.SHA256)
        self.description = "Small library with error codes and descriptions shared by most GnuPG related software"
        self.defaultTarget = "1.43"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

    def postInstall( self ):
        return (self.patchInstallPrefix([os.path.join(self.installDir(), "bin", "gpg-error-config"),
                                         os.path.join(self.installDir(), "bin", "gpgrt-config")],
                        OsUtils.toMSysPath(self.subinfo.buildPrefix),
                        OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot())))
