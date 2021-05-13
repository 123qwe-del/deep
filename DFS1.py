from aiohttp_requests import requests
from lxml import etree
import aiofiles
import asyncio

cra = []
args = None


async def get_html(url):  # 获取网页html文件
    if url not in cra:
        res = await requests.get(url)
        v = await res.read()
        html = v.decode("utf-8")
        await donwload(html, url)
        cra.append(url)
        return html


# 获取每页的url
async def get_url(url):
    res = await get_html(url)
    # print(res)
    try:
        ele = etree.HTML(res)
        url_list1 = []
        try:
            hreflist = ele.xpath('//a/@href')
            for href in hreflist:
                if href.startswith("http"):
                    url_list1.append(href)
            return url_list1
        except:
            pass
    except:
        pass


# 爬虫代码
async def spider(url):
    urls = await get_url(url)
    for i in range(1, len(urls)):
        urls2 = await get_url(urls[i])
        try:
            for k in range(1, len(urls2)):
                res2 = await requests.get(urls2[k], allow_redirects=False).text
                cra.append(url)
                donwload(res2, urls[k])
        except:
            pass

#文件保存代码
async def donwload(res2, urls):
    if args != None:
        if str(args) in res2:
            async with aiofiles.open("关键字数据文本.text", 'a+', encoding="utf-8") as key:
                await key.write(urls + "\n")
                print("保存了{}条url".format(len(cra) + 1))
        else:
            async with aiofiles.open("非关键字文本.text", 'a+', encoding="utf-8") as item:
                await item.write(urls + "\n")
                print("保存了{}条url".format(len(cra) + 1))
    else:
        async with aiofiles.open("非关键字文本.text", 'a+', encoding="utf-8") as item:
            await item.write(urls + "\n")
            print("保存了{}条url".format(len(cra) + 1))


async def run():
    startUrl = "https://www.csdn.net/"
    await spider(startUrl)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
