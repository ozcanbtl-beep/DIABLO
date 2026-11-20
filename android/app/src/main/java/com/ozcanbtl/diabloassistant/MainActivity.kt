package com.ozcanbtl.diabloassistant

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.media.projection.MediaProjectionManager
import android.os.Bundle
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var status: TextView
    private val captureRequestCode = 4102

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
        heading("Android yardımcı uygulama • İlk prototip", 15f)
        heading("Karakter profili", 19f)
        heading("Sınıf: Druid\nParagon: 1635\nÇarpışma Puanı: 62.000\nRezonans: 794\nHasar: 27.000\nCan: 338.000")
        heading("PvE becerileri", 19f)
        heading("Heyelan • Ateşli Hortum • Diken Zırh\nKuduz Kudret • Kuzgun Sürüsü")
        heading("Durum", 19f)
        status = TextView(this).apply {
            text = "Henüz ekran izni verilmedi. Bu prototip oyun içinde dokunma yapmaz ve otomatik savaşmaz."
            textSize = 15f
            setPadding(0, pad / 2, 0, pad)
        }
        column.addView(status)

        column.addView(Button(this).apply {
            text = "Ekran paylaşım iznini iste"
            setOnClickListener { requestScreenPermission() }
        })
        column.addView(Button(this).apply {
            text = "İzin durumunu sıfırla"
            setOnClickListener {
                status.text = "Durum sıfırlandı. Ekran kaydı başlatılmadı."
            }
        })
        heading("Güvenlik", 19f)
        heading("Ekran paylaşımı Android'in sistem penceresiyle onaylanır. Bu sürüm yalnızca izin akışını doğrular; görüntü kaydetmez, dokunma göndermez, oyun belleğine erişmez ve anti-cheat atlatmaz.", 14f)

        val scroll = ScrollView(this).apply {
            addView(column)
        }
        setContentView(scroll, ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        ))
    }

    private fun requestScreenPermission() {
        val manager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        startActivityForResult(manager.createScreenCaptureIntent(), captureRequestCode)
    }

    @Deprecated("Deprecated by Android; retained for broad device compatibility in this prototype")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == captureRequestCode) {
            status.text = if (resultCode == RESULT_OK && data != null) {
                "Android ekran paylaşım iznini verdi. Bu ilk prototip görüntüyü henüz yakalamıyor veya kaydetmiyor."
            } else {
                "Ekran paylaşım izni verilmedi. Uygulama normal şekilde bekliyor."
            }
        }
    }
}
