from django.contrib import admin
from . models import BibleBooksKlv, Bquad, KlvBible, KlvOutline
# Register your models here.

admin.site.register(BibleBooksKlv)
admin.site.register(KlvBible)
admin.site.register(KlvOutline)
