package com.example.ui.screens.onboarding
import androidx.compose.material.icons.outlined.FileDownload
import androidx.compose.ui.draw.alpha

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.Hd
import androidx.compose.material.icons.outlined.Movie
import androidx.compose.material.icons.outlined.PhoneAndroid
import androidx.compose.material.icons.outlined.StarOutline
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.example.R
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.data.repository.UserPreferencesRepository
import kotlinx.coroutines.launch

@Composable
fun OnboardingScreen(onComplete: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val userPrefs = UserPreferencesRepository(context)
    val pagerState = rememberPagerState(pageCount = { 3 })

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF09090C))
    ) {
        // Red glows at top corners
        Box(
            modifier = Modifier
                .align(Alignment.TopStart)
                .size(200.dp)
                .background(
                    brush = Brush.radialGradient(
                        colors = listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f), Color.Transparent)
                    )
                )
        )
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .size(200.dp)
                .background(
                    brush = Brush.radialGradient(
                        colors = listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f), Color.Transparent)
                    )
                )
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(top = 48.dp, bottom = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Top Section (Consistent)
            Text(
                text = stringResource(R.string.welcome_to),
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.Normal
            )
            Text(
                text = buildAnnotatedString {
                    withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.primary)) { append("Cine") }
                    withStyle(style = SpanStyle(color = Color.White)) { append("Stream") }
                },
                fontSize = 36.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(12.dp))
            Box(modifier = Modifier.width(40.dp).height(2.dp).background(MaterialTheme.colorScheme.primary))
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = stringResource(R.string.slogan2),
                color = Color.Gray,
                fontSize = 14.sp,
                textAlign = TextAlign.Center,
                lineHeight = 20.sp,
                modifier = Modifier.padding(horizontal = 32.dp)
            )

            Spacer(modifier = Modifier.height(32.dp))

            // Pager Section
            HorizontalPager(
                state = pagerState,
                modifier = Modifier.weight(1f)
            ) { page ->
                when (page) {
                    0 -> PageOneContent()
                    1 -> PageTwoContent()
                    2 -> PageThreeContent()
                }
            }

            // Bottom Section
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                repeat(3) { index ->
                    val color = if (pagerState.currentPage == index) MaterialTheme.colorScheme.primary else Color.DarkGray
                    Box(modifier = Modifier.size(8.dp).clip(CircleShape).background(color))
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Next / Get Started Button
            Button(
                onClick = {
                    if (pagerState.currentPage < 2) {
                        scope.launch {
                            pagerState.animateScrollToPage(pagerState.currentPage + 1)
                        }
                    } else {
                        scope.launch {
                            userPrefs.saveOnboardingCompleted(true)
                            onComplete()
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp)
                    .height(56.dp)
                    // Inner red glow effect for the button
                    .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha=0.5f), RoundedCornerShape(28.dp)),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                shape = RoundedCornerShape(28.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = if (pagerState.currentPage < 2) stringResource(R.string.onboarding_next) else stringResource(R.string.onboarding_get_started),
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Icon(imageVector = Icons.Default.ChevronRight, contentDescription = null, tint = Color.White)
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = buildAnnotatedString {
                    withStyle(style = SpanStyle(color = Color.Gray)) {
                        append(stringResource(R.string.already_have_account) + " ")
                    }
                    withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.primary)) {
                        append(stringResource(R.string.sign_in))
                    }
                },
                fontSize = 14.sp,
                modifier = Modifier.clickable {
                    scope.launch {
                        userPrefs.saveOnboardingCompleted(true)
                        onComplete()
                    }
                }
            )
        }
    }
}

