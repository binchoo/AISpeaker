# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class BibleBooksKlv(models.Model):
    book_number = models.IntegerField(primary_key=True)
    korean = models.CharField(max_length=20)
    k_abb = models.CharField(max_length=6)
    english = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=3)
    book = models.CharField(max_length=3)
    chapter_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bible_books_klv'
        app_label = 'bible'

    def __str__(self) :
        return '{} {}'.format(self.book_number, self.korean)

    def save_data(self) :
        self.save(using=self._meta.app_label)


class Bquad(models.Model):
    paragraph_id = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()
    answer_start = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bquad'
        app_label = 'bible'

    def __str__(self) :
        return '{}'.format(self.paragraph_id)

    def save_data(self) :
        self.save(using=self._meta.app_label)


class KlvBible(models.Model):
    book = models.CharField(max_length=3)
    chapter = models.IntegerField()
    verse = models.IntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'klv_bible'
        app_label = 'bible'

    def __str__(self) :
        return '{} {}장 {}절'.format(self.book, self.chapter, self.verse)

    def save_data(self) :
        self.save(using=self._meta.app_label)


class KlvOutline(models.Model):
    title = models.TextField()
    start_id = models.IntegerField()
    end_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'klv_outline'
        app_label = 'bible'

    def __str__(self) :
        return '{} {} {}'.format(self.title, self.start_id, self.end_id)

    def save_data(self) :
        self.save(using=self._meta.app_label)
