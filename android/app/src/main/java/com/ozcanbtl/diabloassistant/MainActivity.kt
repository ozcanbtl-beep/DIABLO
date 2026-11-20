package com.ozcanbtl.diabloassistant

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.media.projection.MediaProjectionManager
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var status: TextView
    private val captureRequestCode = 4102
    private val overlayRequestCode = 4103

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pad = (18 * resources.displayMetrics.density).toInt()
        val column = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(pad, pad, pad, pad)
        }
        fun heading(text: String, size: Float = 20f) {
            column.addView(TextView(this).apply {
                this.text = text
                textSize = size
                setPadding(0, pad / 2, 0, pad / 2)
            })
        }
        heading("DIABLO Assistant", 26f)
        heading("Oyun üstü kontrol paneli", 18f)
        heading("Sınıf: Druid\nParagon: 1635\nÇarpışma Puanı: 62.000\nRezonans: 794\nHasar: 27.000\nCan: 338.000")
        heading("PvE becerileri", 19f)
        heading("Heyelan • Ateşli Hortum • Diken Zırh\nKuduz Kudret • Kuzgun Sürüsü")
        heading("Durum", 19f)
        status = TextView(this).apply {
            textSize = 15f
            text = "Kayan simge izni bekleniyor."
            setPadding(0, pad / 2, 0, pad)
        }
        column.addView(status)
        column.addView(Button(this).apply {
            text = "Oyun üstü simgeyi etkinleştir"
            setOnClickListener { requestOverlayPermission() }
        })
        column.addView(Button(this).apply {
            text = "Ekran paylaşım iznini iste"
            setOnClickListener { requestScreenPermission() }
        })
        heading("Nasıl kullanılır?", 19f)
        heading("İzin verdikten sonra Diablo Immortal'ı aç. Ekranın üstünde DIABLO simgesi kalır. Simgeye dokununca kontrol paneli açılır; Kapat düğmesiyle küçültüp oyuna dönersin.", 15f)
        heading("Not: Bu panel yalnızca arayüzdür. Şimdilik oyun içi dokunma veya otomatik savaş yapmaz.", 14f)
        setContentView(ScrollView(this).apply { addView(column) },
            ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
        if (Settings.canDrawOverlays(this)) startOverlayService()
    }

    private fun requestOverlayPermission() {
        if (Settings.canDrawOverlays(this)) {
            startOverlayService()
            status.text = "Kayan simge etkinleştirildi. Oyuna geçebilirsin."
        } else {
            val intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:$packageName"))
            startActivityForResult(intent, overlayRequestCode)
        }
    }

    private fun startOverlayService() {
        if (Settings.canDrawOverlays(this)) {
            val intent = Intent(this, OverlayControlService::class.java)
            startService(intent)
            status.text = "Kayan DIABLO simgesi etkin. Oyun üzerinde simgeye dokun."
        }
    }

    private fun requestScreenPermission() {
        val manager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        startActivityForResult(manager.createScreenCaptureIntent(), captureRequestCode)
    }

    @Deprecated("Deprecated by Android; retained for broad device compatibility")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == overlayRequestCode) {
            if (Settings.canDrawOverlays(this)) startOverlayService()
            else status.text = "Kayan simge izni verilmedi."
        } else if (requestCode == captureRequestCode) {
            status.text = if (resultCode == RESULT_OK && data != null)
                "Ekran paylaşım izni verildi; bu sürüm görüntüyü henüz işlemiyor."
            else "Ekran paylaşım izni verilmedi."
        }
    }
}