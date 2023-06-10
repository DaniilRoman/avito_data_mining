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
import java.nio.file.Files
import java.nio.file.Paths
import kotlin.io.path.writeText

@OptIn(DelicateCoroutinesApi::class)
class MainPageParser(threadsCount: Int = 10) {
    private val log = KtorSimpleLogger(this.javaClass.name)

    private val mainPagesScrappingDispatcher = newFixedThreadPoolContext(threadsCount, "Avito main pages scraper")

    suspend fun <T>run(context: MainPagesParserContext<T>) = withContext(mainPagesScrappingDispatcher) {
        val targetDir = Paths.get(context.targetDir)
        val targetFile = targetDir.resolve(context.targetFile)

        withContext(Dispatchers.IO) {
            Files.createDirectories(targetDir)
            Files.createFile(targetFile)
        }

        val mainPagesDir = File(context.sourceDir)
        val values = mainPagesDir.listFiles()!!.map{ file ->
            async {
                context.getValues(file)
            }
        }.awaitAll().flatten()

        targetFile.writeText(values.joinToString { context.separator(it) })
    }
}

data class MainPagesParserContext<T>(
    val sourceDir: String,
    val targetDir: String,
    val targetFile: String,
    val getValues: (File) -> List<T>,
    val separator: (T) -> String
)

fun main() = runBlocking {
    val mainPagesDirPath = "/Users/daniil.roman/Desktop/test/pers/avito_data_mining/scraper-v2/src/main/resources/avito_main_pages/04_06_2023/1"
    val targetParsedMainPagesDir = "/Users/daniil.roman/Desktop/test/pers/avito_data_mining/scraper-v2/src/main/resources/avito_main_pages/04_06_2023/parsed/1"
    val targetParsedMainPagesFile = "parsed.txt"

    val getValues: (file: File) -> List<String> = { file ->
        val mainPage = file.readText()
        listOf(file.name)
    }

    val context = MainPagesParserContext<String>(mainPagesDirPath, targetParsedMainPagesDir, targetParsedMainPagesFile,
        getValues
    ) { "$it\n" }
    MainPageParser().run(context)
}