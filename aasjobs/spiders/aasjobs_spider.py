from __future__ import print_function
import sys, re
import scrapy
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from aasjobs.items import Job

def warning(*objs):
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    print(WARNING, *(objs+(ENDC,)), file=sys.stderr)

class AASJobsSpider(CrawlSpider):
    name = 'aasjobs'

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule( LinkExtractor(allow=('issue', )), follow=False),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('JobID', ), unique=True), callback='parse_item', follow=False),
    )

    def __init__(self, year=None, month=None):
        super(AASJobsSpider, self).__init__()
        if year:
            if month:
                self.start_urls = ['https://jobregister.aas.org/archives/issue?year=%s&month=%s' % (year, month)]
                print('\n'.join(self.start_urls))
            else:
                self.start_urls = [
                    'https://jobregister.aas.org/archives/issue?year=%s&month=%i' % (year, month)
                    for month in range(1, 13)]
        else:
            self.start_urls = ["https://jobregister.aas.org/archives/back_issues"]

    def parse_item(self, response):
        self.log('Found job page %s' % (response.url), log.INFO)
        job = Job()
        jobid = int(re.findall('JobID=(\d+)', response.url)[0])
        title = re.findall(
            '(.*) - JRID\d',
            response.xpath('//h2[@class="title"]/a/text()')[0].extract()
            )[0]
        job['jobid'] = jobid
        job['title'] = title

        fielditems = response.xpath('//div[contains(concat(" ",normalize-space(@class)," "), " field-item " )]')
        # default values
        postdate, deadline, category, city = None, None, None, None
        try:
            for item in fielditems:
                s = item.extract()
                if 'Post Date' in s:
                    postdate = item.xpath('./span/text()').extract()[0]
                if 'Deadline to Apply for Job' in s:
                    deadline = item.xpath('./span/text()').extract()[0]
                if 'Job Category' in s:
                    category = item.xpath('./text()').extract()[1].strip()
                if 'City' in s:
                    city = item.xpath('./text()').extract()[1].strip()
        except IndexError as e:
            pass

        # job description
        desc = response.xpath('//div[@class="field field-type-text field-field-job-announcement"]//div[@class="field-item odd"]//text()').extract()
        descstr = '\n'.join([s.strip() for s in desc if s.strip()])
        job['postdate'] = postdate
        job['deadline'] = deadline
        job['category'] = category
        job['link'] = response.url
        job['description'] = descstr
        # self.log('Job category %s' % (category), log.INFO)
        yield job