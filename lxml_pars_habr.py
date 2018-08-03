import lxml.html as html
from requests import get
import json


def parse():
    result = []
    main_domain_stat = 'https://habr.com/'
    req = get(main_domain_stat)
    page = html.fromstring(req.content)
    article_links = page.xpath('//li/article[contains(@class, "post_preview")]/h2[@class="post__title"]/'
                               'a[@class="post__title_link"]/@href')

    for article in article_links:
        req = get(article)
        art_page = html.fromstring(req.content)
        art_headers = art_page.xpath('//article[contains(@class, "post")]/div[@class="post__wrapper"]/'
                                     'h1[contains(@class, "post__title")]/span/text()')
        art_text = ''.join(s.strip() for s in art_page.xpath('//article[contains(@class, "post")]/'
                                                             'div[@class="post__wrapper"]/'
                                                             'div[contains(@class, "post__body")]'
                                                             '/div[contains(@class, "post__text")]/text()'))
        art_img = art_page.xpath('//article[contains(@class, "post")]/div[@class="post__wrapper"]/'
                                 'div[contains(@class, "post__body")]/div[contains(@class, "post__text")]/img/@src')

        result.append({'title': art_headers,
                       'post': {
                           'text': art_text,
                           'img': art_img
                       }})

    # print(result)

    with open('result.json', 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False)


if __name__ == "__main__":
    parse()
