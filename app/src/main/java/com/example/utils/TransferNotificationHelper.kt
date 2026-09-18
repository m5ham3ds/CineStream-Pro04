package com.example.utils

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import com.example.R

object TransferNotificationHelper {
    private const val CHANNEL_ID = "p2p_transfer_channel"
    private const val NOTIFICATION_ID_PROGRESS = 1001
    private const val NOTIFICATION_ID_STATUS = 1002

    fun initChannel(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "File Transfers"
            val descriptionText = "Notifications for offline P2P file transfers"
            val importance = NotificationManager.IMPORTANCE_LOW
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    fun showConnectionNotification(context: Context, deviceName: String) {
        initChannel(context)
        try {
            val notification = NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle(context.getString(R.string.connected_to, deviceName))
                .setContentText("Connected and ready to share media files")
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .setAutoCancel(true)
                .build()

            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.notify(NOTIFICATION_ID_STATUS, notification)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun showTransferProgress(context: Context, title: String, progressPercent: Int, isSender: Boolean) {
        initChannel(context)
        try {
            val actionText = if (isSender) "Sending" else "Receiving"
            val notification = NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("$actionText: $title")
                .setContentText("$progressPercent% completed")
                .setProgress(100, progressPercent, false)
                .setOngoing(true)
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .build()

            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.notify(NOTIFICATION_ID_PROGRESS, notification)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun showTransferComplete(context: Context, title: String, isSender: Boolean) {
        initChannel(context)
        try {
            val actionText = if (isSender) "Sent" else "Received"
            val notification = NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("Transfer Complete")
                .setContentText("Successfully $actionText $title (100%)")
                .setProgress(0, 0, false)
                .setOngoing(false)
                .setAutoCancel(true)
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                .build()

            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.notify(NOTIFICATION_ID_PROGRESS, notification)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun cancelProgressNotification(context: Context) {
        try {
            val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.cancel(NOTIFICATION_ID_PROGRESS)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
