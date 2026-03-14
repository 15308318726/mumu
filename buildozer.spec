[app]
# 应用基本信息
title = AutoCard
package.name = autocard
package.domain = org.autocard
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xml,java
version = 1.0

# 依赖库
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests

# 安卓配置
android.api = 33
android.ndk = 25b
android.sdk = 24
android.archs = arm64-v8a, armeabi-v7a  # 适配绝大多数安卓手机

# 关键权限（无障碍+通知+网络）
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_NOTIFICATIONS,BIND_ACCESSIBILITY_SERVICE

# 注册无障碍服务（核心！）
android.add_manifest = <application android:allowBackup="true"><service android:name="org.kivy.android.PythonAccessibilityService" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE" android:exported="true"><intent-filter><action android:name="android.accessibilityservice.AccessibilityService"/></intent-filter><meta-data android:name="android.accessibilityservice" android:resource="@xml/accessibility_service"/></service></application>

# 其他配置
android.accept_sdk_license = True
android.use_aapt2 = True
p4a.branch = master