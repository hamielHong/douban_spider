#coding:utf-8
import url_manager,html_downloader,html_parser,html_outputer
import time, threading

class SpiderMain(object):
    def __init__(self):
        self.count = 1
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.lock = threading.Lock()

    def url_init(self, movieId):

        for i in range(11):
            start = i * 20
            #https://movie.douban.com/subject/26607693/comments?start=200&limit=20&sort=new_score&status=P
            new_url = 'https://movie.douban.com/subject/' + movieId + '/comments?start='+ str(start) +'&limit=20&sort=new_score'
            self.urls.add_new_url(new_url)

    def thread_craw(self):
        while (self.urls.has_new_url()):
            self.lock.acquire()
            lockb = True
            try:
                new_url = self.urls.get_new_url()
                self.lock.release()
                lockb = False
                content = self.downloader.download(new_url)
                new_data = self.parser.parse(content)
                self.lock.acquire()
                lockb = True
                self.outputer.collect_data(new_data)
                self.lock.release()
                lockb = False
                print('%s craw : %s' % (threading.current_thread().name, new_url))

            except Exception as e:
                print('failed! : %s' % (e))

            finally:
                if lockb:
                    self.lock.release()

        print('%s exit.' % (threading.current_thread().name))

    def run_spider(self, n, movieId):
        self.url_init(movieId)
        threads = []
        for i in range(n):
            thread = threading.Thread(target=self.thread_craw)
            thread.start()  # 线程开始处理任务
            threads.append(thread)

        for thread in threads:
            thread.join()

        try:
            self.outputer.output_html()
        except Exception as e:
            print(e)

        print('Main thread exit.')


if __name__ == "__main__":
    start = time.time()
    movieId = "26607693"
    object_spider = SpiderMain()
    object_spider.run_spider(4, movieId)
    end = time.time()
    print("cost all time: %s" % (end-start))