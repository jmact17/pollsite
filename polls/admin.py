from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 # 3 slots for choices

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    # display field names as columns on change list page
    list_display = ('question_text', 'pub_date', 'was_published_recently') 
    # sidebar to filter by date
    list_filter = ['pub_date']
    # search box
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)