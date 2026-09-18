package com.example.data.model

data class P2PTransferRecord(
    val id: String,
    val mediaId: String,
    val title: String,
    val posterUrl: String,
    val isMovie: Boolean,
    val isReceived: Boolean, // true = received, false = sent
    val timestamp: Long,
    val deviceName: String = "",
    val quality: String = ""
)
