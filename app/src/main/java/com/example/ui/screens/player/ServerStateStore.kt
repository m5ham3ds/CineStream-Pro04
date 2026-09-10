package com.example.ui.screens.player

object ServerStateStore {
    var extractedServers: List<String> = emptyList()
    var extractedServerLinks: Map<String, String> = emptyMap()
    var extractedServerIds: Map<String, String> = emptyMap()
    
    fun clear() {
        extractedServers = emptyList()
        extractedServerLinks = emptyMap()
        extractedServerIds = emptyMap()
    }
}
