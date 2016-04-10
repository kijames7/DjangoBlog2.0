from __future__ import unicode_literals
from django.conf import settings

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify
# Create your models here.

#show non drafts
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	#filebase, extension = filename.split(".")
	#return "%s/%s.%s" %(instance.id, instance.id, filename)
	return "%s/%s" %(instance.id, filename)
class Author(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	bio = models.TextField()

	def __str__(self):
		return self.name

class Category(models.Model):
	cat_name = models.CharField('category name',max_length=50)
	cat_description = models.CharField('category description',max_length=255)

	#fix plural for category
	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.cat_name

class Tag(models.Model):
	tag_name = models.CharField(max_length=50)
	tag_description = models.CharField(max_length=255)

	def __str__(self):
		return self.tag_name

class Post(models.Model):
	#show author of posting
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	#add image files
	image = models.ImageField(upload_to=upload_location, 
		null=True, blank=True, 
		width_field="width_field", 
		height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)

	body = models.TextField()
	#drafts
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)

	created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
	author = models.ForeignKey(Author)

	categories = models.ManyToManyField(Category)
	#categories = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag)
#linking to postManager
	objects = PostManager()
	#TODO add to other classes
	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	#absolute url
	def get_absolute_url(self):
		#kwargs is keyword arguments
		return reverse("posts:detail", kwargs={"slug": self.slug})
		#return "/posts/%s/" %(self.id)

	class Meta:
		ordering = ["-created_date", "-updated_date"]

#cannot have duplicates
# def pre_save_post_reciever(sender, instance, *args, **kwargs):
# 	slug = slugify(instance.title)
# 	exists = Post.objects.filter(slug=slug).exists()
# 	if exists:
# 		slug = "%s-%s" %(slug, instance.id)
# 	instance.slug = slug

#pre_save.connect(pre_save_post_reciever, sender=Post)

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)