@Composable
fun PageOneContent() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(horizontal = 16.dp),
            contentAlignment = Alignment.Center
        ) {
            AsyncImage(
                model = "https://images.unsplash.com/photo-1595769816263-9b910be24d5f?q=80&w=1000&auto=format&fit=crop",
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(220.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .alpha(0.6f)
            )
            
            // Side texts overlaid on image
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column {
                    Text(stringResource(R.string.good_stories_never_end).replace(" ", "\n"), color = Color.Gray, fontSize = 10.sp, letterSpacing = 2.sp, lineHeight = 16.sp)
                    Box(modifier = Modifier.width(20.dp).height(1.dp).background(MaterialTheme.colorScheme.primary).padding(top=4.dp))
                }
                Column(horizontalAlignment = Alignment.End) {
                    Text((stringResource(R.string.movies) + "\n" + stringResource(R.string.category_series) + "\n" + stringResource(R.string.category_anime)).uppercase(), color = Color.Gray, fontSize = 10.sp, letterSpacing = 2.sp, lineHeight = 16.sp, textAlign = TextAlign.End)
                    Box(modifier = Modifier.width(20.dp).height(1.dp).background(MaterialTheme.colorScheme.primary).padding(top=4.dp))
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // 3 Cards Box
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .border(1.dp, Color.DarkGray.copy(alpha=0.5f), RoundedCornerShape(24.dp))
                .background(Color(0xFF101014), RoundedCornerShape(24.dp))
                .padding(vertical = 24.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                FeatureItem(icon = Icons.Outlined.Hd, text = stringResource(R.string.hd_quality), iconTint = MaterialTheme.colorScheme.primary)
                Box(modifier = Modifier.width(1.dp).height(40.dp).background(Color.DarkGray))
                FeatureItem(icon = Icons.Outlined.Movie, text = stringResource(R.string.movies_and_series), iconTint = Color.LightGray)
                Box(modifier = Modifier.width(1.dp).height(40.dp).background(Color.DarkGray))
                FeatureItem(icon = Icons.Outlined.PhoneAndroid, text = stringResource(R.string.anytime_anywhere), iconTint = Color.LightGray)
            }
        }
        Spacer(modifier = Modifier.height(24.dp))
    }
}

@Composable
fun PageTwoContent() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        AsyncImage(
            model = "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=1000&auto=format&fit=crop",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .height(220.dp)
                .clip(RoundedCornerShape(16.dp))
                .alpha(0.8f)
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Download Icon
        Box(
            modifier = Modifier
                .size(64.dp)
                .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
                .background(
                    Brush.radialGradient(
                        colors = listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), Color.Transparent)
                    )
                ),
            contentAlignment = Alignment.Center
        ) {
            Icon(imageVector = androidx.compose.material.icons.Icons.Outlined.FileDownload, contentDescription = null, tint = Color.White, modifier = Modifier.size(32.dp))
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = buildAnnotatedString {
                append(stringResource(R.string.download_and_watch))
                withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.primary)) {
                    append(stringResource(R.string.offline_highlight))
                }
            },
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = stringResource(R.string.download_any_movie_offline),
            color = Color.Gray,
            fontSize = 14.sp,
            textAlign = TextAlign.Center,
            lineHeight = 20.sp
        )
    }
}

@Composable
fun PageThreeContent() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        AsyncImage(
            model = "https://image.tmdb.org/t/p/w500/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg",
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 48.dp)
                .height(200.dp)
                .clip(RoundedCornerShape(24.dp))
                .border(2.dp, Color.DarkGray, RoundedCornerShape(24.dp))
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            SmallCard(icon = Icons.Outlined.StarOutline, text = stringResource(R.string.personalized_recommendations))
            SmallCard(icon = Icons.Outlined.FavoriteBorder, text = stringResource(R.string.your_favorite_genres))
            SmallCard(icon = Icons.Outlined.BookmarkBorder, text = stringResource(R.string.build_your_watchlist))
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = buildAnnotatedString {
                append(stringResource(R.string.personalized_prefix))
                withStyle(style = SpanStyle(color = MaterialTheme.colorScheme.primary)) {
                    append(stringResource(R.string.for_you_highlight))
                }
            },
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = stringResource(R.string.get_recommendations_tailored),
            color = Color.Gray,
            fontSize = 14.sp,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
fun FeatureItem(icon: ImageVector, text: String, iconTint: Color) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.width(100.dp)
    ) {
        Icon(imageVector = icon, contentDescription = null, tint = iconTint, modifier = Modifier.size(32.dp))
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = text, color = Color.LightGray, fontSize = 12.sp, textAlign = TextAlign.Center, lineHeight = 16.sp)
    }
}

@Composable
fun SmallCard(icon: ImageVector, text: String) {
    Box(
        modifier = Modifier
            .width(110.dp)
            .height(110.dp)
            .border(1.dp, Color.DarkGray.copy(alpha=0.5f), RoundedCornerShape(16.dp))
            .background(Color(0xFF101014), RoundedCornerShape(16.dp))
            .padding(12.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(imageVector = icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
            Spacer(modifier = Modifier.height(12.dp))
            Text(text = text, color = Color.LightGray, fontSize = 10.sp, textAlign = TextAlign.Center, lineHeight = 14.sp)
        }
    }
}
