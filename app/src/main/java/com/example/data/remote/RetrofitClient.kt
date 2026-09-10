package com.example.data.remote

import android.content.Context
import android.net.ConnectivityManager
import com.example.MyApplication
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import okhttp3.Cache
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.io.File

object RetrofitClient {

    private const val BASE_URL = "https://api.themoviedb.org/3/"

    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val cacheSize = (50 * 1024 * 1024).toLong() // 50 MB

    private fun isNetworkAvailable(): Boolean {
        val connectivityManager = com.example.di.AppContainer.application.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val activeNetworkInfo = connectivityManager.activeNetworkInfo
        return activeNetworkInfo != null && activeNetworkInfo.isConnected
    }

    private val okHttpClient by lazy {
        OkHttpClient.Builder()
            .cache(Cache(File(com.example.di.AppContainer.application.cacheDir, "http_cache"), cacheSize))
            .addInterceptor { chain ->
                var request = chain.request()
                if (isNetworkAvailable()) {
                    request = request.newBuilder()
                        .header("Cache-Control", "public, max-age=" + 60)
                        .build()
                } else {
                    request = request.newBuilder()
                        .header("Cache-Control", "public, only-if-cached, max-stale=" + 60 * 60 * 24 * 7)
                        .build()
                }
                chain.proceed(request)
            }
            .addNetworkInterceptor { chain ->
                val response = chain.proceed(chain.request())
                val cacheControl = response.header("Cache-Control")
                if (cacheControl == null || cacheControl.contains("no-store") || cacheControl.contains("no-cache") ||
                    cacheControl.contains("must-revalidate") || cacheControl.contains("max-age=0")) {
                    response.newBuilder()
                        .removeHeader("Pragma")
                        .header("Cache-Control", "public, max-age=" + 60 * 60 * 24 * 7) // Cache for 7 days
                        .build()
                } else {
                    response
                }
            }
            .addInterceptor(loggingInterceptor)
            .build()
    }

    val tmdbApi: TmdbApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
            .create(TmdbApiService::class.java)
    }
}
