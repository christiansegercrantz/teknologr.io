from django.shortcuts import render
from members.models import Member
from django.db.models import Q
from functools import reduce
from operator import and_


# Create your views here.

def home(request):
    context = {}
    context['abc'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    context['persons'] = Member.objects.all() # TODO: not all!
    return render(request, 'browse.html', context)

def search(request):
    context = {}
    context['abc'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    query = request.GET.get('q')
    query_list = query.split()
    result = Member.objects.all() # TODO: not all!
    if not query_list:
        context['persons'] = []
    else:
        context['persons'] = result.filter(
           reduce(and_, (Q(given_names__icontains=q) | Q(surname__icontains=q) for q in query_list))
        )

    return render(request, 'browse.html', context)

def profile(request):
    # TODO: implement
    context = {}
    context['abc'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    context['persons'] = Member.objects.all() # TODO: not all!
    return render(request, 'browse.html', context)

