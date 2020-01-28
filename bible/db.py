from . models import KlvBible, BibleBooksKlv
from django.db.models.manager import Manager
from django.db import connections
import re

class Iterator :

    @classmethod
    def fromModel(cls, model_obj) :
        iterator = cls()
        iterator.setModelObject(model_obj)
        return iterator

    def __init__(self) :
        self.cursor = 0
        self.model_obj = None

    def setCursor(self, cursor) :
        self.cursor = cursor
        return self

    def setModelObject(self, model_obj) :
        if isinstance(model_obj, Manager) :
            self.model_obj = model_obj
        else :
            print(type(model_obj))
            raise ValueError('Please inject an instance of django.db.models.manager.Manager')
        return self
    
    #To Do : id가 0에서 부터 생성되는지, 1에서부터 생성되는지 확인할 것
    def hasNext(self) :
        return self.cursor < self.model_obj.count()

    def next(self) :
        next_one = self.model_obj.filter(id=self.cursor)
        self.cursor += 1
        return next_one

class BatchIterator(Iterator) :

    def __init__(self) :
        super(BatchIterator, self).__init__()
        self.batch = 1

    def setBatch(self, batch) :
        if batch < 1 :
            raise Exception
        self.batch = batch
        return self

    def next(self) :
        first_id = self.cursor
        last_id = self.cursor + self.batch - 1
        next_one = self.model_obj.filter(id__gte=first_id, id__lte=last_id)
        self.cursor = last_id + 1
        return next_one

class BibleReader() :

    __seperator = re.compile(r"에서|부터")
    __batch_lines = 4

    @classmethod
    def fromQuery(cls, query) :
        reader = cls()
        reader.parse(query)
        return reader

    def __init__(self) :
        self.bible = BatchIterator.fromModel(KlvBible.objects)

    def _splitQuery(self, query) :
        '''
        정규표현식 __seperator = re.compile(r"에서|부터") 를 사용하여
        사용자의 질문을 둘로 쪼갭니다. 쪼갤 수 없을 경우 
        튜플 query, None을 반환합니다
        '''
        splitted_query = BibleReader.__seperator.split(query)
        if len(splitted_query) < 2 :
            left_query, right_query = query, None
        else :
            left_query, right_query = splitted_query
        return left_query, right_query

    def _makeTitle(self) :
        '''
        지정된 데이터베이스 범위를 {} {}:{} ~ {} {}:{} 꼴로 표현합니다
        '''
        title_form = "{} {}:{}"
        try :
            start = title_form.format(self._bookIdToKortitle(self.start.book), self.start.chapter, self.start.verse)
            end = title_form.format(self._bookIdToKortitle(self.end.book), self.end.chapter, self.end.verse)
        except :
            raise self.BibleScopeError('your designated scope is unacceptable.')
        return start + "~" + end
        
    def _makeContents(self) :
        '''
        지정된 범위의 성경 데이터베이스를 읽어들여 문자열로 취합해 반환합니다
        '''
        contents = None
        try :
            batch = self.end.id - self.start.id + 1
            query_set = self.bible.setCursor(self.start.id).setBatch(batch).next()
            contents = self._mergeQuerySetString(query_set)
            self.bible.setBatch(BibleReader.__batch_lines)
        except :
            raise self.BibleScopeError('your designated scope is unacceptable.')
        return contents

    def _nextQuerySet(self) :
        query_set = self.bible.next()
        self.end = query_set.last()
        return query_set

    def _mergeQuerySetString(self, query_set) :
        return "".join([row.data for row in query_set])

    def parse(self, query) :
        '''
        사용자 질의가 요구하는 성경의 범위를 파악합니다
        '''
        left_verbose, right_verbose = None, None
        keys_with_order=('book', 'chapter', 'verse')

        for n, splitted_query in enumerate(self._splitQuery(query)) :
            if splitted_query is not None :
                verbose = BibleReader.VerboseLabel.fromQuery(splitted_query)
                if n == 0 :
                    left_verbose = verbose
                else :
                    right_verbose = verbose.adjustToLeft(left_verbose, keys_with_order)
            elif n == 1 :
                right_verbose = left_verbose
            
        self.start = left_verbose.narrowQuerySet(KlvBible.objects, keys_with_order).first()
        self.end = right_verbose.narrowQuerySet(KlvBible.objects, keys_with_order).last()
        return self

    def read(self) :
        '''
        지정된 성경 범위를 웹 페이지에 표시할 타이틀과 컨텐츠로 만들어 반환합니다
        '''
        title = self._makeTitle()
        contents = self._makeContents()
        return title, contents

    # To Do : kortitle로 조회가능하도록 자료구조를 바꾸자. 
    # 혹은 2자리 영어 book을 kortitle과 매칭하는 테이블을 메모리에 올려두자
    def readMore(self) :
        '''
        여태 읽어들인 위치에서부터
        __batch_lines 만큼의 구절을 더 읽어들여 반환합니다
        '''
        query_set = self._nextQuerySet()
        title = self._makeTitle()
        contents = self._mergeQuerySetString(query_set)
        return title, contents

    @staticmethod
    def _kortitleToBookId(kortitle) :
        return BibleBooksKlv.objects.get(korean=kortitle).book

    @staticmethod
    def _bookIdToKortitle(book_id) :
        return BibleBooksKlv.objects.get(book=book_id).korean

    class VerboseLabel :

        __regexs = {
        'book': re.compile(r"(창세기|출애굽기|레위기|민수기|신명기|여호수아|사사기|룻기|사무엘상|사무엘하|열왕기상|열왕기하|역대상|역대하|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도행전|로마서|고린도전서|고린도후서|갈라디아서|에베소서|빌립보서|골로새서|데살로니가전서|데살로니가후서|디모데전서|디모데후서|디도서|빌레몬서|히브리서|야고보서|베드로전서|베드로후서|요한1서|요한2서|요한3서|유다서|요한계시록)"),
        'chapter': re.compile(r"\d+장"),
        'verse': re.compile(r"\d+절"),
        }

        @classmethod
        def fromQuery(cls, query) :
            attributes = cls.getKeywordsInQuery(query)
            return cls(**attributes)

        @classmethod
        def getKeywordsInQuery(cls, query) :
            key_val = dict()
            for key, regex in cls.__regexs.items() :
                found = regex.findall(query)
                if len(found) == 1 :
                    key_val[key] = found[0]
                else :
                    key_val[key] = None
            return key_val
           
        def __init__(self, **kwargs) :
            if len(kwargs) > 0 :
                self.label = kwargs
            else :
                self.label = dict()

        def adjustToLeft(self, left, keys_with_order) :
            for key in keys_with_order :
                if self.getField(key) is None :
                    self.setField(key, left.getField(key))
                else :
                    break
            return self

        def setField(self, key, value) :
            self.label[key] = value
        
        def getField(self, key) :
            return self.label[key]

        def getUnverboseField(self, key) :
            val = self.label[key]
            if val is not None :
                if key == 'book' :
                    return BibleReader._kortitleToBookId(val)
                else:
                    return val[:-1]
            else :
                return None

        def narrowQuerySet(self, model_obj, keys_with_order) :
            row = model_obj
            print(self.label)
            for key in keys_with_order :
                unverbose_value = self.getUnverboseField(key)
                if unverbose_value is not None :
                    row = row.filter(**{key : unverbose_value})
            return row

    class BibleScopeError(Exception) :
        pass
