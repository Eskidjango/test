from urllib import quote_plus # for
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import  HttpResponseRedirect, Http404

from .forms import PostForm
from .models import Post


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    print request.FILES, request.POST    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'form_button_value': 'Create',
    }
    return render(request, 'post_create.html', context)

def post_update(request, slug=None): # retrieve/read
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    template = 'post_create.html'
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Successfully Changed", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
        'form_button_value': 'Change'
    }
    return render(request, template, context)

def post_list(request): # list items
    queryset_list = Post.objects.all().order_by('-timestamp')
    template = 'post_list.html'
    paginator = Paginator(queryset_list, 2) # Show 25 posts per page
    page_number_variable = 'page'
    page = request.GET.get(page_number_variable)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'object_list': queryset,
        'title': 'List',
        'page_number_variable':page_number_variable,
    }
    return render(request, template, context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    template = 'detail.html'  
    share_string = quote_plus(instance.content) # changing how content looks like in the brower's line  
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
    }
    return render(request, template, context)


def post_delete(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('posts:main_page')

