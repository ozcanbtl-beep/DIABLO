package com.ozcanbtl.diabloassistant

import android.app.Service
import android.content.Intent
import android.graphics.PixelFormat
import android.os.IBinder
import android.provider.Settings
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

    private fun params(width: Int, height: Int) =
        WindowManager.LayoutParams(
            width, height,
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        ).apply { gravity = Gravity.TOP or Gravity.END; x = 18; y = 180 }

    private fun showBubble() {
        if (bubble != null || !Settings.canDrawOverlays(this)) return
        bubble = Button(this).apply {
            text = "DIABLO"
            textSize = 12f
            setOnClickListener { showPanel() }
        }
        windowManager.addView(
            bubble,
            params((76 * resources.displayMetrics.density).toInt(), (52 * resources.displayMetrics.density).toInt())
        )
    }

    private fun showPanel() {
        if (panel != null) return
        val d = resources.displayMetrics.density
        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding((16*d).toInt(), (12*d).toInt(), (16*d).toInt(), (12*d).toInt())
            setBackgroundColor(0xEE20242A.toInt())
        }
        content.addView(TextView(this).apply {
            text = "DIABLO ASİSTAN\nPvE KONTROL PANELİ"
            textSize = 19f
            setTextColor(-1)
        })
        content.addView(TextView(this).apply {
            text = "Heyelan: temel saldırı\nAteş Hortumu • Dikenli Zırh\nKuduz Kudret • Kuzgun Sürüsü"
            textSize = 14f
            setTextColor(-1)
            setPadding(0, (10*d).toInt(), 0, (10*d).toInt())
        })
        content.addView(Button(this).apply {
            text = "OTOMATİK SALDIRIYI BAŞLAT"
            setOnClickListener {
                val start = Intent(this@OverlayControlService, GameTapAccessibilityService::class.java)
                    .setAction(GameTapAccessibilityService.ACTION_START)
                sendBroadcast(start.setPackage(packageName))
            }
        })
        content.addView(Button(this).apply {
            text = "SALDIRIYI DURDUR"
            setOnClickListener {
                val stop = Intent(this@OverlayControlService, GameTapAccessibilityService::class.java)
                    .setAction(GameTapAccessibilityService.ACTION_STOP)
                sendBroadcast(stop.setPackage(packageName))
            }
        })
        content.addView(Button(this).apply {
            text = "Ekran analizini başlat"
            setOnClickListener {
                hidePanel()
                val launch = Intent(this@OverlayControlService, MainActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                    .putExtra("REQUEST_CAPTURE", true)
                startActivity(launch)
            }
        })
        content.addView(Button(this).apply {
            text = "Ekran analizini durdur"
            setOnClickListener {
                stopService(Intent(this@OverlayControlService, ScreenCaptureService::class.java))
            }
        })
        content.addView(Button(this).apply { text = "Kapat ve oyuna dön"; setOnClickListener { hidePanel() } })
        panel = content
        windowManager.addView(
            content,
            params((292*d).toInt(), WindowManager.LayoutParams.WRAP_CONTENT).apply {
                gravity = Gravity.TOP or Gravity.CENTER_HORIZONTAL
                x = 0
                y = (100*d).toInt()
            }
        )
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