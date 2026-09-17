package com.example.ui.screens.profile

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.db.AppDatabase
import com.example.data.model.SupportMessage
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class SupportViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = AppDatabase.getDatabase(application).supportDao()

    val messages: StateFlow<List<SupportMessage>> = dao.getAllMessages()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    init {
        viewModelScope.launch {
            if (dao.getMessageCount() == 0) {
                // Initial greeting message
                dao.insertMessage(
                    SupportMessage(
                        text = "Hi! 👋\nWelcome to CineStream Support.\nHow can we help you today?",
                        isFromUser = false
                    )
                )
            }
        }
    }

    fun sendMessage(text: String) {
        if (text.isBlank()) return
        
        viewModelScope.launch {
            // User message
            dao.insertMessage(SupportMessage(text = text.trim(), isFromUser = true))
            
            // Simulate bot thinking
            delay(1000)
            
            val response = generateResponse(text.trim())
            dao.insertMessage(SupportMessage(text = response, isFromUser = false))
        }
    }
    
    private fun generateResponse(input: String): String {
        val lower = input.lowercase()
        return when {
            lower.contains("premium") || lower.contains("plan") -> "Sure! I'll be happy to help you with that. What would you like to know about the premium plan?"
            lower.contains("device") || lower.contains("multiple") -> "Yes! You can use your CineStream premium account on up to 5 devices at the same time. If you need anything else, feel free to ask."
            lower.contains("hello") || lower.contains("hi") -> "Hello there! How can I assist you today?"
            lower.contains("issue") || lower.contains("problem") || lower.contains("playback") -> "I'm sorry to hear you're experiencing an issue. Could you please provide more details so I can assist you better?"
            else -> "Thank you for reaching out. A support agent will review your message and get back to you shortly."
        }
    }
}
