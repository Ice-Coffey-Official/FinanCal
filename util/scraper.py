from util.config import years, dataType, scrollTimeOut, pixelScroll, processors, depthExpense, depthRevenue, numSample
from util.utilFun import generate_urls, append_to_json
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from typing import List
from tqdm import tqdm
from multiprocessing import Pool
from util.customLogger import customLogging

class Scraper:
    def __init__(self):
        self.cityURL = "https://counties.bythenumbers.sco.ca.gov/#!/year/2022/operating/0/entity_name"
        self.baseURL = "https://counties.bythenumbers.sco.ca.gov/#!/year/{year}/{expenseType}/0/entity_name/{city}/0/category"
        self.edge_options = Options()
        self.edge_options.add_argument("ms:inPrivate")
        self.edge_options.add_argument("headless")
        self.edge_options.add_argument("disable-gpu")
        self.cityInfo = {}
        self.addUrlExpend = {
            0 : "/{}/0/subcategory_1",
            1 : "/{}/0/subcategory_2",
            2 : "/{}/0/line_description",
            3 : "/{}/0/line_description"
        }

        self.addUrlRevenue = {
            0 : "/{}/0/subcategory_1",
            1 : "/{}/0/subcategory_2",
            2 : "/{}/0/subcategory_3",
            3 : "/{}/0/subcategory_4",
            4 : "/{}/0/line_description",
            5 : "/{}/0/line_description"
        }

        self.levelExpend = {
            0 : "category",
            1 : "sub_category_1",
            2 : "sub_category_2",
            3 : "line_item"
        }
        self.levelRevenue = {
            0 : "category",
            1 : "sub_category_1",
            2 : "sub_category_2",
            3 : "sub_category_3",
            4 : "sub_category_4",
            5 : "line_item"
        }


    def slowScroll(self, driver, count=400, timeout=1000):
        try:
            script = """
                count = {count};
                let callback = arguments[arguments.length - 1];
                t = setTimeout(function scrolldown() {{
                    console.log(count, t);
                    window.scrollTo(0, count);
                    if (count < (document.body.scrollHeight || document.documentElement.scrollHeight)) {{
                        count += {count};
                        t = setTimeout(scrolldown, {timeout});
                    }} else {{
                        callback((document.body.scrollHeight || document.documentElement.scrollHeight));
                    }}
                }}, {timeout});
            """.format(count=count, timeout=timeout)
            driver.execute_async_script(script=script)
        except TimeoutException:
            logger.info("Script TimeOutException in SlowScroll()")
    

    def getCities(self):
        driver = webdriver.Edge(options=self.edge_options)
        driver.get(self.cityURL)
        self.slowScroll(driver, count=pixelScroll, timeout=scrollTimeOut)
        elements = driver.find_elements(by=By.CLASS_NAME, value="trigger-click-on-enter.ng-scope")
        return [elem.find_element(by=By.CLASS_NAME, value="ng-binding.ng-scope").text.replace(' ', '+') for elem in elements]
    

    def getDataPoint(self, url, depth, expenseType, pid):
        cLog = customLogging(name=str(pid))
        logger = cLog.getLogger()

        driver = webdriver.Edge(options=self.edge_options)
        driver.get(url=url)
        self.slowScroll(driver=driver,count=pixelScroll, timeout=scrollTimeOut)
        elements = driver.find_elements(by=By.CLASS_NAME, value="trigger-click-on-enter.ng-scope")
        if(expenseType.lower() == "revenue"):
            if(depth >= depthRevenue):
                logger.info("process named {pid} has reached depth {depth} in {etype} for {city}. Returning result for {url}.".format(pid=pid,depth=depth,etype=expenseType,city=url.split('/')[9],url=url))
                return [{self.levelRevenue[depth] + "_name":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[0].text,"gross":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[1].text,"percent":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[2].text} for elem in elements]
            logger.info("process named {pid} has reached depth {depth} in {etype} for {city}.".format(pid=pid,depth=depth,etype=expenseType,city=url.split('/')[9]))
            return [{self.levelRevenue[depth] + "_name":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[0].text,"gross":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[1].text,"percent":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[2].text, self.levelRevenue[depth+1] : self.getDataPoint(url=(url+self.addUrlRevenue[depth]).format((elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[0].text.replace(' ', '+'))), depth=depth+1, expenseType=expenseType, pid=pid)} for elem in elements]
        else:
            if(depth >= depthExpense):
                logger.info("process named {pid} has reached depth {depth} in {etype} for {city}. Returning result for {url}.".format(pid=pid,depth=depth,etype=expenseType,city=url.split('/')[9],url=url))
                return [{self.levelExpend[depth] + "_name":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[0].text,"gross":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[1].text,"percent":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[2].text} for elem in elements]
            logger.info("process named {pid} has reached depth {depth} in {etype} for {city}.".format(pid=pid,depth=depth,etype=expenseType,city=url.split('/')[9]))
            return [{self.levelExpend[depth] + "_name":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[0].text,"gross":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[1].text,"percent":elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[2].text, self.levelExpend[depth+1] : self.getDataPoint(url=(url+self.addUrlExpend[depth]).format((elem.find_elements(by=By.CLASS_NAME, value="ng-binding.ng-scope")[0].text.replace(' ', '+'))), depth=depth+1, expenseType=expenseType, pid=pid)} for elem in elements]


    '''def generateData(self, urls : List[tuple]):
        for i in range(len(urls)):
            url, city, expense_type, year, pid = urls[i]
            
            append_to_json(city, {expense_type + " " + str(year) : self.getDataPoint(url, 0, expense_type)})'''
            

    def run(self):
        urls = generate_urls(base_url=self.baseURL, years=years, expense_types=dataType,cities=self.getCities())
        self.run_in_parallel(urls)

    def runSample(self, logger):
        urls = generate_urls(base_url=self.baseURL, years=years, expense_types=dataType,cities=self.getCities())
        sampleURLs = urls[-1*numSample:]
        #logger.info("{0} sample URLs tested.\nThey are:\n{1}\n{2}\n{3}\n{4}\n". format((len(sampleURLs)), sampleURLs[0], sampleURLs[1], sampleURLs[2], sampleURLs[3]))
        self.run_in_parallel(sampleURLs)

    def process_url(self, url_data):
        url, city, expense_type, year, pid = url_data
        data_point = self.getDataPoint(url, 0, expense_type, pid)
        append_to_json(city, {f"{expense_type} {year}": data_point})

    def run_in_parallel(self, urls):
        with Pool(processes=processors) as pool:
            pool.map(self.process_url, urls)


if __name__ == "__main__":
    cLog = customLogging(name='Parent')
    logger = cLog.getLogger()
    myScraper = Scraper()
    logger.info("Initialized scraper... Running Sample...")
    myScraper.runSample(logger=logger)
