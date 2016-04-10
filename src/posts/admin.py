from django.contrib import admin
from .models import Post, Author, Category, Tag
# Register your models here.
#params to list in the admin
class PostModelAdmin(admin.ModelAdmin):
	#model admin options 
	#list of params to show on the admin page
	list_display = ["title", "author", "created_date", "updated_date"]
	#which params to use as links
	list_display_links = ["created_date"]
	#filter function
	list_filter = ["created_date", "updated_date"]
	#search bar
	search_fields = ["title", "author"]
	#make a param be able to edit
	list_editable = ["title"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)
