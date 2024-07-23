    Section "Un.Cleanup Stray Files"
        RMDir /r /rebootok  $INSTDIR\bin
        RMDir /REBOOTOK $INSTDIR
    SectionEnd
    
    Section "Un.Cleanup Regsistry"
        SetRegView 64
        DeleteRegKey SHCTX "Software\Classes\CLSID\${DIFF_EXT_CLSID}"
        DeleteRegKey SHCTX "Software\Classes\*\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
        DeleteRegKey SHCTX "Software\Classes\Folder\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
        DeleteRegKey SHCTX "Software\Classes\Directory\shellex\ContextMenuHandlers\${DIFF_EXT_ID}"
        DeleteRegValue SHCTX "Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved" "${DIFF_EXT_CLSID}"
        DeleteRegValue SHCTX "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers\" "$INSTDIR\bin\kdiff3.exe"
    SectionEnd
    