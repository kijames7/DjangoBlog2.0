from urllib import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
									#looks for object related to some call
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

#import for queryset
from .models import Post
from .forms import PostForm
#TODO
#from .forms import AuthorForm
# Create your views here.
#function based views


def post_create(request):
	#user authenication
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	#forms.py                             for images
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		#get to print on the terminal
		print form.cleaned_data.get("title")
		instance.user = request.user
		instance.save()
		messages.success(request, "Created successfully")
		#redirect after editing
		return HttpResponseRedirect(instance.get_absolute_url())
	#else:
	#	messages.error(request, "NOT created successfully")

	#capturing the data on terminal without validation
	#if request.method == "POST":
	#	print request.POST.get("title")
	#	print request.POST.get("body")
	#	print request.POST.get("author")
	#	print request.POST.get("categories")
	#	print request.POST.get("tags")


	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)
                         #used in urls regex
def post_detail(request, slug=None):
	#to query by param

	instance = get_object_or_404(Post, slug=slug)#change to slug=slug
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.body)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, "post_detail.html", context)
	#return HttpResponse("<h1>Detail</h1>")

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() 
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	#search listings
	query = request.GET.get("query")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(body__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()

	#to query by param
	#instance = get_object_or_404(Post, id=3)
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	page_request_var = "page" 
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	
	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}

	#to authenticate
	#if request.user.is_authenticated():
	#	context = {
			#title will route into index.html
	#		"title": "Authenticated list"
	#	}
	#else:
	#	context = {
	#		"title": "Not authenticated list" 
	#	}
	#coming from templates/index.html
	return render(request, "post_list.html", context)
	#return HttpResponse("<h1>List</h1>")


def post_update(request, slug=None):
	#user authenication
	#user authenication
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	#to query by param
	instance = get_object_or_404(Post, slug=slug)
											#allow editing
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Saved successfully")
		#success
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, slug=None):
	#user authenication
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=None)
	instance.deleted()
	messages.success(request, "Deleted successfully")
		#redirect import
	return redirect("posts:list")
	