#SingleInstance Force
DetectHiddenWindows, On

; Activate Spotify window and send a key using SendInput.
sendKeyToSoftware(class, key) {
    WinGet, winState, MinMax, ahk_class %class%  ; Get current window state
    WinActivate, ahk_class %class%  ; Activate Spotify window
    SendInput, % key  ; Send the key
    if (winState == -1)  ; If window was previously minimized
        WinMinimize, ahk_class %class%  ; Minimize the window again
    Return
}

;Volume up
F14::
{
    sendKeyToSoftware("Chrome_WidgetWin_0", "^{Up}")
    Return
}

;Volume down
F15::
{
    sendKeyToSoftware("Chrome_WidgetWin_0", "^{Down}")
    Return
}

;Pause/Play
F16::
{
    sendKeyToSoftware("Chrome_WidgetWin_0", "{Space}")
    Return
}

;Back 15s
F17::
{
    sendKeyToSoftware("Chrome_WidgetWin_0", "+{Left}")
    Return
}

;Forward 15s
F18::
{
    sendKeyToSoftware("Chrome_WidgetWin_0", "+{Right}")
    Return
}
