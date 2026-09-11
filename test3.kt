interface Base { val iconUrl: String; val isAnime: Boolean }
class Impl : Base { override val iconUrl = "http://a"; override val isAnime = true }
fun main() {
    val obj = Impl()
    val clazz = obj.javaClass
    println(clazz.methods.map { it.name })
}
