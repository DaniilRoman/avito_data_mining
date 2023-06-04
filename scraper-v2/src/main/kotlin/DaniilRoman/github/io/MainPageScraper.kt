package DaniilRoman.github.io

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.logging.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.util.logging.*
import kotlinx.coroutines.*
import java.io.File
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.createDirectories
import kotlin.io.path.writeText
import kotlin.random.Random

@OptIn(DelicateCoroutinesApi::class)
class MainPageScraper() {
    val log = KtorSimpleLogger(this.javaClass.name)
    val client = HttpClient(CIO) {
        install(Logging) {
            level = LogLevel.INFO
        }
    }
    val mainPagesScrappingDispatcher = newFixedThreadPoolContext(10, "Avito main pages scrabber")

    suspend fun run(context: MainPagesScraperContext) = withContext(mainPagesScrappingDispatcher) {
        val dirPath = context.dirPath
        val startPage = context.startPage
        val stopPage = context.stopPage
        val url = context.url
        val headersFileName = context.headersFileName

        Paths.get(dirPath).createDirectories()

        val headers: Array<Pair<String, List<String>>> = parseHeaders(headersFileName)

        (startPage..stopPage).forEach {pageNumber ->
            val pageUrl = constructPageUrl(url, pageNumber)
            val fileName = constructFilename(pageNumber)

            val createFileDeferred = async(CoroutineName("Create new file for page $pageNumber\"")) {
                val newFileForContent = Paths.get(dirPath, fileName)
                newFileForContent.toFile().createNewFile()
                newFileForContent
            }

            val pageResponseDeferred = async(CoroutineName("Get data for page $pageNumber")) {
                client.get(pageUrl) {
                    headersOf(*headers)
                }
            }

            val newFileForContent: Path = createFileDeferred.await()
            val pageResponse: HttpResponse = pageResponseDeferred.await()

            val htmlPage = pageResponse.bodyAsText()
            newFileForContent.writeText(htmlPage)
            log.info("Content was written for page $pageNumber")

            randomDelay(context.randomFromMs, context.randomUntilMs)
        }
    }

    private suspend fun randomDelay(from: Long, until: Long) {
        val randomDelay = Random.nextLong(from, until)
        log.info("Delay $randomDelay")
        delay(randomDelay)
    }

    private fun parseHeaders(headersFileName: String): Array<Pair<String, List<String>>> {
        val headers: Array<Pair<String, List<String>>> = File(headersFileName)
            .readLines().map { headerKeyValue ->
                headerKeyValue.substringBeforeLast(":") to
                        headerKeyValue.substringAfterLast(":").split(",")
            }.toTypedArray()
        return headers
    }

    private fun constructPageUrl(url: String, page: Int) = "$url$page"

    private fun constructFilename(page: Int) = "$page.html"
}

data class MainPagesScraperContext(
    val dirPath: String,
    val startPage: Int,
    val stopPage: Int,
    val url: String,
    val headersFileName: String,
    val randomFromMs: Long = 5000,
    val randomUntilMs: Long = 7000
)
