import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

def get_page(): # 記事へのurlを抽出
    raw_url = []
    with open('tweets1.json', 'r') as f:
        res_json = json.load(f)

    rlink = re.compile(r'http')
    rbracket = re.compile(r'【|】')
    text = []

    for prop in res_json:
        try:
            tweet = prop["tweet"]
            words = tweet.split()

            midashi = tweet[tweet.index("【") + 1:tweet.rindex("】")]

            for each in words:
                if rlink.search(each):
                    url.append(each)
                elif not rbracket.search(each):
                    youyaku = each

            news = midashi, youyaku
            text.append(news)
        except:
            pass

    return raw_url, text

def get_comment(raw_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    url_list = [] # コメントページurl

    for each in raw_url:
        driver.get(each)
        com_class = driver.find_element_by_class_name("news-comment-plugin")
        c_url = com_class.get_attribute('data-full-page-url')
        url_list.append(c_url)
    
    return url_list

class Scraper(object):
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def kiji(self, url):
        self.driver.get(url)
        self.url = url
        #self.title = self.driver.title

    def crawl(self):
        if not hasattr(self, 'url'):
            raise Exception('call page() before crawl()')

        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, WebDriverException)
            
        while True:
            try:
                comment = self.driver.find_element_by_css_selector('div.news-comment-plugin')
            except ignored_exceptions:
                continue
            break

        # コメントの属性を抽出
        data_sort = comment.get_attribute('data-sort')
        data_order = comment.get_attribute('data-order')
        data_keys = comment.get_attribute('data-keys')
        data_full_page_url = comment.get_attribute('data-full-page-url')
        data_comment_num = comment.get_attribute('data-comment-num')
        page = 1

        while True:
            print (u'--- Page %d ---' % page)

            try:
                com_url = 'https://news.yahoo.co.jp/comment/plugin/v1/full/?' + \
                        'origin=https%3A%2F%2Fheadlines.yahoo.co.jp' + '&' + \
                        'sort=' + data_sort + '&' + \
                        'order=' + data_order + '&' + \
                        'page=' + str(page) + '&' + \
                        'type=' + 't' + '&' + \
                        'keys=' +  data_keys + '&' + \
                        'full_page_url=' +  data_full_page_url + '&' + \
                        'comment_num=' +  data_comment_num + '&' + \
                        'ref=' + '&' + \
                        'bkt=' + '&' + \
                        'flt=' + '&' + \
                        'disable_total_count=' + '&' + \
                        'compact=' + '&' + \
                        'compact_initial_view=' + '&' + \
                        'display_author_banner=' + 'off' + '&' + \
                        'ua=' + 'Mozilla%2F5.0+(Windows+NT+6.3%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F58.0.3029.110+Safari%2F537.36'
            except:
                continue

            # コメントページ 取得
            self.driver.get(com_url)

            # 「返信」 リンクを click
            while True:
                try:
                    henshin = self.driver.find_elements_by_css_selector('a.btnView.expandBtn')
                except ignored_exceptions:
                    continue
                break
            for link in henshin:
                link.click()
                time.sleep(1)
            
            # 「返信」 リンクを 表示
            while True:
                try:
                    link_hyouji = self.driver.find_elements_by_css_selector('a.moreReplyCommentList')
                except ignored_exceptions:
                    continue
                break
            for view_link in link_hyouji:
                while view_link.is_displayed():
                    view_link.click()
                    time.sleep(2)
    
            # コメント 取り出し
            comments = self.driver.find_elements_by_css_selector('li[id^="comment-"]')
            for comment in comments:
                rootComments = comment.find_elements_by_css_selector('div.action article.root')
                if len(rootComments) == 0:
                    continue
            
                rootComment = rootComments[0]
                comment_reply = {'user': rootComment.find_elements_by_css_selector('h1.name a')[0].text,
                                 'date': rootComment.find_elements_by_css_selector('time.date')[0].text.strip(),
                                 'comment': rootComment.find_elements_by_css_selector('p span.cmtBody')[0].text,
                                 'agree': rootComment.find_elements_by_css_selector('a.agreeBtn.emotion_tapArea.rapid-noclick-resp span.userNum')[0].text,
                                 'disagree' : rootComment.find_elements_by_css_selector('a.disagreeBtn.emotion_tapArea.rapid-noclick-resp span.userNum')[0].text
                                }
        
                # 返信コメント 取り出し
                henshinList = []
                replys = comment.find_elements_by_css_selector('li[id^="reply-"]')
                for reply in replys:
                    cmtBodies = reply.find_elements_by_css_selector('div.action article p span.cmtBody')
                    if len(cmtBodies) == 0:
                        continue
            
                    henshinList.append({'user': reply.find_elements_by_css_selector('h1.name a')[0].text,
                                       'date': reply.find_elements_by_css_selector('time.date')[0].text.strip(),
                                       'comment': cmtBodies[0].text,
                                       'agree': reply.find_elements_by_css_selector('a.agreeBtn.emotion_tapArea.rapid-noclick-resp span.userNum')[0].text,
                                       'disagree': reply.find_elements_by_css_selector('a.disagreeBtn.emotion_tapArea.rapid-noclick-resp span.userNum')[0].text
                                       })
        
                comment_reply['replies'] = henshinList
                yield comment_reply

            # 「次へ」を確認
            nextLink = self.driver.find_elements_by_css_selector('ul.pagenation li.next a')
            if len(nextLink) > 0:
                time.sleep(2)
                page += 1
            else:
                break

if __name__ == '__main__':
    # 初期化
    #url = get_page()
    #get_comment(url)

    url = 'https://headlines.yahoo.co.jp/cm/main?d=20200521-00000034-jij-pol'

    scraper = Scraper()
    scraper.kiji(url)

    data = []

    data_set = {
        "midashi": "hello",
        "youyaku": "world",
        "kiji_id": 1,
        "comments": {}
    }

    for i, c in enumerate(scraper.crawl()):

        #print (u'----- コメント %d --------------------------' % (i+1))
        data_set["comments"][c['comment']]  = []
        j_com = data_set["comments"][c['comment']]
        j_com.append('agree %s  disagree %s' % (c['agree'], c['disagree']))

        for j, r in enumerate(c['replies']):
            #print ('')
            print (u'(返信 %d)' % (j+1))
            print (r['comment'])
            print ('Y %s  N %s' % (r['agree'], r['disagree']))

        j_com.append()

        print ('\n')









# for i, c in enumerate(scraper.crawl()):

#         print (u'----- コメント %d --------------------------' % (i+1))
#         print (c['comment'])
#         print ('Y %s  N %s' % (c['agree'], c['disagree']))

#         for j, r in enumerate(c['replies']):
#             print ('')
#             print (u'(返信 %d)' % (j+1))
#             print (r['comment'])
#             print ('Y %s  N %s' % (r['agree'], r['disagree']))

#         print ('\n')