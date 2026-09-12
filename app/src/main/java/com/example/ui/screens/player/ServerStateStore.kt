package com.example.ui.screens.player

object ServerStateStore {
    var currentMediaKey: String? = null
    var extractedServers: List<String> = emptyList()
    var extractedServerLinks: Map<String, String> = emptyMap()
    var extractedServerIds: Map<String, String> = emptyMap()
    var extractedDownloadLinks: Map<String, String> = emptyMap()
    var extractedQualities: List<com.example.utils.M3U8Parser.QualityInfo> = emptyList()
    
    fun clear() {
        currentMediaKey = null
        extractedServers = emptyList()
        extractedServerLinks = emptyMap()
        extractedServerIds = emptyMap()
        extractedDownloadLinks = emptyMap()
        extractedQualities = emptyList()
    }
}
