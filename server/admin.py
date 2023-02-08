from django import forms
from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm


admin.site.register(Voting)
admin.site.register(Question)
admin.site.register(News, NewsAdmin)
admin.site.register(Chat)
admin.site.register(Message)
