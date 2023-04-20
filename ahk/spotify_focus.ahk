; adapted from https://gist.github.com/jcsteh/7ccbc6f7b1b7eb85c1c14ac5e0d65195

#SingleInstance Force
DetectHiddenWindows, On

; Get the HWND of the software's main window.
getSoftwareHwnd(processExe) {
	WinGet, softwareHwnd, ID, ahk_exe %processExe%
	; We need the app's third top level window, so get next twice.
	; Not needed for newer versions of app!
	; softwareHwnd := DllCall("GetWindow", "uint", softwareHwnd, "uint", 2)
	; softwareHwnd := DllCall("GetWindow", "uint", softwareHwnd, "uint", 2)
	Return softwareHwnd
}

; Send a key to a software.
sendKeyToSoftware(processExe, key, method) {
	softwareHwnd := getsoftwareHwnd(processExe)
	if  WinExist("A") != softwareHwnd {
		if (method == "PostMessage" ) {
			PostMessage, 0x319,, 0xE0000,, ahk_id %softwareHwnd%
		}
		if (method == "ControlSend" ) {
			; Chromium ignores keys when it isn't focused.
			; Focus the document window without bringing the app to the foreground.
			ControlFocus, Chrome_RenderWidgetHostHWND1, ahk_id %softwareHwnd%
			ControlSend, , %key%, ahk_id %softwareHwnd%
		}
	} else {
		Send %key%
	}
	Return
}

;Volume up
F14::
{
	sendKeyToSoftware("spotify.exe","^{Up}", "ControlSend")
	Return
}

;Volume down
F15::
{
	sendKeyToSoftware("spotify.exe","^{Down}", "ControlSend")
	Return
}

;Pause/Play
F16::
{
	sendKeyToSoftware("spotify.exe","{Space}", "ControlSend")
	Return
}

;Back 15s
F17::
{
	sendKeyToSoftware("spotify.exe","+{Left}", "ControlSend")
	Return
}

;Forward 15s
F18::
{
	sendKeyToSoftware("spotify.exe","+{Right}", "ControlSend")
	Return
}