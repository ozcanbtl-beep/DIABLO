package com.ozcanbtl.diabloassistant

import android.app.Service
import android.content.Intent
import android.graphics.PixelFormat
import android.os.IBinder
import android.view.Gravity
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView

class OverlayControlService : Service() {
    private lateinit var windowManager: WindowManager
    private var bubble: View? = null
    private var panel: View? = null

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        showBubble()
    }

    private fun params(width: Int, height: Int) = WindowManager.LayoutParams(
        width, height, WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
        WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
        PixelFormat.TRANSLUCENT
    ).apply { gravity = Gravity.TOP or Gravity.END; x = 18; y = 180 }

    private fun showBubble() {
        if (bubble != null) return
        val button = Button(this).apply {
            text = "DIABLO"
            textSize = 12f
            setOnClickListener { showPanel() }
        }
        bubble = button
        windowManager.addView(button, params(
            (76 * resources.displayMetrics.density).toInt(),
            (52 * resources.displayMetrics.density).toInt()
        ))
    }

    private fun showPanel() {
        if (panel != null) return
        val density = resources.displayMetrics.density
        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding((16*density).toInt(), (12*density).toInt(), (16*density).toInt(), (12*density).toInt())
            setBackgroundColor(0xEE20242A.toInt())
        }
        content.addView(TextView(this).apply {
            text = "DIABLO ASİSTAN\nKontrol Paneli"
            textSize = 20f
            setTextColor(0xFFFFFFFF.toInt())
        })
        content.addView(TextView(this).apply {
            text = "PvE profili: Druid • Paragon 1635\nPanel hazır. Otomatik savaş henüz etkin değil."
            textSize = 14f
            setTextColor(0xFFFFFFFF.toInt())
            setPadding(0, (12*density).toInt(), 0, (12*density).toInt())
        })
        content.addView(Button(this).apply {
            text = "Kapat ve oyuna dön"
            setOnClickListener { hidePanel() }
        })
        panel = content
        windowManager.addView(content, params(
            (280*density).toInt(), WindowManager.LayoutParams.WRAP_CONTENT
        ).apply { gravity = Gravity.TOP or Gravity.CENTER_HORIZONTAL; x = 0; y = (100*density).toInt() })
    }

    private fun hidePanel() {
        panel?.let { windowManager.removeView(it) }
        panel = null
    }

    override fun onDestroy() {
        hidePanel()
        bubble?.let { windowManager.removeView(it) }
        bubble = null
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}