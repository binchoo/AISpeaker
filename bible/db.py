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

    __regexs = {
        'book': re.compile(r"(창세기|출애굽기|레위기|민수기|신명기|여호수아|사사기|룻기|사무엘상|사무엘하|열왕기상|열왕기하|역대상|역대하|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도행전|로마서|고린도전서|고린도후서|갈라디아서|에베소서|빌립보서|골로새서|데살로니가전서|데살로니가후서|디모데전서|디모데후서|디도서|빌레몬서|히브리서|야고보서|베드로전서|베드로후서|요한1서|요한2서|요한3서|유다서|요한계시록)"),
        'chapter': re.compile(r"\d+장"),
        'verse': re.compile(r"\d+절"),
    }
    __seperator = re.compile(r"에서|부터")
    __batch_lines = 4

    @staticmethod
    def fromQuery(query) :
        reader = BibleReader()
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

    def _queryToVerboseLabel(self, query) :
        '''
        query로 부터 book, chapter, verse를 키로 갖는
        딕셔너리를 두 개를 얻습니다.
        각각 자료의 시작과 자료의 끝 위치를 의미합니다
        '''
        left_query, right_query = self._splitQuery(query)
        start, end = None, None
        if left_query is not None :
            start = self._makeVerboseLabel(left_query)
        if right_query is not None :
            end = self._makeVerboseLabel(right_query)
        self._validateVerboseLabel(start, end)
        if end is None :
            end = start
        return start, end

    def _makeVerboseLabel(self, query) :
        '''
        query로 부터 book, chapter, verse를 키로 갖는
        딕셔너리를 얻습니다. query는 __seperator = re.compile(r"에서|부터")를 사용하여 분할된 query여야 합니다.
        '''
        label = dict()
        for key, regex in BibleReader.__regexs.items() :
            label[key] = self._findKeyword(regex, query)
        return label

    def _findKeyword(self, regex, query) :
        '''
        사용자 질의에 정규표현식을 적용하여 키워드를 추출합니다
        '''
        found = regex.findall(query)
        if len(found) == 1 :
            return found[0]
        else :
            return None

    def _kortitleToBookId(self, kortitle) :
        '''
        한국어 성경이름을 O(구약)1(순서), N(신약)1(순서) 형태로 바꿉니다
        '''
        if kortitle is not None :
            return BibleBooksKlv.objects.get(korean=kortitle).book
        else :
            return None

    def _verboseLabelToQuerySet(self, label) :
        '''
        레이블이 의미하는 대로 데이터베이스 조회 범위를 한정합니다
        '''
        book = self._kortitleToBookId(label['book'])
        row = KlvBible.objects.filter(book=book)
        if label['chapter'] is not None :
            chapter = label['chapter'][:-1]
            row = row.filter(chapter=chapter)
        if label['verse'] is not None :
            verse = label['verse'][:-1]
            row = row.filter(verse=verse)
        return row

    def _validateVerboseLabel(self, left, right) :
        '''
        우측 BCV 레이블 중 빈 값들을 유추합니다.
        문맥에 맞추어 left 값을 복사해 옵니다.
        매개변수로 받은 right의 내용물이 변경되니 주의하세요
        '''        
        keys = ['book', 'chapter', 'verse']
        if right is not None :
            for key in keys :
                if right[key] is None :
                    right[key] = left[key]
                else :
                    break

    def _makeTitle(self) :
        '''
        지정된 데이터베이스 범위를 {} {}:{} ~ {} {}:{} 꼴로 표현합니다
        '''
        title_form = "{} {}:{}"
        start = title_form.format(self.verbose_start['book'], self.start.chapter, self.start.verse)
        end = title_form.format(self.verbose_end['book'], self.end.chapter, self.end.verse)
        return start + "~" + end
        
    def _makeContents(self) :
        '''
        지정된 범위의 성경 데이터베이스를 읽어들여 문자열로 취합해 반환합니다
        '''
        contents = None
        try :
            batch = self.end.id - self.start.id + 1
            query_set = self.bible.setCursor(self.start.id).setBatch(batch).next()
            contents = "".join([row.data for row in query_set])
            self.bible.setBatch(BibleReader.__batch_lines)
        except :
            raise self.BibleScopeError('your designated scope is unacceptable.')
        return contents

    def parse(self, query) :
        '''
        사용자 질의가 요구하는 성경의 범위를 파악합니다
        '''
        self.verbose_start, self.verbose_end = self._queryToVerboseLabel(query)
        self.start = self._verboseLabelToQuerySet(self.verbose_start).first()
        self.end = self._verboseLabelToQuerySet(self.verbose_end).last()
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
        query_set = self.bible.next()
        contents = self._querySetToText(query_set)
        return contents

    class BibleScopeError(Exception) :
        pass
