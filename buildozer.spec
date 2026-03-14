[app]
title = AutoCard
package.name = autocard
package.domain = org.autocard
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xml,java
version = 1.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests

android.api = 33
android.ndk = 25b
android.sdk = 24
android.archs = arm64-v8a,armeabi-v7a  # 移除注释中的中文和多余空格

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_NOTIFICATIONS,BIND_ACCESSIBILITY_SERVICE

android.add_manifest = <application android:allowBackup="true"><service android:name="org.kivy.android.PythonAccessibilityService" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE" android:exported="true"><intent-filter><action android:name="android.accessibilityservice.AccessibilityService"/></intent-filter><meta-data android:name="android.accessibilityservice" android:resource="@xml/accessibility_service"/></service></application>

android.accept_sdk_license = True
android.use_aapt2 = True
p4a.branch = master
