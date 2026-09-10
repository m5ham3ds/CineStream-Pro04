package com.example.ui.screens.details

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.PhotoLibrary
import androidx.compose.material.icons.filled.CalendarToday
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Movie
import androidx.compose.material.icons.filled.Tv
import androidx.compose.material.icons.outlined.Star
import androidx.compose.material3.*
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.ui.ViewModelFactory
import java.util.Calendar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PersonDetailsScreen(
    personId: String,
    onBack: () -> Unit,
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    viewModel: PersonDetailsViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(personId) {
        viewModel.loadPerson(personId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(uiState.person?.name ?: "", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.SemiBold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    IconButton(
                        onClick = { /* Share */ },
                        modifier = Modifier
                            .padding(end = 8.dp)
                            .background(Color(0xFF1C1C1E), CircleShape)
                            .size(36.dp)
                    ) {
                        Icon(Icons.Default.Share, contentDescription = "Share", tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color(0xFF0F0F11)
                ),
                windowInsets = WindowInsets(0.dp)
            )
        },
        containerColor = Color(0xFF0F0F11)
    ) { padding ->
        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator(color = Color(0xFFE50914)) }
        } else if (uiState.person != null) {
            val person = uiState.person!!
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .verticalScroll(rememberScrollState())
            ) {
                // Header Profile
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.Top
                ) {
                    // Portrait Image
                    Box(
                        modifier = Modifier
                            .weight(0.42f)
                            .aspectRatio(0.7f)
                            .clip(RoundedCornerShape(12.dp))
                            .background(Color.DarkGray)
                    ) {
                        AsyncImage(
                            model = person.profileUrl ?: "https://via.placeholder.com/150",
                            contentDescription = person.name,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        // Gallery Icon
                        Box(
                            modifier = Modifier
                                .align(Alignment.BottomEnd)
                                .padding(8.dp)
                                .size(32.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color.Black.copy(alpha = 0.6f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.PhotoLibrary, contentDescription = "Gallery", tint = Color.White, modifier = Modifier.size(16.dp))
                        }
                    }

                    Spacer(modifier = Modifier.width(16.dp))
                    
                    // Info Section
                    Column(
                        modifier = Modifier.weight(0.58f)
                    ) {
                        val names = person.name.split(" ", limit = 2)
                        val firstName = names.getOrNull(0) ?: ""
                        val lastName = names.getOrNull(1) ?: ""
                        
                        Text(firstName, fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color.White, lineHeight = 32.sp)
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(lastName, fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color(0xFFE50914), lineHeight = 32.sp)
                            Spacer(modifier = Modifier.width(6.dp))
                            Icon(Icons.Default.CheckCircle, contentDescription = "Verified", tint = Color(0xFFE50914), modifier = Modifier.size(20.dp))
                        }
                        
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(person.knownFor ?: "Actor", fontSize = 14.sp, color = Color.Gray)
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        // Info Grid
                        Row(modifier = Modifier.fillMaxWidth()) {
                            // Born
                            Column(modifier = Modifier.weight(1f)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.CalendarToday, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(12.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text("Born", fontSize = 11.sp, color = Color.Gray)
                                }
                                Text(person.birthday ?: "-", fontSize = 11.sp, color = Color.LightGray, maxLines = 2)
                            }
                            // Birthplace
                            Column(modifier = Modifier.weight(1.2f)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.LocationOn, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(12.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text("Birthplace", fontSize = 11.sp, color = Color.Gray)
                                }
                                Text(person.placeOfBirth ?: "-", fontSize = 11.sp, color = Color.LightGray, maxLines = 2, overflow = TextOverflow.Ellipsis)
                            }
                            // Known For
                            Column(modifier = Modifier.weight(0.8f)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Star, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(12.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text("Known For", fontSize = 11.sp, color = Color.Gray)
                                }
                                Text(person.knownFor ?: "-", fontSize = 11.sp, color = Color.LightGray, maxLines = 2)
                            }
                        }
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        // Stats Row
                        val firstCreditYear = (person.movies.map { it.year } + person.series.map { it.year }).filter { it > 0 }.minOrNull()
                        val currentYear = Calendar.getInstance().get(Calendar.YEAR)
                        val yearsActive = if (firstCreditYear != null && firstCreditYear > 0) {
                            currentYear - firstCreditYear
                        } else {
                            0
                        }
                        val yearsActiveStr = if (yearsActive > 0) "${yearsActive}+" else "-"

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            StatBox(icon = Icons.Default.Movie, value = if (person.movies.isNotEmpty()) "${person.movies.size}+" else "-", label = "Movies", modifier = Modifier.weight(1f))
                            Spacer(modifier = Modifier.width(8.dp))
                            StatBox(icon = Icons.Default.Tv, value = if (person.series.isNotEmpty()) "${person.series.size}+" else "-", label = "TV Shows", modifier = Modifier.weight(1f))
                            Spacer(modifier = Modifier.width(8.dp))
                            StatBox(icon = Icons.Outlined.Star, value = yearsActiveStr, label = "Years Active", modifier = Modifier.weight(1f))
                        }
                    }
                }
                
                // Biography
                if (person.biography.isNotBlank()) {
                    Spacer(modifier = Modifier.height(16.dp))
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF1C1C1E)),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.width(3.dp).height(16.dp).background(Color(0xFFE50914), RoundedCornerShape(4.dp)))
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("Biography", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            }
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(person.biography, color = Color.LightGray, fontSize = 14.sp, lineHeight = 20.sp)
                        }
                    }
                }

                // Movies
                if (person.movies.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(24.dp))
                    SectionHeader("Top Movies")
                    Spacer(modifier = Modifier.height(12.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(person.movies) { movie ->
                            MediaCreditCard(title = movie.title, posterUrl = movie.posterUrl, year = movie.year, onClick = { onMovieClick(movie.id) })
                        }
                    }
                }

                // Series
                if (person.series.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(24.dp))
                    SectionHeader("Top TV Shows")
                    Spacer(modifier = Modifier.height(12.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(person.series) { series ->
                            MediaCreditCard(title = series.title, posterUrl = series.posterUrl, year = series.year, onClick = { onSeriesClick(series.id) })
                        }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}

@Composable
fun StatBox(icon: androidx.compose.ui.graphics.vector.ImageVector, value: String, label: String, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .background(Color(0xFF1C1C1E))
            .padding(vertical = 12.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(icon, contentDescription = label, tint = Color.Gray, modifier = Modifier.size(16.dp))
            Spacer(modifier = Modifier.height(4.dp))
            Text(value, color = Color(0xFFE50914), fontSize = 14.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(2.dp))
            Text(label, color = Color.Gray, fontSize = 10.sp)
        }
    }
}

@Composable
fun SectionHeader(title: String) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(title, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.White)
        }
        Text("View all", fontSize = 12.sp, color = Color(0xFFE50914), modifier = Modifier.clickable { })
    }
}

@Composable
fun MediaCreditCard(title: String, posterUrl: String, year: Int, onClick: () -> Unit) {
    Column(
        modifier = Modifier.width(110.dp).clickable { onClick() }
    ) {
        AsyncImage(
            model = posterUrl,
            contentDescription = title,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxWidth().aspectRatio(2f/3f).clip(RoundedCornerShape(8.dp)).background(Color.DarkGray)
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = title,
            color = Color.White,
            fontSize = 13.sp,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
        if (year > 0) {
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = year.toString(),
                color = Color.Gray,
                fontSize = 12.sp
            )
        }
    }
}
