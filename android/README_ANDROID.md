# CrowdGuard Android development

## 1. Run Flask from VS Code
From the project root:

```powershell
python app.py
```

Keep Flask running.

## 2. Connect phone through USB
Enable Developer Options and USB debugging on the Android phone.

From Android SDK `platform-tools`:

```powershell
.\adb.exe devices
```

The phone should appear as `device`.

## 3. Reverse Flask port to the phone

```powershell
.\adb.exe reverse tcp:5000 tcp:5000
```

## 4. Run the Android project
Open `android/CrowdGuardAndroid` in Android Studio and run the app on the connected phone.

The WebView opens:

```text
http://127.0.0.1:5000/
```

Because of `adb reverse`, that address reaches Flask on the laptop.

## 5. Important
The Android app is a WebView shell. The Citizen and Guard UI is served by the Flask templates, so HTML/CSS/JS changes in VS Code appear after refreshing/reloading the WebView while Flask is running.

For a packaged APK used without the laptop, this architecture will later need a deployed backend or an on-device backend. `127.0.0.1:5000` is specifically the USB/ADB development configuration.
