package com.example.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "user_prefs")

class UserPreferencesRepository(private val context: Context) {
    private val ONBOARDING_COMPLETED = booleanPreferencesKey("onboarding_completed")
    private val IS_GUEST = booleanPreferencesKey("is_guest")
    private val IS_LOGGED_IN = booleanPreferencesKey("is_logged_in")
    
    // New Settings Keys
    private val THEME_MODE = intPreferencesKey("theme_mode") // 0 = System, 1 = Light, 2 = Dark
    private val PRIMARY_COLOR = intPreferencesKey("primary_color") // 0 = Default(Red), 1 = Blue, 2 = Green, 3 = Purple, 4 = Orange
    private val APP_LANGUAGE = stringPreferencesKey("app_language") // "system", "en", "ar"
    private val START_SCREEN = stringPreferencesKey("start_screen") // "home", "search", "downloads", "settings"

    val onboardingCompleted: Flow<Boolean> = context.dataStore.data.map { it[ONBOARDING_COMPLETED] ?: false }
    val isGuest: Flow<Boolean> = context.dataStore.data.map { it[IS_GUEST] ?: false }
    val isLoggedIn: Flow<Boolean> = context.dataStore.data.map { it[IS_LOGGED_IN] ?: false }
    
    val themeMode: Flow<Int> = context.dataStore.data.map { it[THEME_MODE] ?: 0 }
    val primaryColor: Flow<Int> = context.dataStore.data.map { it[PRIMARY_COLOR] ?: 0 }
    val appLanguage: Flow<String> = context.dataStore.data.map { it[APP_LANGUAGE] ?: "system" }
    val startScreen: Flow<String> = context.dataStore.data.map { it[START_SCREEN] ?: "home" }

    suspend fun saveOnboardingCompleted(completed: Boolean) {
        context.dataStore.edit { it[ONBOARDING_COMPLETED] = completed }
    }
    suspend fun saveIsGuest(isGuest: Boolean) {
        context.dataStore.edit { it[IS_GUEST] = isGuest }
    }
    suspend fun saveIsLoggedIn(isLoggedIn: Boolean) {
        context.dataStore.edit { it[IS_LOGGED_IN] = isLoggedIn }
    }
    suspend fun saveThemeMode(mode: Int) {
        context.dataStore.edit { it[THEME_MODE] = mode }
    }
    suspend fun savePrimaryColor(color: Int) {
        context.dataStore.edit { it[PRIMARY_COLOR] = color }
    }
    suspend fun saveAppLanguage(lang: String) {
        context.dataStore.edit { it[APP_LANGUAGE] = lang }
    }
    suspend fun saveStartScreen(screen: String) {
        context.dataStore.edit { it[START_SCREEN] = screen }
    }
}
