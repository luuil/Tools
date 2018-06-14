# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # prefix = //game.gtimg.cn/images/yxzj/img201606/heroimg
        # passive skill0  {prefix}/187/18700.png    Discard
        # active skill1   {prefix}/187/18710.png    Wanted
        # active skill2   {prefix}/187/18720.png    Wanted
        # active skill3   {prefix}/187/18730.png    Wanted
        IMURL_REX = r'^\/\/game.gtimg.cn\/images\/yxzj\/img201606\/heroimg\/(\d{3})\/\b\1(?!00)\d{2}\b.png$'
        IMURL_PATTERN = re.compile(IMURL_REX)
        image_urls = set(item['image_urls'])
        n = 1
        for image_url in image_urls:
            match = IMURL_PATTERN.match(image_url)
            if match:
                hero_no = int(match.groups()[0])
                url = match.group()
                file_path = '{no}_{name}{n}.png'.format(no=hero_no, name=item['hero_dict'][0][hero_no], n=n) # 文件名
                n += 1
                meta={'file_path': file_path}
                
                # //game.gtimg.cn/images/yxzj/img201606/heroimg/187/18730.png
                # http://game.gtimg.cn/images/yxzj/img201606/heroimg/187/18730.png
                yield scrapy.Request('http:{}'.format(url.strip()), meta=meta)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        file_path = request.meta['file_path']
        print('name', file_path[:-4]) # remove suffix '.png'
        return file_path
