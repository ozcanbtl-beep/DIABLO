package com.ozcanbtl.diabloassistant

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.graphics.Path
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.view.accessibility.AccessibilityEvent

class GameTapAccessibilityService : AccessibilityService() {
    companion object {
        const val ACTION_START = "com.ozcanbtl.diabloassistant.START_ATTACK"
        const val ACTION_STOP = "com.ozcanbtl.diabloassistant.STOP_ATTACK"
    }

    private val handler = Handler(Looper.getMainLooper())
    private var running = false
    private var receiverRegistered = false
    private var nextSkillIndex = 0
    private val skillCooldownsMs = longArrayOf(9_000L, 9_000L, 15_000L, 6_000L)
    private var nextSkillAt = LongArray(skillCooldownsMs.size)

    // Fixed landscape positions: Fire Tornado, Thorn Armor, Rabid Might, Raven Swarm.
    // Landslide / primary attack is intentionally excluded.
    private val skillTaps = listOf(
        Pair(0.72f, 0.86f),
        Pair(0.79f, 0.86f),
        Pair(0.86f, 0.86f),
        Pair(0.93f, 0.86f)
    )

    private val commandReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            when (intent?.action) {
                ACTION_START -> startAttack()
                ACTION_STOP -> stopAttack()
            }
        }
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        if (!receiverRegistered) {
            val filter = IntentFilter().apply {
                addAction(ACTION_START)
                addAction(ACTION_STOP)
            }
            if (Build.VERSION.SDK_INT >= 33) {
                registerReceiver(commandReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
            } else {
                @Suppress("DEPRECATION")
                registerReceiver(commandReceiver, filter)
            }
            receiverRegistered = true
        }
    }

    private fun startAttack() {
        if (running) return
        running = true
        val now = SystemClock.uptimeMillis()
        nextSkillAt = LongArray(skillCooldownsMs.size) { index ->
            now + index * 250L
        }
        nextSkillIndex = 0
        handler.post(attackLoop)
    }

    private fun stopAttack() {
        running = false
        handler.removeCallbacks(attackLoop)
    }

    private val attackLoop = object : Runnable {
        override fun run() {
            if (!running) return

            val now = SystemClock.uptimeMillis()
            var selected = -1
            for (offset in skillTaps.indices) {
                val index = (nextSkillIndex + offset) % skillTaps.size
                if (now >= nextSkillAt[index]) {
                    selected = index
                    break
                }
            }

            if (selected >= 0) {
                val w = resources.displayMetrics.widthPixels.toFloat()
                val h = resources.displayMetrics.heightPixels.toFloat()
                val (xRatio, yRatio) = skillTaps[selected]
                dispatchTap(w * xRatio, h * yRatio)
                nextSkillAt[selected] = now + skillCooldownsMs[selected]
                nextSkillIndex = (selected + 1) % skillTaps.size
                handler.postDelayed(this, 180L)
            } else {
                val nextReadyAt = nextSkillAt.minOrNull() ?: (now + 500L)
                handler.postDelayed(this, (nextReadyAt - now).coerceAtLeast(80L))
            }
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

    override fun onDestroy() {
        stopAttack()
        if (receiverRegistered) {
            unregisterReceiver(commandReceiver)
            receiverRegistered = false
        }
        super.onDestroy()
    }
}
