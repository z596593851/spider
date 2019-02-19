# -*- coding: utf-8 -*-
import os
import random
import re


if __name__ == '__main__':
    rule = ".*?>(.*)<"
    rule2=".*?([0-9]*)"
    s='<div class="markdown_body"><p>团队一起做了一个人工智能建模平台 Mo （ <a href="http://momodel.cn" rel="nofollow">momodel.cn</a> ），初衷是降低机器学习门槛，让初学者能够更快上手机器学习，体会到自己开发 AI 应用的成就感。</p>\n<p>最近的版本新上了“训练营”功能，把吴恩达老师和 Udacity 的两套机器学习视频课程分章节改写成.ipynb 文档，用户可以在 Jupyter 环境中边看视频边进行代码运行。此外还有一些实战题目。这样的学习形式你会喜欢吗？欢迎提意见哈～</p><p><img src="https://ws2.sinaimg.cn/large/006tKfTcly1g0bjqoyc12j31p40u0dmn.jpg" alt=""></p><p><img src="https://ws2.sinaimg.cn/large/006tKfTcly1g0bk65l8o8j31wz0u0tim.jpg" alt=""></p>'
    s=s.replace('\n','').strip()
    list=['<div class="markdown_body"><p>团队一起做了一个人工智能建模平台 Mo （ <a href="http://momodel.cn" rel="nofollow">momodel.cn</a> ），初衷是降低机器学习门槛，让初学者能够更快上手机器学习，体会到自己开发 AI 应用的成就感。</p>','<p>最近的版本新上了“训练营”功能，把吴恩达老师和 Udacity 的两套机器学习视频课程分章节改写成.ipynb 文档，用户可以在 Jupyter 环境中边看视频边进行代码运行。此外还有一些实战题目。这样的学习形式你会喜欢吗？欢迎提意见哈～</p>']
    match_re = re.match(rule, s)
    print(match_re.group(1))




