; Computer-side actions for the macropad's Media page (AutoHotkey v1).
; Run at login, e.g. put a shortcut to this file in shell:startup.
;
;   F19        volume 0%
;   F24        unmute, volume 100%
;   Shift+F19  Spotify seek back
;   Shift+F24  Spotify seek forward

#SingleInstance Force
DetectHiddenWindows, On

SPOTIFY := "Chrome_WidgetWin_0"  ; Spotify desktop app's window class

; Activate a window, send it a key with SendInput, then restore its minimised state.
sendKeyToSoftware(class, key) {
    WinGet, winState, MinMax, ahk_class %class%
    WinActivate, ahk_class %class%
    SendInput, % key
    if (winState == -1)  ; Was minimised
        WinMinimize, ahk_class %class%
    Return
}

F19::SoundSet, 0

F24::
    SoundSet, 0, MASTER, MUTE  ; 0 = mute off
    SoundSet, 100
Return

+F19::sendKeyToSoftware(SPOTIFY, "+{Left}")
+F24::sendKeyToSoftware(SPOTIFY, "+{Right}")
