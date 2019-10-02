from parser.Writer import writeVipHrefs


def handleVipOrder(tree):
    vipBlocks = tree.find_all('div', {'class': 'serp-vips'})
    hrefList = []

    for vipBlock in vipBlocks:
        for vip in vipBlock.findAll('a', {'class': 'description-title-link'}):
            href = vip['href']
            hrefList.append(href)
        vipBlock.decompose()
    writeVipHrefs(hrefList)