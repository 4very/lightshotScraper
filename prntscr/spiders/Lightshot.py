# -*- coding: utf-8 -*-
import scrapy


def inc(instr):
    str_l = list(instr)
    for i in range(len(str_l) - 1, -1, -1):
        if ord(str_l[i]) in range(97, 122) or ord(str_l[i]) in range(48, 57):
            str_l[i] = chr(ord(str_l[i]) + 1)
            for j in range(i+1, len(str_l)):
                str_l[j] = 'a'
            return "".join(str_l)
        elif ord(str_l[i]) == 122 and i != 0:
            str_l[i] = '0'
            for j in range(i+1, len(str_l)):
                str_l[j] = 'a'
            return "".join(str_l)
        elif ord(str_l[i]) == 122 and i == 0:
            str_l[i] = '1'
            for j in range(i+1, len(str_l)):
                str_l[j] = 'a'
            return "".join(str_l)
    return "".join(["a" for _ in range(len(str_l) + 1)])


class LightshotSpider(scrapy.Spider):
    name = 'Lightshot'
    start_urls = ['https://prnt.sc/a']

    def parse(self, response):
        if (response.css(
                "div.image-container img.screenshot-image::attr('src')").extract_first() != "//st.prntscr.com/2019/11"
                                                                                            "/26/0154/img"
                                                                                            "/0_173a7b_211be8ff.png"):
            yield {
                'url': response.url,
                'img-url': response.css("div.image-container img.screenshot-image::attr('src')").extract_first()
            }

        new_imgid = inc(response.css("div.image-container img.screenshot-image::attr('image-id')").extract_first())
        if len(new_imgid) <= 7:
            yield scrapy.Request(url=response.urljoin(new_imgid))

