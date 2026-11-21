package com.ozcanbtl.diabloassistant

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.PixelFormat
import android.hardware.display.DisplayManager
import android.hardware.display.VirtualDisplay
import android.media.ImageReader
import android.media.projection.MediaProjection
import android.media.projection.MediaProjectionManager
import android.os.Build
import android.os.IBinder
import android.util.DisplayMetrics
import android.view.WindowManager

class ScreenCaptureService : Service() {
    companion object {
        const val EXTRA_RESULT_CODE="projection_result_code"
        const val EXTRA_DATA="projection_data"
        private const val CHANNEL="diablo_screen_analysis"
        private const val NOTIFICATION_ID=4104
    }
    private var projection:MediaProjection?=null
    private var reader:ImageReader?=null
    private var display:VirtualDisplay?=null
    private var frameCount=0L

    override fun onStartCommand(intent:Intent?,flags:Int,startId:Int):Int {
        if(intent==null) { stopSelf(); return START_NOT_STICKY }
        createChannel()
        val notification=Notification.Builder(this,CHANNEL)
            .setSmallIcon(android.R.drawable.ic_menu_view)
            .setContentTitle("DIABLO ekran analizi")
            .setContentText("Ekran akışı açık; görüntüler kaydedilmiyor.")
            .setOngoing(true).build()
        if(Build.VERSION.SDK_INT>=29) startForeground(NOTIFICATION_ID,notification,android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION)
        else startForeground(NOTIFICATION_ID,notification)

        val resultCode=intent.getIntExtra(EXTRA_RESULT_CODE,0)
        @Suppress("DEPRECATION")
        val data=intent.getParcelableExtra<Intent>(EXTRA_DATA)
        if(data==null || resultCode==0) { stopSelf(); return START_NOT_STICKY }
        try {
            val manager=getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
            projection=manager.getMediaProjection(resultCode,data)
            val metrics=DisplayMetrics()
            @Suppress("DEPRECATION")
            (getSystemService(Context.WINDOW_SERVICE) as WindowManager).defaultDisplay.getRealMetrics(metrics)
            reader=ImageReader.newInstance(metrics.widthPixels,metrics.heightPixels,PixelFormat.RGBA_8888,2)
            reader?.setOnImageAvailableListener({ source ->
                val image=source.acquireLatestImage()
                if(image!=null) { frameCount++; image.close() }
            },null)
            display=projection?.createVirtualDisplay("DiabloScreenAnalysis",metrics.widthPixels,metrics.heightPixels,metrics.densityDpi,
                DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,reader?.surface,null,null)
            projection?.registerCallback(object:MediaProjection.Callback() {
                override fun onStop() { stopSelf() }
            },null)
        } catch (_:SecurityException) { stopSelf() }
        return START_NOT_STICKY
    }

    private fun createChannel() {
        if(Build.VERSION.SDK_INT>=26) {
            val channel=NotificationChannel(CHANNEL,"DIABLO ekran analizi",NotificationManager.IMPORTANCE_LOW)
            (getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager).createNotificationChannel(channel)
        }
    }
    override fun onDestroy() {
        display?.release(); display=null
        reader?.close(); reader=null
        projection?.stop(); projection=null
        stopForeground(STOP_FOREGROUND_REMOVE)
        super.onDestroy()
    }
    override fun onBind(intent:Intent?):IBinder?=null
}