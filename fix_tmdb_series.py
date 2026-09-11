with open('app/src/main/java/com/example/data/remote/TmdbModels.kt', 'r') as f:
    text = f.read()

broken_part = """data class TmdbSeries(
    @Json(name = "id") val id: Int,
    @Json(name = "name") val name: String?,
    @Json(name = "original_name") val originalName: String? = null,
    @Json(name = "overview") val overview: String?,
    @Json(name = "poster_path") val posterPath: String?,
    @Json(name = "backdrop_path") val backdropPath: String?,
    @Json(name = "first_air_date") val firstAirDate: String?,
    @Json(name = "vote_average") val voteAverage: Double?
) {"""

fixed_part = """data class TmdbSeries(
    @Json(name = "id") val id: Int,
    @Json(name = "name") val name: String?,
    @Json(name = "original_name") val originalName: String? = null,
    @Json(name = "overview") val overview: String?,
    @Json(name = "poster_path") val posterPath: String?,
    @Json(name = "backdrop_path") val backdropPath: String?,
    @Json(name = "first_air_date") val firstAirDate: String?,
    @Json(name = "vote_average") val voteAverage: Double?,
    @Json(name = "genre_ids") val genreIds: List<Int>? = emptyList(),
    @Json(name = "origin_country") val originCountry: List<String>? = emptyList()
) {"""

if broken_part in text:
    text = text.replace(broken_part, fixed_part)
    with open('app/src/main/java/com/example/data/remote/TmdbModels.kt', 'w') as f:
        f.write(text)
    print("Added genreIds and originCountry to TmdbSeries!")
else:
    print("Could not find broken part.")
