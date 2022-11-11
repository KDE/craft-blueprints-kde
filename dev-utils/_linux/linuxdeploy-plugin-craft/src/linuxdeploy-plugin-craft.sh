#! /bin/bash
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2022 KDE e.V.
# SPDX-FileContributor: Ingo Klöcker <dev@ingo-kloecker.de>

# exit whenever a command called in this script fails
set -eo pipefail

appdir=""

show_usage() {
    echo "Usage: bash $0 --appdir <AppDir>"
}

while [ "$1" != "" ]; do
    case "$1" in
        --plugin-api-version)
            echo "0"
            exit 0
            ;;
        --appdir)
            appdir="$2"
            shift
            shift
            ;;
        *)
            echo "Invalid argument: $1"
            echo
            show_usage
            exit 2
    esac
done

if [[ "$appdir" == "" ]]; then
    show_usage
    exit 2
fi

cd ${appdir}/usr
plugins=$(find plugins -type f)
for p in ${plugins}; do
    fullpath=${appdir}/usr/${p}
    old_rpath=$(strings ${p} | grep ORIGIN || true)
    if [[ -n ${old_rpath} ]]; then
        relative_lib_path=$(dirname ${p} | sed "s;[^/]*;..;g")/lib
        new_rpath='$ORIGIN/'${relative_lib_path}:'$ORIGIN'
        #echo "Old patched rpath in ELF file ${fullpath} is ${old_rpath}"
        echo "Setting rpath in ELF file ${fullpath} to ${new_rpath}"
        patchelf --set-rpath "${new_rpath}" ${p}
    else
        echo "Not setting rpath in file ${fullpath}"
    fi
done
