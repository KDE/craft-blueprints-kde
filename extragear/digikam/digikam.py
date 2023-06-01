# -*- coding: utf-8 -*-
# Copyright (c) 2019-2022 by Gilles Caulier <caulier dot gilles at gmail dot com>
# Copyright (c) 2019-2020 by Ben Cooksley <bcooksley at kde dot org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# NOTE: see relevant phabricator entry https://phabricator.kde.org/T12071

import info
import utils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/digikam.git"
        self.defaultTarget = "master"
        self.displayName = "digiKam"
        self.webpage = "https://www.digikam.org"
        self.description = "Professional Photo Management with the Power of Open Source"

    def setDependencies(self):
        # For i18n extraction

        if CraftCore.compiler.isWindows or CraftCore.compiler.isMacOS:
            self.buildDependencies["dev-utils/subversion"] = None
            self.buildDependencies["dev-utils/ruby"] = None

        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/flexbison"] = None

        # Android ffmpeg is broken.

        if not CraftCore.compiler.isAndroid:
            # digiKam mediaPlayer is not yet fully ported to FFMPEG 5 API

            self.runtimeDependencies["libs/ffmpeg"] = "4.4"

        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/x265"] = None
        self.runtimeDependencies["libs/libass"] = None
        self.runtimeDependencies["libs/tiff"] = None

        if CraftCore.compiler.isLinux or CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/libgphoto2"] = None
            self.runtimeDependencies["libs/libusb-compat"] = None

        # do not force boost deps (see: https://phabricator.kde.org/T12071#212690)

        # self.runtimeDependencies["libs/boost/boost-system"]            = None
        # self.runtimeDependencies["libs/boost"]                         = None

        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["libs/lensfun"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/openal-soft"] = None
        self.runtimeDependencies["libs/pthreads"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libass"] = None
        self.runtimeDependencies["libs/libusb"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtimageformats"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["libs/qt5/qtnetworkauth"] = None

        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None

        if CraftCore.compiler.isMinGW():
            # mingw-based builds need this

            self.runtimeDependencies["libs/runtime"] = None

            self.buildDependencies["libs/boost/boost-graph"] = None

            # QtWebEngine do not compile with MinGW

            self.runtimeDependencies["libs/qt5/qtwebkit"] = None

        else:
            self.runtimeDependencies["libs/qt5/qtwebengine"] = None

        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None

        # For Panorama export tool.

        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None

        # For Calendar export plugin.

        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None

        # For some digiKam plugins used to export on web services.

        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None

        # To support more formats in digiKam Qt plugin image loaders.

        self.runtimeDependencies["kde/frameworks/tier1/kimageformats"] = None

        # Install libmarble, plugins and data for geolocation.
        # Marble application will be removed at packaging stage.

        self.runtimeDependencies["kde/applications/marble"] = None

        # To support Mysql database

        self.runtimeDependencies["binary/mysql"] = None


from Package.CMakePackageBase import *
from Packager.AppxPackager import AppxPackager
from Utils import GetFiles


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=ON"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=ON"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_PO=ON"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_DIGIKAM=ON"

        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=ON"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_PO=ON"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_DIGIKAM=ON"

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=ON"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=ON"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_PO=ON"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_DIGIKAM=ON"

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=ON"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_PO=ON"
            self.subinfo.options.configure.args += f" -DDIGIKAMSC_COMPILE_DIGIKAM=ON"

    def createPackage(self):
        self.defines["productname"] = "digiKam"
        self.defines["website"] = "https://www.digikam.org"
        self.defines["company"] = "digiKam.org"
        self.defines["license"] = os.path.join(self.sourceDir(), "COPYING")

        # Not yet supported by Craft with NSIS
        # self.defines["readme"]      = os.path.join(self.packageDir(), "ABOUT.txt")

        # In AppImage, run the new startup script sctip with advanced features.

        self.defines["runenv"] = [
            'APPIMAGE_EXTRACT_AND_RUN=1 && "$this_dir"/usr/bin/AppRun.digiKam "$@" && exit',
        ]

        # Windows-only, mac is handled implicitly

        self.defines["executable"] = "bin\\digikam.exe"

        # Windows-only

        self.defines["icon"] = os.path.join(self.packageDir(), "digikam.ico")

        # Windows-only extra icons

        self.defines["icon_png"] = os.path.join(self.sourceDir(), "core", "data", "icons", "apps", "128-apps-digikam.png")

        # Windows-only application shortcuts

        self.defines["shortcuts"] = [
            {"name": "digiKam", "target": "bin/digikam.exe", "description": self.subinfo.description, "icon": "$INSTDIR\\digikam.ico"},
            {"name": "Showfoto", "target": "bin/showfoto.exe", "description": "digiKam stand alone Image Editor", "icon": "$INSTDIR\\showfoto.ico"},
        ]

        # Files to drop from the bundles

        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_common.txt"))

        if CraftCore.compiler.isWindows:
            self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_win.txt"))

        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_mac.txt"))

        if CraftCore.compiler.isLinux:
            self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_lin.txt"))

        # Drop dbus support for non Linux target

        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return TypePackager.createPackage(self)

    def preArchive(self):
        # Copy More application icons in Windows bundle.

        if CraftCore.compiler.isWindows:
            if not utils.copyFile(os.path.join(self.packageDir(), "showfoto.ico"), os.path.join(self.archiveDir(), "showfoto.ico")):
                print("Could not copy showfoto.ico file")
                return False

        if CraftCore.compiler.isMSVC():
            # Manage files under Windows bundle:

            # remove setup_vars_opencv4.cmd               (blacklist.txt)
            # remove Marble LICENSE                       (blacklist.txt)

            # See bug #455232:
            # - move astro.dll to digiKam/bin/
            # - move marbledeclarative.dll to digiKam/bin/
            # - move marblewidget-qt5.dll to digiKam/bin/
            # - move data/ to digiKam/data
            # - remove marble-qt.exe                      (blacklist.txt)

            archiveDir = self.archiveDir()
            binPath = os.path.join(archiveDir, "bin")

            if not utils.moveFile(os.path.join(archiveDir, "astro.dll"), os.path.join(binPath, "astro.dll")):
                print("Could not move astro.dll file")
                return False

            if not utils.moveFile(os.path.join(archiveDir, "marbledeclarative.dll"), os.path.join(binPath, "marbledeclarative.dll")):
                print("Could not move marbledeclarative.dll file")
                return False

            if not utils.moveFile(os.path.join(archiveDir, "marblewidget-qt5.dll"), os.path.join(binPath, "marblewidget-qt5.dll")):
                print("Could not move marblewidget-qt5.dll file")
                return False

            if not utils.mergeTree(os.path.join(archiveDir, "data"), os.path.join(binPath, "data")):
                print("Could not move Marble data dir")
                return False

            # Move translations/ to bin/translations/

            #  if not utils.moveFile(os.path.join(archiveDir,  "translations"),
            #                        os.path.join(binPath,     "translations")):
            #      print("Could not move Qt translations dir")
            #      return False

            # Move digiKam plugins from bin/digikam/ to bin/plugins/digikam/

            pluginsPath = os.path.join(archiveDir, "bin", "plugins")
            utils.createDir(pluginsPath)

            if not utils.moveFile(os.path.join(archiveDir, "bin", "digikam"), os.path.join(pluginsPath, "digikam")):
                print("Could not move digiKam plugins dir")
                return False

            # Move bin/*marble_plugins*.dll to bin/plugins/

            pluginsLst = [
                "AnnotatePlugin.dll",
                "AprsPlugin.dll",
                "AtmospherePlugin.dll",
                "CachePlugin.dll",
                "CompassFloatItem.dll",
                "CrosshairsPlugin.dll",
                "CycleStreetsPlugin.dll",
                "EarthquakePlugin.dll",
                "EclipsesPlugin.dll",
                "ElevationProfileFloatItem.dll",
                "ElevationProfileMarker.dll",
                "FlightGearPositionProviderPlugin.dll",
                "FoursquarePlugin.dll",
                "GeoUriPlugin.dll",
                "GosmoreReverseGeocodingPlugin.dll",
                "GosmoreRoutingPlugin.dll",
                "GpsbabelPlugin.dll",
                "GpsInfo.dll",
                "GpxPlugin.dll",
                "GraticulePlugin.dll",
                "HostipPlugin.dll",
                "JsonPlugin.dll",
                "KmlPlugin.dll",
                "LatLonPlugin.dll",
                "License.dll",
                "LocalDatabasePlugin.dll",
                "LocalOsmSearchPlugin.dll",
                "MapQuestPlugin.dll",
                "MapScaleFloatItem.dll",
                "MeasureTool.dll",
                "MonavPlugin.dll",
                "NavigationFloatItem.dll",
                "NominatimReverseGeocodingPlugin.dll",
                "NominatimSearchPlugin.dll",
                "NotesPlugin.dll",
                "OpenLocationCodeSearchPlugin.dll",
                "OpenRouteServicePlugin.dll",
                "OsmPlugin.dll",
                "OSRMPlugin.dll",
                "OverviewMap.dll",
                "Pn2Plugin.dll",
                "PntPlugin.dll",
                "PositionMarker.dll",
                "PostalCode.dll",
                "ProgressFloatItem.dll",
                "RoutingPlugin.dll",
                "RoutinoPlugin.dll",
                "SatellitesPlugin.dll",
                "Speedometer.dll",
                "StarsPlugin.dll",
                "SunPlugin.dll",
                "YoursPlugin.dll",
            ]

            for dll in pluginsLst:
                if not utils.moveFile(os.path.join(binPath, dll), os.path.join(pluginsPath, dll)):
                    print("Could not move Marble plugin " + dll)
                    return False

            # Download exiftool.exe in the bundle

            if not GetFiles.getFile("https://files.kde.org/digikam/exiftool/exiftool.zip", binPath, "exiftool.zip"):
                print("Could not get ExifTool archive")
                return False

            if not utils.unpackFile(binPath, "exiftool.zip", binPath):
                print("Could not unpack ExifTool archive")
                return False

            if not utils.moveFile(os.path.join(binPath, "exiftool(-k).exe"), os.path.join(binPath, "exiftool.exe")):
                print("Could not rename ExifTool binary")
                return False

            if not utils.deleteFile(os.path.join(binPath, "exiftool.zip")):
                print("Could not remove ExifTool archive")
                return False

        if CraftCore.compiler.isLinux:
            # --- Manage files under AppImage bundle

            archiveDir = self.archiveDir()
            binPath = os.path.join(archiveDir, "bin")

            # Download exiftool in the bundle

            if not GetFiles.getFile("https://files.kde.org/digikam/exiftool/Image-ExifTool.tar.gz", binPath, "Image-ExifTool.tar.gz"):
                print("Could not get ExifTool archive")
                return False

            if not utils.unpackFile(binPath, "Image-ExifTool.tar.gz", binPath):
                print("Could not unpack ExifTool archive")
                return False

            binfiles = os.listdir(binPath)
            etname = None

            for f in binfiles:
                if f.startswith("Image-ExifTool-"):
                    etname = f
                    break

            if not utils.moveFile(os.path.join(binPath, etname), os.path.join(binPath, "Image-ExifTool")):
                print("Could not rename ExifTool directory")
                return False

            os.symlink(os.path.join("./", "Image-ExifTool", "exiftool"), os.path.join(self.archiveDir(), "bin", "exiftool"))

            if not utils.deleteFile(os.path.join(binPath, "Image-ExifTool.tar.gz")):
                print("Could not remove ExifTool archive")
                return False

            # Replace AppImage AppRun script by own one with advanced features.

            if not utils.copyFile(os.path.join(self.packageDir(), "AppRun"), os.path.join(binPath, "AppRun.digiKam")):
                print("Could not copy AppImage startup script")
                return False

        if CraftCore.compiler.isMacOS:
            # --- Manage files under MacOS package

            archiveDir = self.archiveDir()
            binPath = os.path.join(archiveDir, "bin")

            # Download exiftool in the bundle

            if not GetFiles.getFile("https://files.kde.org/digikam/exiftool/Image-ExifTool.tar.gz", binPath, "Image-ExifTool.tar.gz"):
                print("Could not get ExifTool archive")
                return False

            if not utils.unpackFile(binPath, "Image-ExifTool.tar.gz", binPath):
                print("Could not unpack ExifTool archive")
                return False

            binfiles = os.listdir(binPath)
            etname = None

            for f in binfiles:
                if f.startswith("Image-ExifTool-"):
                    etname = f
                    break

            if not utils.moveFile(os.path.join(binPath, etname), os.path.join(binPath, "Image-ExifTool")):
                print("Could not rename ExifTool directory")
                return False

            os.symlink(os.path.join("./", "Image-ExifTool", "exiftool"), os.path.join(self.archiveDir(), "bin", "exiftool"))

            if not utils.deleteFile(os.path.join(binPath, "Image-ExifTool.tar.gz")):
                print("Could not remove ExifTool archive")
                return False

        return True
