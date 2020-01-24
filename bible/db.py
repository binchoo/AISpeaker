from . models import KlvBible, BibleBooksKlv
from django.db import connections
import re

class Iterator :

    __creatable = False

    @staticmethod
    def fromModel(model_obj) :
        Iterator.__creatable = True
        iterator = Iterator()
        iterator.setModelObject(model_obj)

        Iterator.__creatable = False
        return iterator

    def __init__(self) :
        '''
        이 클래스의 생성자는 Private 생성자로서 행동합니다
        '''
        assert(Iterator.__creatable)
        self.cursor = 0
        self.model_obj = None

    def setCursor(self, cursor) :
        self.cursor = cursor
        return self

    def setModelObject(self, model_obj) :
        self.model_obj = model_obj
        return self
    
    #To Do : id가 0에서 부터 생성되는지, 1에서부터 생성되는지 확인할 것
    def hasNext(self) :
        return self.cursor < self.model_obj.count()

    def next(self) :
        next_one = self.model_obj.filter(id=self.cursor)
        self.cursor += 1
        return next_one

class BatchIterator(Iterator) :

    __creatable = False

    @staticmethod
    def fromModel(model_obj) :
        BatchIterator.__creatable = True
        iterator = BatchIterator()
        iterator.setModelObject(model_obj)

        BatchIterator.__creatable = False
        return iterator

    def __init__(self) :
        '''
        이 클래스의 생성자는 Private 생성자로서 행동합니다
        '''
        assert(BatchIterator.__creatable)
        self.cursor = 0
        self.model_obj = None
        self.batch = 1

    def setBatch(self, batch) :
        self.batch = batch
        return self

    def next(self) :
        if self.batch == 1 :
            super().next()
        else :
            first_id = self.cursor
            last_id = self.cursor + self.batch - 1
            next_one = self.model_obj.filter(id__gte=first_id, id__lte=last_id)
            self.cursor = last_id + 1
        return next_one

class BibleReader() :

    __regexs = {
        'book': re.compile(r"(창세기|출애굽기|레위기|민수기|신명기|여호수아|사사기|룻기|사무엘상|사무엘하|열왕기상|열왕기하|역대상|역대하|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도행전|로마서|고린도전서|고린도후서|갈라디아서|에베소서|빌립보서|골로새서|데살로니가전서|데살로니가후서|디모데전서|디모데후서|디도서|빌레몬서|히브리서|야고보서|베드로전서|베드로후서|요한1서|요한2서|요한3서|유다서|요한계시록)"),
        'chapter': re.compile(r"\d+장"),
        'verse': re.compile(r"\d+절"),
    }
    __seperator = re.compile(r"에서|부터")

    def __init__(self) :
        self.bible = BatchIterator.fromModel(KlvBible.objects)

    def _splitQuery(self, query) :
        splitted_query = BibleReader.__seperator.split(query)
        if len(splitted_query) < 2 :
            left_query, right_query = query, None
        else :
            left_query, right_query = splitted_query
        return left_query, right_query

    def _findKeyword(self, regex, query) :
        '''
        정규표현식을 사용하여 사용자 질의에서 중요 키워드(책, 장 절)를 추출해냅니다
        '''
        found = regex.findall(query)
        if len(found) == 1 :
            return found[0]
        else :
            return None

    def _makeVerboseLabel(self, query) :
        if query is not None :
            label = dict()
            for key, regex in BibleReader.__regexs.items() :
                label[key] = self._findKeyword(regex, query)
            return label
        else :
            return None

    def _validateVerboseLabel(self, left, right) :
        '''
        좌측 BCV 레이블과 우측 BCV 레이블을 유효하게 만듭니다
        매개변수로 받은 left와 right의 내용이 변경되니 주의하세요
        '''
        if right is not None :
            for key, val in right.items() :
                if val is None :
                    right[key] = left[key]
        else :
            right = left

        for key, val in left.items() :
            if val is None :
                left[key] = '1 '

    def _parseVerboseLabelToRowId(self, label) :
        '''
        BCV 레이블이 성경 데이터베이스 상에서 몇 번째 행에 위치하는지 계산합니다
        '''
        book = BibleBooksKlv.objects.filter(book = label['book'])
        chapter = label['chapter'][:-1]
        verse = label['verse'][:-1]
        row = KlvBible.objects.get(book__exact=book, chapter=chapter, verse=verse)
        return row.id

    def _parseVerboseLabelIntoTitle(self, left, right) :
        '''
        좌측 BCV 레이블과 우측 BCV 레이블이 나타내는 범위를 타이틀로 전시할 수 있는 문자열로 반환합니다
        '''
        title = "{} {}:{}".format(left['book'], left['chapter'][:-1], left['verse'][:-1])
        if right is not None :
            title += "~ {} {}:{}".format(right['book'], right['chapter'][:-1], right['verse'][:-1])
        return title

    def _parseQuery(self, query) :
        left_query, right_query = self._splitQuery(query)
        start = self._makeVerboseLabel(left_query)
        end = self._makeVerboseLabel(right_query)
        self._validateVerboseLabel(start, end)
        return start, end

    def search(self, query) :
        '''
        사용자 질의가 요구하는 성경의 범위를 파악하여
        해당하는 성경 텍스트를 반환합니다.
        '''
        start, end = self._parseQuery(query)
        print(start, end)

        title = self._parseVerboseLabelIntoTitle(start, end)

        id_start = self._parseVerboseLabelToRowId(start)
        id_end = self._parseVerboseLabelToRowId(end)
        assert(id_start <= id_end)
        print(id_start, id_end)

        contents = self.bible.setCursor(id_start).setBatch(id_end - id_start + 1).next()
        return title, contents

    def readMore(self) :
        return self.bible.setBatch(4).next()
