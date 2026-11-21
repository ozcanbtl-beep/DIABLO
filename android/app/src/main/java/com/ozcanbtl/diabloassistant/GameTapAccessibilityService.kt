package com.ozcanbtl.diabloassistant

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.Intent
import android.graphics.Path
import android.os.Handler
import android.os.Looper
import android.view.accessibility.AccessibilityEvent

class GameTapAccessibilityService : AccessibilityService() {
    companion object {
        const val ACTION_START = "com.ozcanbtl.diabloassistant.START_ATTACK"
        const val ACTION_STOP = "com.ozcanbtl.diabloassistant.STOP_ATTACK"
    }

    private val handler = Handler(Looper.getMainLooper())
    private var running = false
    private var step = 0

    override fun onServiceConnected() {
        super.onServiceConnected()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START -> startAttack()
            ACTION_STOP -> stopAttack()
        }
        return START_STICKY
    }

    private fun startAttack() {
        if (running) return
        running = true
        step = 0
        handler.post(attackLoop)
    }

    private fun stopAttack() {
        running = false
        handler.removeCallbacksAndMessages(null)
    }

    private val attackLoop = object : Runnable {
        override fun run() {
            if (!running) return
            val w = resources.displayMetrics.widthPixels.toFloat()
            val h = resources.displayMetrics.heightPixels.toFloat()

            // Landscape standard-layout estimate: four skill buttons along the lower-right,
            // primary attack above/right. These are provisional tap zones, not enemy detection.
            val taps = listOf(
                Pair(0.72f, 0.86f), // Ateş Hortumu
                Pair(0.79f, 0.86f), // Dikenli Zırh
                Pair(0.86f, 0.86f), // Kuduz Kudret
                Pair(0.93f, 0.86f), // Kuzgun Sürüsü
                Pair(0.95f, 0.69f)  // Heyelan / temel saldırı
            )
            val (xRatio, yRatio) = taps[step % taps.size]
            dispatchTap(w * xRatio, h * yRatio)
            step++
            handler.postDelayed(this, if (step % taps.size == 0) 220L else 420L)
        }
    }

    private fun dispatchTap(x: Float, y: Float) {
        val path = Path().apply { moveTo(x, y) }
        val gesture = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, 70))
            .build()
        dispatchGesture(gesture, null, null)
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {}
    override fun onInterrupt() { stopAttack() }
    override fun onDestroy() { stopAttack(); super.onDestroy() }
}