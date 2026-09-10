package com.example

import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.Robolectric
import androidx.test.ext.junit.rules.ActivityScenarioRule
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class CrashTest {
    @Test
    fun testCrash() {
        try {
            val controller = Robolectric.buildActivity(MainActivity::class.java)
            controller.setup()
        } catch (e: Exception) {
            e.printStackTrace()
            throw e
        }
    }
}
