package com.example.extensions

import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.util.Log
import dalvik.system.PathClassLoader
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.Locale

class ExtensionReflectionWrapper(private val instance: Any) : ProviderExtension {
    private val clazz = instance.javaClass
    
    override val id: String get() = clazz.getMethod("getId").invoke(instance) as String
    override val name: String get() = clazz.getMethod("getName").invoke(instance) as String
    override val baseUrl: String get() = clazz.getMethod("getBaseUrl").invoke(instance) as String
    override val isAnime: Boolean get() = clazz.getMethod("isAnime").invoke(instance) as Boolean
    override val isMovie: Boolean get() = clazz.getMethod("isMovie").invoke(instance) as Boolean
    override val isSeries: Boolean get() = clazz.getMethod("isSeries").invoke(instance) as Boolean
    override val lang: String get() = clazz.getMethod("getLang").invoke(instance) as String
    override val iconUrl: String get() = clazz.getMethod("getIconUrl").invoke(instance) as String

    override fun getSearchUrl(titleOriginal: String, titleClean: String): String {
        return clazz.getMethod("getSearchUrl", String::class.java, String::class.java)
            .invoke(instance, titleOriginal, titleClean) as String
    }

    override fun getExtractionScript(isMovie: Boolean, episode: Int, title: String): String {
        return clazz.getMethod("getExtractionScript", Boolean::class.java, Int::class.java, String::class.java)
            .invoke(instance, isMovie, episode, title) as String
    }
}

object ExtensionManager {
    private const val PREFS_NAME = "extensions_prefs"
    private const val INSTALLED_KEY = "installed_extensions"
    private lateinit var prefs: SharedPreferences
    
    // Store all available extensions
    private val _availableExtensions = mutableListOf<ProviderExtension>()
    val availableExtensions: List<ProviderExtension> get() = _availableExtensions

    // Reactive state for installed extensions
    private val _installedExtensions = MutableStateFlow<List<ProviderExtension>>(emptyList())
    val installedExtensions: StateFlow<List<ProviderExtension>> = _installedExtensions.asStateFlow()

    fun init(context: Context) {
        prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        scanExternalExtensions(context)
        loadInstalled()
    }

    private fun scanExternalExtensions(context: Context) {
        try {
            val pm = context.packageManager
            val packages = pm.getInstalledPackages(PackageManager.GET_META_DATA)
            
            for (pkg in packages) {
                val isPlural = pkg.packageName.startsWith("com.aistudio.cinestream.xyzabc.extensions.")
                val isSingular = pkg.packageName.startsWith("com.aistudio.cinestream.xyzabc.extension.")
                if (isPlural || isSingular) {
                    try {
                        val appInfo = pkg.applicationInfo
                        val sourceDir = appInfo?.sourceDir
                        if (sourceDir == null) continue
                        val classLoader = PathClassLoader(sourceDir, null, context.classLoader)
                        
                        // Extract site name from package (e.g., egydead)
                        val prefix = if (isPlural) "com.aistudio.cinestream.xyzabc.extensions." else "com.aistudio.cinestream.xyzabc.extension."
                        val suffix = pkg.packageName.substringAfter(prefix)
                        val capitalizedSuffix = suffix.replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() }
                        
                        // Account for different naming styles that might occur
                        val classNamesToTry = mutableListOf<String>()
                        val baseNames = listOf(
                            "${capitalizedSuffix}Extension",
                            "EgyDeadExtension",
                            "EgydeadExtension",
                            "${suffix}Extension",
                            "${suffix.uppercase()}Extension",
                            "${capitalizedSuffix}Provider",
                            "EgyDeadProvider",
                            "EgydeadProvider",
                            "MainExtension",
                            "ExtensionImpl",
                            "EgyDead",
                            "Egydead",
                            capitalizedSuffix,
                            "ProviderExtension",
                            "Extension"
                        )
                        
                        val namespaces = listOf(
                            pkg.packageName,
                            "${pkg.packageName}.providers",
                            "${pkg.packageName}.extension",
                            "com.example",
                            "com.example.providers",
                            "com.example.extension",
                            "com.example.extensions",
                            "com.example.extensions.providers",
                            "com.example.${suffix}",
                            "com.example.${suffix}.providers",
                            "com.example.extension.${suffix}",
                            "com.aistudio.cinestream.xyzabc.extensions.${suffix}",
                            "com.aistudio.cinestream.xyzabc.extension.${suffix}",
                            "com.aistudio.cinestream.xyzabc.extensions.${suffix}.providers",
                            "com.aistudio.cinestream.xyzabc.extension.${suffix}.providers"
                        )
                        
                        for (ns in namespaces) {
                            for (name in baseNames) {
                                classNamesToTry.add("$ns.$name")
                            }
                        }
                        
                        // Also try without any package just in case (unlikely but possible)
                        classNamesToTry.addAll(baseNames)
                        
                        var extensionInstance: Any? = null
                        var lastError: Exception? = null
                        for (className in classNamesToTry) {
                            try {
                                val extensionClass = classLoader.loadClass(className)
                                // Try to get Kotlin object INSTANCE first
                                extensionInstance = try {
                                    val instanceField = extensionClass.getDeclaredField("INSTANCE")
                                    instanceField.get(null)
                                } catch (e: Exception) {
                                    // Fallback to regular instantiation
                                    extensionClass.newInstance()
                                }
                                if (extensionInstance != null) {
                                    Log.d("ExtensionManager", "Found extension class: $className")
                                    break
                                }
                            } catch (e: Exception) {
                                lastError = e
                                // Try next naming convention
                            }
                        }
                        
                        if (extensionInstance != null) {
                            val wrapper = ExtensionReflectionWrapper(extensionInstance)
                            if (_availableExtensions.none { it.id == wrapper.id }) {
                                _availableExtensions.add(wrapper)
                                Log.d("ExtensionManager", "Successfully loaded external APK extension: ${wrapper.name} from ${pkg.packageName}")
                            }
                        } else {
                            Log.e("ExtensionManager", "Could not find a matching Extension class in ${pkg.packageName}")
                        }
                    } catch (e: Exception) {
                        Log.e("ExtensionManager", "Failed to load extension APK ${pkg.packageName}", e)
                    }
                }
            }
        } catch (e: Exception) {
             Log.e("ExtensionManager", "Failed to scan packages", e)
        }
    }

    fun registerExtension(extension: ProviderExtension) {
        if (_availableExtensions.none { it.id == extension.id }) {
            _availableExtensions.add(extension)
        }
    }

    private fun loadInstalled() {
        val installedIds = prefs.getStringSet(INSTALLED_KEY, emptySet()) ?: emptySet()
        val installed = _availableExtensions.filter { it.id in installedIds }
        _installedExtensions.value = installed
    }

    fun installExtension(extensionId: String) {
        val currentIds = prefs.getStringSet(INSTALLED_KEY, emptySet())?.toMutableSet() ?: mutableSetOf()
        currentIds.add(extensionId)
        prefs.edit().putStringSet(INSTALLED_KEY, currentIds).apply()
        loadInstalled()
    }

    fun uninstallExtension(extensionId: String) {
        val currentIds = prefs.getStringSet(INSTALLED_KEY, emptySet())?.toMutableSet() ?: mutableSetOf()
        currentIds.remove(extensionId)
        prefs.edit().putStringSet(INSTALLED_KEY, currentIds).apply()
        loadInstalled()
    }

    fun isInstalled(extensionId: String): Boolean {
        val currentIds = prefs.getStringSet(INSTALLED_KEY, emptySet()) ?: emptySet()
        return currentIds.contains(extensionId)
    }
}
