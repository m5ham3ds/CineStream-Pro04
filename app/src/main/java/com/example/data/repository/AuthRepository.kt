package com.example.data.repository

import android.net.Uri
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

data class User(
    val uid: String = "",
    val email: String = "",
    val firstName: String = "",
    val lastName: String = "",
    val username: String = "",
    val photoUrl: String = "",
    val isProfilePublic: Boolean = true
)

object AuthRepository {

    val currentUserFlow = MutableStateFlow<User?>(null)
    val auth: FirebaseAuth = FirebaseAuth.getInstance()
    private val db: FirebaseFirestore = FirebaseFirestore.getInstance()
    private val storage: FirebaseStorage = FirebaseStorage.getInstance()

    suspend fun uploadProfilePicture(uid: String, uri: Uri): String {
        val cloudName = com.example.BuildConfig.CLOUDINARY_CLOUD_NAME
        val uploadPreset = com.example.BuildConfig.CLOUDINARY_UPLOAD_PRESET
        
        if (cloudName.isNotEmpty() && uploadPreset.isNotEmpty()) {
            try {
                try {
                    com.cloudinary.android.MediaManager.get()
                } catch (e: Exception) {
                    // This function is typically called from a ViewModel where context isn't directly available.
                    // Instead, MediaManager should be initialized in MyApplication.
                    // For safety here, we throw an error if it's not initialized.
                    throw Exception("Cloudinary MediaManager not initialized. Must be initialized in Application class.")
                }
                
                val cloudinaryUrl = suspendCancellableCoroutine<String> { continuation ->
                    com.cloudinary.android.MediaManager.get().upload(uri)
                        .unsigned(uploadPreset)
                        .callback(object : com.cloudinary.android.callback.UploadCallback {
                            override fun onSuccess(requestId: String?, resultData: Map<*, *>?) {
                                val secureUrl = resultData?.get("secure_url") as? String
                                if (secureUrl != null) {
                                    continuation.resume(secureUrl)
                                } else {
                                    continuation.resumeWithException(Exception("Secure URL not found"))
                                }
                            }
                            
                            override fun onStart(requestId: String?) {}
                            override fun onProgress(requestId: String?, bytes: Long, totalBytes: Long) {}
                            override fun onError(requestId: String?, error: com.cloudinary.android.callback.ErrorInfo?) {
                                continuation.resumeWithException(Exception(error?.description ?: "Unknown error"))
                            }
                            override fun onReschedule(requestId: String?, error: com.cloudinary.android.callback.ErrorInfo?) {}
                        }).dispatch()
                }
                return cloudinaryUrl
            } catch (e: Exception) {
                // If Cloudinary fails, fallback to Firebase Storage below
                android.util.Log.e("Upload", "Cloudinary failed, falling back to Firebase", e)
            }
        }
        
        // Fallback to Firebase Storage
        val ref = storage.reference.child("profile_pictures/$uid/${System.currentTimeMillis()}.jpg")
        ref.putFile(uri).await()
        return ref.downloadUrl.await().toString()
    }

    suspend fun getCurrentUser(): User? {
        val firebaseUser = auth.currentUser
        if (firebaseUser == null) {
            currentUserFlow.value = null
            return null
        }
        return try {
            val snapshot = kotlinx.coroutines.withTimeout(15000) { db.collection("users").document(firebaseUser.uid).get().await() }
            if (snapshot.exists()) {
                val user = snapshot.toObject(User::class.java)
                currentUserFlow.value = user
                user
            } else {
                currentUserFlow.value = null
                null
            }
        } catch (e: Exception) {
            null
        }
    }

    suspend fun saveUser(user: User) {
        db.collection("users").document(user.uid).set(user).await()
        currentUserFlow.value = user
    }

    suspend fun isUsernameTaken(username: String, currentUid: String): Boolean {
        val snapshot = db.collection("users")
            .whereEqualTo("username", username)
            .get()
            .await()
            
        for (doc in snapshot.documents) {
            if (doc.id != currentUid) return true
        }
        return false
    }

    suspend fun generateUniqueUsername(baseName: String): String {
        var base = baseName.replace(Regex("[^a-zA-Z0-9]"), "").lowercase()
        if (base.isEmpty()) base = "user"
        
        var attempt = base
        var isTaken = isUsernameTaken(attempt, "")
        var count = 1
        
        while (isTaken) {
            attempt = "${base}${count}"
            isTaken = isUsernameTaken(attempt, "")
            count++
        }
        return attempt
    }
}
