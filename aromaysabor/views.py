from django.shortcuts import render
from .models import CPC
from random import shuffle
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def get_distinct_values():
    neighborhoods = CPC.objects.values_list('neighborhood', flat=True).distinct().order_by('neighborhood')
    communes = CPC.objects.values_list('commune', flat=True).distinct().order_by('commune')
    categories = CPC.objects.values_list('category', flat=True).distinct().order_by('category')
    types = CPC.objects.values_list('local_type', flat=True).distinct().order_by('local_type')
    return neighborhoods, communes, categories, types

def index(request):
    objects = list(CPC.objects.all())
    shuffle(objects)
    paginator = Paginator(objects, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    neighborhoods, communes, categories, types = get_distinct_values()
    return render(request, 'public/views/index.html', {
        'objects': objects,
        'neighborhoods': neighborhoods,
        'communes': communes,
        'categories': categories,
        'types': types,
        'page_obj': page_obj,
    })

def search(request):
    neighborhoods, communes, categories, types = get_distinct_values()
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        neighborhood_filter = request.POST.getlist('neighborhood[]')
        commune_filter = request.POST.getlist('commune[]')
        category_filter = request.POST.getlist('category[]')
        type_filter = request.POST.getlist('type[]')

        query = Q(name__icontains=searched) | Q(neighborhood__icontains=searched) | Q(commune__icontains=searched) | Q(category__icontains=searched) | Q(local_type__icontains=searched) | Q(address__icontains=searched)

        if neighborhood_filter:
            query &= Q(neighborhood__in=neighborhood_filter)
        if commune_filter:
            query &= Q(commune__in=commune_filter)
        if category_filter:
            query &= Q(category__in=category_filter)
        if type_filter:
            query &= Q(local_type__in=type_filter)

        objects = CPC.objects.filter(query).distinct()

        return render(request, 'public/views/search.html', {
            'searched': searched,
            'objects': objects,
            'neighborhoods': neighborhoods,
            'communes': communes,
            'categories': categories,
            'types': types
        })
    else:
        return render(request, 'public/views/search.html', {
            'neighborhoods': neighborhoods,
            'communes': communes,
            'categories': categories,
            'types': types
        })