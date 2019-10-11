import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["1.27", "1.31"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgpg-error-{ver}"
        self.patchToApply["1.31"] = [("libgpg-error-1.31.diff", 1)]
        self.targetDigests['1.27'] = (['4f93aac6fecb7da2b92871bb9ee33032be6a87b174f54abf8ddf0911a22d29d2'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.31'] =  (['40d0a823c9329478063903192a1f82496083b277265904878f4bc09e0db7a4ef'], CraftHash.HashAlgorithm.SHA256)
        self.description = "Small library with error codes and descriptions shared by most GnuPG related software"
        self.patchLevel["1.31"] = 2
        self.defaultTarget = "1.31"

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
