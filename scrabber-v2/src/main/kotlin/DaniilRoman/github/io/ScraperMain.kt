package DaniilRoman.github.io

import kotlinx.coroutines.*

fun main() = runBlocking {
    val url = "https://www.avito.ru/nizhniy_novgorod/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?p="
    val headersFileName = "/Users/daniil.roman/Desktop/test/pers/avito_data_mining/scraper-v2/src/main/resources/headers.text"
    val startPage = 6
    val stopPage = 15
    val dirPath = "/Users/daniil.roman/Desktop/test/pers/avito_data_mining/scraper-v2/src/main/resources/avito_main_pages/04_06_2023/2/"
    val randomFromMs = 10000L
    val randomUntilMs = 15000L

    val mainPagesScraper = MainPageScraper()
    val context = MainPagesScraperContext(dirPath, startPage, stopPage, url, headersFileName, randomFromMs, randomUntilMs)
    mainPagesScraper.run(context)
}
