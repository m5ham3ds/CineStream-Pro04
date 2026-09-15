import re

with open("app/src/main/java/com/example/data/repository/UserPreferencesRepository.kt", "r") as f:
    content = f.read()

keys = """
    private val MAX_CONCURRENT_DOWNLOADS = intPreferencesKey("max_concurrent_downloads")
    private val MAX_SEGMENTS = intPreferencesKey("max_segments")
    private val DOWNLOAD_NETWORK = intPreferencesKey("download_network") // 0=All, 1=WiFi
"""

flows = """
    val maxConcurrentDownloads: Flow<Int> = context.dataStore.data.map { it[MAX_CONCURRENT_DOWNLOADS] ?: 3 }
    val maxSegments: Flow<Int> = context.dataStore.data.map { it[MAX_SEGMENTS] ?: 8 }
    val downloadNetwork: Flow<Int> = context.dataStore.data.map { it[DOWNLOAD_NETWORK] ?: 0 }
"""

methods = """
    suspend fun saveMaxConcurrentDownloads(count: Int) {
        context.dataStore.edit { it[MAX_CONCURRENT_DOWNLOADS] = count }
    }
    suspend fun saveMaxSegments(count: Int) {
        context.dataStore.edit { it[MAX_SEGMENTS] = count }
    }
    suspend fun saveDownloadNetwork(network: Int) {
        context.dataStore.edit { it[DOWNLOAD_NETWORK] = network }
    }
"""

if "MAX_CONCURRENT_DOWNLOADS" not in content:
    content = content.replace("val onboardingCompleted", keys + "\n    val onboardingCompleted")
    content = content.replace("val startScreen: Flow<String> = context.dataStore.data.map { it[START_SCREEN] ?: \"home\" }", "val startScreen: Flow<String> = context.dataStore.data.map { it[START_SCREEN] ?: \"home\" }\n" + flows)
    content = content + "\n" + methods + "\n}"
    
    # fix duplicate bracket
    content = content.replace("}\n\n    suspend fun", "\n    suspend fun")

with open("app/src/main/java/com/example/data/repository/UserPreferencesRepository.kt", "w") as f:
    f.write(content)
