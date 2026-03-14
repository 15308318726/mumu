package org.kivy.android;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.util.Log;
import java.util.List;

public class PythonAccessibilityService extends AccessibilityService {
    private static final String TAG = "AutoCardAccessibility";
    private static AutoCardApp appInstance;

    public static void setAppInstance(AutoCardApp app) {
        appInstance = app;
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() != AccessibilityEvent.TYPE_NOTIFICATION_STATE_CHANGED) {
            return;
        }

        CharSequence title = event.getText().size() > 0 ? event.getText().get(0) : "";
        CharSequence text = event.getText().size() > 1 ? event.getText().get(1) : "";
        
        if (title.toString().contains("微信收款") || text.toString().contains("微信收款")) {
            Log.d(TAG, "收到微信收款通知：" + title + " - " + text);
            if (appInstance != null) {
                appInstance.onNotification(title.toString(), text.toString());
            }
        }
    }

    @Override
    public void onInterrupt() {
        Log.d(TAG, "无障碍服务被中断");
    }
}
