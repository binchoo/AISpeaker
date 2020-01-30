from . models import KlvBible, BibleBooksKlv
from django.db.models.manager import Manager
from django.db import connections
import re

class Iterator :

    @classmethod
    def from_model(cls, model_obj) :
        iterator = cls()
        iterator.set_model_obj(model_obj)
        return iterator

    def __init__(self) :
        self.cursor = 0
        self.model_obj = None

    def set_cursor(self, cursor) :
        self.cursor = cursor
        return self

    def set_model_obj(self, model_obj) :
        if isinstance(model_obj, Manager) :
            self.model_obj = model_obj
        else :
            print(type(model_obj))
            raise ValueError('Please inject an instance of django.db.models.manager.Manager')
        return self
    
    #To Do : id가 0에서 부터 생성되는지, 1에서부터 생성되는지 확인할 것
    def has_next(self) :
        return self.cursor < self.model_obj.count()

    def next(self) :
        next_one = self.model_obj.filter(id=self.cursor)
        self.cursor += 1
        return next_one

class BatchIterator(Iterator) :

    def __init__(self) :
        super(BatchIterator, self).__init__()
        self.batch = 1

    def set_batch(self, batch) :
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

    __SEPERATOR = re.compile(r"에서|부터")
    __BATCH_LINES = 4

    @classmethod
    def from_query(cls, query) :
        reader = cls()
        reader.parse(query)
        return reader

    def __init__(self) :
        self.bible = BatchIterator.from_model(KlvBible.objects)

    #TODO 이 메서드는 speakerapp.utils.QueryAnalyzer로 편입하자.
    def parse(self, query) :
        left_query, right_query = self._split_query(query)
        left_verbose, right_verbose = self._make_verboselabels(left_query, right_query)   
        self.start_row = left_verbose.fetch_first_of(KlvBible.objects)
        self.end_row = right_verbose.fetch_last_of(KlvBible.objects)
        return self
    
    #TODO 이 메서드는 speakerapp.utils.QueryAnalyzer로 편입하자.
    def _split_query(self, query) :
        splitted_query = BibleReader.__SEPERATOR.split(query)
        if len(splitted_query) < 2 :
            left_query, right_query = query, None
        else :
            left_query, right_query = splitted_query
        return left_query, right_query

    #TODO 이 메서드는 speakerapp.utils.QueryAnalyzer로 편입하자.
    def _make_verboselabels(self, left_query, right_query) :
        left_verbose = BibleReader.VerboseLabel.from_query(left_query)
        if right_query :
            right_verbose = BibleReader.VerboseLabel.from_query(right_query)
            right_verbose.adjust_to_left(left_verbose)
        else :
            right_verbose = left_verbose
        return left_verbose, right_verbose

    def read(self) :
        title = self._make_title()
        contents = self._make_contents()
        return title, contents

    def readmore(self) :
        query_set = self._next_queryset()
        title = self._make_title()
        contents = self._merge_queryset_string(query_set)
        return title, contents

    def _make_title(self) :
        '''
        지정된 데이터베이스 범위를 {} {}:{} ~ {} {}:{} 꼴로 표현한다
        '''
        start_title = self._make_title_from_row(self.start_row)
        end_title = self._make_title_from_row(self.end_row, self.start_row)
        return start_title + " ~ " + end_title

    def _make_title_from_row(self, row, *args) :
        try :
            if args and args[0].book == row.book :
                title = "{}:{}".format(row.chapter, row.verse)
            else :
                title = "{} {}:{}".format(self._bookid2kortitle(row.book), row.chapter, row.verse)
        except :
            raise self.BibleScopeError('your designated scope is unacceptable.')
        return title
        
    def _make_contents(self) :
        contents = None
        try :
            batch = self.end_row.id - self.start_row.id + 1
            query_set = self.bible.set_cursor(self.start_row.id).set_batch(batch).next()
            contents = self._merge_queryset_string(query_set)
            self.bible.set_batch(BibleReader.__BATCH_LINES)
        except :
            raise self.BibleScopeError('your designated scope is unacceptable.')
        return contents

    def _next_queryset(self) :
        query_set = self.bible.next()
        self.end_row = query_set.last()
        return query_set

    @staticmethod
    def _merge_queryset_string(query_set) :
        return "".join([row.data for row in query_set])

    @staticmethod
    def _kortitle2bookid(kortitle) :
        return BibleBooksKlv.objects.get(korean=kortitle).book

    @staticmethod
    def _bookid2kortitle(book_id) :
        return BibleBooksKlv.objects.get(book=book_id).korean

    #TODO 이 클래스를 일반화하여 speakerapp.utils.QueryAnalyzer로 편입하자.
    class VerboseLabel :

        __REGEXS = {
            'book': re.compile(r"(창세기|출애굽기|레위기|민수기|신명기|여호수아|사사기|룻기|사무엘상|사무엘하|열왕기상|열왕기하|역대상|역대하|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도행전|로마서|고린도전서|고린도후서|갈라디아서|에베소서|빌립보서|골로새서|데살로니가전서|데살로니가후서|디모데전서|디모데후서|디도서|빌레몬서|히브리서|야고보서|베드로전서|베드로후서|요한1서|요한2서|요한3서|유다서|요한계시록)"),
            'chapter': re.compile(r"\d+장"),
            'verse': re.compile(r"\d+절"),
        }
        _KEYS_ORDERED_DESCENDING_HIERARCHY = [
            'book', 'chapter', 'verse'
        ]

        @classmethod
        def from_query(cls, query) :
            attributes = cls.get_keywords_in_query(query)
            return cls(**attributes)

        @classmethod
        def get_keywords_in_query(cls, query) :
            key_val = dict()
            for key, regex in cls.__REGEXS.items() :
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

        def adjust_to_left(self, left) :
            '''
            오른쪽 쿼리는 이 메소드를 사용할 필요가 있다.
            자신의 빈 레이블을 왼편 쿼리로부터 유추하기 위해서다.
            ex) "창세기 1장 1절부터 10절까지 보여줘"
                left_verbose <- {book:"창세기", chapter:"1장", verse:"10절"}
                right_verbose <- {book:None, chapter:None, verse:"10절"}
                right_query.adjust_to_left(left_query) -> {book:"창세기", chapter:"1장", verse:"10절"}
            '''
            for key in self._KEYS_ORDERED_DESCENDING_HIERARCHY :
                if self.get_field(key) is None :
                    self.set_field(key, left.get_field(key))
                else :
                    break
            return self
        
        def fetch_first_of(self, model_obj) :
            return self.narrow_queryset(model_obj).first()

        def fetch_last_of(self, model_obj) :
            return self.narrow_queryset(model_obj).last()

        def narrow_queryset(self, model_obj) :
            row = model_obj
            for key in self._KEYS_ORDERED_DESCENDING_HIERARCHY :
                unverbose_field = self.get_unverbose_field(key)
                if unverbose_field is not None :
                    row = row.filter(**{key : unverbose_field})
            return row

        def get_unverbose_field(self, key) :
            '''
            KlvBible 데이터베이스의 칼럼 값들은 정수와 같이 단순(Unverbose)하다.
            이 메소드는 Verbose 값 "창세기"를 "1O", "1장"을 "1"로 반환하는 역할을 하고 있다.
            '''
            val = self.label[key]
            if val is not None :
                if key == 'book' :
                    return BibleReader._kortitle2bookid(val)
                else:
                    return val[:-1]
            else :
                return None

        def set_field(self, key, value) :
            self.label[key] = value
        
        def get_field(self, key) :
            return self.label[key]

    class BibleScopeError(Exception) :
        pass
