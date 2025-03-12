from django.contrib import admin

from web.models import Articles

@admin.register(Articles)
class WebAdmin(admin.ModelAdmin):
    list_display = ("id", "title",  "create_date", "user")
    list_display_links = ("id", "title")
    list_per_page = 5


# admin.site.register(Articles, WebAdmin)
