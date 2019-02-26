# -*- coding:utf-8 -*-

import re

from bs4 import BeautifulSoup

class PageParseTool(object):

    def beautifulsoup_parse_html(self, content, selecter):
        soup = BeautifulSoup(content, "html.parser")
        return soup.select(selecter)

    def regex_parse_str(self, content, regexp):
        pattern = re.compile(regexp)
        result = re.findall(pattern, content)

        if not result:
            return None
        return result

page_parse_tool = PageParseTool()