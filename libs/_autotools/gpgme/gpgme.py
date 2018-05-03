import info
import CraftCore


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["1.9.0", "1.11.1"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/gpgme/gpgme-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"gpgme-{ver}"

        self.targetDigests["1.9.0"] = (["1b29fedb8bfad775e70eafac5b0590621683b2d9869db994568e6401f4034ceb"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11.1"] = (["2d1b111774d2e3dd26dcd7c251819ce4ef774ec5e566251eb9308fa7542fbd6f"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.9.0"] = [("gpgme-1.9.0-20170801.diff", 1)]
        #self.patchToApply["1.11.1"] = [("gpgme-1.1.11-20170801.diff", 1)]

        self.description = "GnuPG cryptography support library (runtime)"
        self.defaultTarget = "1.11.1"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/gpg-error"] = "default"
        self.runtimeDependencies["libs/assuan2"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        if OsUtils.isWin():
            self.subinfo.options.configure.args = "--enable-languages=no"
        else:
            self.subinfo.options.configure.args = "--enable-languages=cpp,qt"
        self.subinfo.options.configure.args += " --disable-gpg-test"

    def configure(self):
        if OsUtils.isMac():
            # The configure script does not honnor the env var is PKG_CONFIG is not installed / env var not set
            # This is problematic especially on macOS, let manually fill the env var to make configure happy finding Qt
            PKG_CONFIG = ":"
            # Gpgme rely on pkg-config to discover Qt, but pkg config files are not shipped / generated...
            # So we need to help it to discover Qt
            _, QT_BINS = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_BINS")
            _, QT_LIBS = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_LIBS")
            if QT_BINS:
                QT_BINS = QT_BINS.strip();
            else:
                print("Invalid or missing Qt installation")
                return False
            if QT_LIBS:
                QT_LIBS = QT_LIBS.strip();
            else:
                print("Invalid or missing Qt installation")
                return False
            MOC = f"{QT_BINS}/moc"
            GPGME_QT_CFLAGS = f"-F{QT_LIBS} -I{QT_LIBS}/QtCore.framework/Headers -DQT_NO_DEBUG -DQT_CORE_LIB"
            GPGME_QT_LIBS = f"-F{QT_LIBS} -framework QtCore"
            GPGME_QTTEST_CFLAGS = f"-F{QT_LIBS} -I{QT_LIBS}/QtTest.framework/Headers -DQT_NO_DEBUG -DQT_TEST_LIB"
            GPGME_QTTEST_LIBS = f"-F{QT_LIBS} -framework QtTest"
            self.subinfo.options.configure.args += (f" PKG_CONFIG='{PKG_CONFIG}'"
                f" MOC='{MOC}'"
                f" GPGME_QT_CFLAGS='{GPGME_QT_CFLAGS}'"
                f" GPGME_QT_LIBS='{GPGME_QT_LIBS}'"
                f" GPGME_QTTEST_CFLAGS='{GPGME_QTTEST_CFLAGS}'"
                f" GPGME_QTTEST_LIBS='{GPGME_QTTEST_LIBS}'")
        return AutoToolsPackageBase.configure(self)

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
