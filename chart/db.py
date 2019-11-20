from . models import StockSeries, Company
from datetime import datetime
import pandas as pd
import os

#helpers
series_cols = {0 : 'time', 1 : 'close', 3 : 'open', 4 : 'high', 5 : 'low',}
def stock_crawller(stock_id, page_num=1):
    '''
    상장기업의 상장번호로 네이버 금융 페이지에서 주가를 크롤링 해 옵니다.
    page_num이 15라면 1페이지 ~ 15페이지 까지 크롤링 해 옵니다.
    크롤링 결과의 레이블을 알맞게 처리한 후 list of dict로 반환합니다.
    '''
    pdf = pd.DataFrame()
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=stock_id)
    
    for page in range(1, page_num + 1):
        page_url = '{url}&page={page}'.format(url=url, page=page) 
        pdf = pdf.append(pd.read_html(page_url, header=0)[0], ignore_index=True)
    
    pdf = pdf.dropna()
    pdf = pdf.drop(['거래량', '전일비'],axis=1)
    pdf.columns = series_cols.values()
    
    data = []
    for r in range(0, len(pdf)) :
        row = pdf.iloc[r].to_dict()
        row['time'] = datetime.strptime(row['time'], '%Y.%m.%d').strftime('%Y-%m-%d')
        data.append(row)
    return data
    
class StockDBBuilder :

    page_max_num = 20
    
    def addNewCompany(self, stock_id, com_name) :
        com, created = Company.objects.update_or_create(stock_id=stock_id, company_name=com_name)
        if created :
            com.save_data()
            stock_data = stock_crawller(stock_id, page_num=StockDBBuilder.page_max_num)
            for each_data in stock_data :
                each_data['ofWhich'] = com
                ss, created = StockSeries.objects.update_or_create(**each_data)
                if created :
                    ss.save_data()
            print('added a new company : ' + com.__str__())

    def updateOnePage(self, rows=10) :
        '''
        모든 회사 주가의 최근 한 페이지의 rows개 열을 db에 갱신합니다.
        '''
        num = 0
        for com in Company.objects.all() :
            stock_data = stock_crawller(com.stock_id, page_num=1)
            for each_data in stock_data[:rows] :
                each_data['ofWhich'] = com
                ss, created = StockSeries.objects.update_or_create(**each_data)
                if created :
                    ss.save_data()
            num += 1
            print('updated {} companies.'.format(num))
    
    def updateWholePage(self) :
        '''
        모든 회사에 대하여 주가 한 페이지를 크롤링하여 갱신합니다.
        '''
        num = 0
        for com in Company.objects.all() :
            stock_data = stock_crawller(com.stock_id, page_num=StockDBBuilder.page_max_num)
            for each_data in stock_data :
                each_data['ofWhich'] = com
                ss, created = StockSeries.objects.update_or_create(**each_data)
                if created :
                    ss.save_data()
            num += 1
            print('updated {} companies.'.format(num))

    def DBMigration(self, org, dest) :
        '''
        org db에 속한 Company와 StockSeries를
        dest db로 복사합니다.
        '''
        print('migration begins')
        origin = Company.objects.using(org).all()
        for row in origin :
            row.save_data()
        
        origin = StockSeries.objects.using(org).all()
        for row in origin :
            row.save_data()
        print('migration {} to {} has done.'.format(org, dest))

class StockDataGetter :

    def getStockData(self, symbol) :
        search_set = StockSeries.objects.filter(ofWhich__company_name=symbol) \
            .values('time', 'high', 'low', 'open', 'close')
        for row in search_set :
            row['time'] = str(row['time'])
        return list(search_set)

class CompanyDataGetter :

    def recogCompanyName(self, question) :
        found = None
        for com in Company.objects.all().values('company_name') :
            if com['company_name'] in question :
                found = com['company_name']
                break
        return found