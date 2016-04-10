from django import forms

from .models import Post

#convention to name after.py file in this case form
class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"title", 
			"body", 
			"author", 
			"categories", 
			"tags",
			"image",
			"draft",
			"publish",
		]
# class AuthorForm(forms.ModelForm):
# 	class Meta:
# 		model = Author
# 		fields = [
# 			"name",
# 			"email",
# 			"bio"
# 		]