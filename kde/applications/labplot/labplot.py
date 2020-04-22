import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Interactive graphing and analysis of scientific data"
        self.webpage = "https://labplot.kde.org/"
        self.displayName = "LabPlot2"

        for ver in ['2.5.0', '2.6.0', '2.7.0']:
            self.targets[ver] = 'http://download.kde.org/stable/labplot/%s/labplot-%s.tar.xz' % (ver, ver)
        for ver in ['2.6.0']:
            self.targetInstSrc[ver] = 'labplot-2.6'
        for ver in ['2.5.0', '2.7.0']:
            self.targetInstSrc[ver] = 'labplot-%s' % ver

        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/png2ico"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/liblz4"] = None
        self.runtimeDependencies["libs/hdf5"] = None
        # netcdf disabled for MSVC until build on binary factory works
        if not CraftCore.compiler.isMSVC():
            self.runtimeDependencies["libs/netcdf"] = None
        self.runtimeDependencies["kde/applications/cantor"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtserialport"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += "-DENABLE_TESTS=OFF"
        # cerf.h is not found when using libcerf from ports
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += " -DENABLE_LIBCERF=OFF"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        self.defines["appname"] = "labplot2"
        self.defines["website"] = "https://labplot.kde.org/"
        self.defines["executable"] = "bin\\labplot2.exe"
        self.defines["shortcuts"] = [{"name" : "LabPlot2", "target" : "bin/labplot2.exe", "description" : self.subinfo.description, "icon" : "$INSTDIR\\labplot2.ico" }]
        self.defines["icon"] = os.path.join(self.packageDir(), "labplot2.ico")
        #self.defines["icon_png"] = os.path.join(self.packageDir(), ".assets", "150-apps-okular.png")
        #self.defines["icon_png_44"] = os.path.join(self.packageDir(), ".assets", "44-apps-okular.png")

        # SHChangeNotify(SHCNE_ASSOCCHANGED,SHCNF_FLUSH,0,0)
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0, SHCNF_FLUSH = 0x1000, SHCNF_FLUSHNOWAIT = 0x2000
        self.defines["registry_hook"] = ("""WriteRegStr SHCTX "Software\\Classes\\.lml" "" "LabPlot2"\n"""
            """WriteRegStr SHCTX "Software\\Classes\\LabPlot2" "" "LabPlot2 project"\n"""
            """WriteRegStr SHCTX "Software\\Classes\\LabPlot2\\DefaultIcon" "" "$INSTDIR\\bin\\data\\labplot2\\application-x-labplot2.ico"\n"""
            """WriteRegStr SHCTX "Software\\Classes\\LabPlot2\\shell" "" "open"\n"""
            """WriteRegStr SHCTX "Software\\Classes\\LabPlot2\\shell\\open\\command" "" '"$INSTDIR\\bin\\labplot2.exe" "%1"'\n"""
            """System::Call "shell32::SHChangeNotify(i,i,i,i) (0x08000000, 0x1000, 0, 0)"\n""")

        # add option for desktop shortcut (see kdeconnect-kde.py)
        self.defines["sections"] = r"""
            Section "Desktop Shortcut"
                    CreateShortCut "$DESKTOP\\@{productname}.lnk" "$INSTDIR\\bin\\@{appname}.exe"
            SectionEnd
            """
        self.defines["un_sections"] = r"""
            Section "Un.Remove Shortcuts"
                Delete "$DESKTOP\\@{productname}.lnk"
            SectionEnd
            """

        if isinstance(self, AppxPackager):
            self.defines["display_name"] = "LabPlot"
        else:
            self.defines["mimetypes"] = ["application/x-labplot2"]
        self.defines["file_types"] = [".lml"]

        return TypePackager.createPackage(self)

