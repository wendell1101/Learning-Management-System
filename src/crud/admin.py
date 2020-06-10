from django.contrib import admin
from .models import ClassName, Quiz, Question,Announcement,Choice,UserAnswer


admin.site.register(ClassName)

# admin.site.register(Choice)
admin.site.register(Quiz)
# admin.site.register(Quiz)




# class QuestionInline(admin.TabularInline):
#     model = Question
#     extra = 3
# class QuizAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['text']}),
#     ]
#     inlines = [QuestionInline]
class ChoiceInline(admin.TabularInline):
    model = Choice  
    admin.site.register(Choice)
class Question(admin.ModelAdmin):
    inlines=[
        ChoiceInline,
    ]

    admin.site.register(Question)
# admin.site.register(Question)

admin.site.register(Announcement)
admin.site.register(UserAnswer)


# admin.site.register(Quiz, QuizAdmin)
