from django.contrib import admin
from .models import ContaPaga, ContaPagar

class ContaPagaInline(admin.StackedInline):
    model = ContaPaga
    extra = 1

class ContaPagarAdmin(admin.ModelAdmin):
    inlines = [ContaPagaInline]

admin.site.register(ContaPagar, ContaPagarAdmin)