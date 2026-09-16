package com.example.ui.screens.details

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp

fun Modifier.shimmer(): Modifier = composed {
    val infiniteTransition = rememberInfiniteTransition(label = "shimmer")
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.2f,
        targetValue = 0.6f,
        animationSpec = infiniteRepeatable(
            animation = tween(800, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "shimmer_alpha"
    )
    this.background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = alpha))
}

@Composable
fun DetailsSkeleton() {
    Column(
        modifier = Modifier.fillMaxSize()
    ) {
        // Hero Image
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(400.dp)
                .shimmer()
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Title
        Box(modifier = Modifier.padding(horizontal = 16.dp).width(200.dp).height(32.dp).clip(RoundedCornerShape(8.dp)).shimmer())
        Spacer(modifier = Modifier.height(8.dp))
        Box(modifier = Modifier.padding(horizontal = 16.dp).width(150.dp).height(20.dp).clip(RoundedCornerShape(8.dp)).shimmer())
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Action Buttons Row
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Box(modifier = Modifier.weight(1f).height(50.dp).clip(RoundedCornerShape(25.dp)).shimmer())
            Box(modifier = Modifier.size(50.dp).clip(CircleShape).shimmer())
            Box(modifier = Modifier.size(50.dp).clip(CircleShape).shimmer())
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Overview Title
        Box(modifier = Modifier.padding(horizontal = 16.dp).width(100.dp).height(24.dp).clip(RoundedCornerShape(8.dp)).shimmer())
        Spacer(modifier = Modifier.height(16.dp))
        
        // Overview Text
        Column(modifier = Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(modifier = Modifier.fillMaxWidth().height(16.dp).clip(RoundedCornerShape(4.dp)).shimmer())
            Box(modifier = Modifier.fillMaxWidth().height(16.dp).clip(RoundedCornerShape(4.dp)).shimmer())
            Box(modifier = Modifier.fillMaxWidth(0.8f).height(16.dp).clip(RoundedCornerShape(4.dp)).shimmer())
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Horizontal list (e.g. Trailers or Seasons)
        Row(modifier = Modifier.padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Box(modifier = Modifier.width(160.dp).height(90.dp).clip(RoundedCornerShape(12.dp)).shimmer())
            Box(modifier = Modifier.width(160.dp).height(90.dp).clip(RoundedCornerShape(12.dp)).shimmer())
        }
    }
}
