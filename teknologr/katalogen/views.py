from django.shortcuts import render, get_object_or_404
from members.models import Member
from django.db.models import Q
from functools import reduce
from operator import and_


def _get_base_context():
    return {'abc': "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ" }


def home(request):
    context = _get_base_context()
    context['persons'] = Member.objects.all() # TODO: not all!
    return render(request, 'browse.html', context)


def search(request):
    context = _get_base_context()
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


def profile(request, member_id):
    context = _get_base_context()
    # TODO: implement
    context['person'] = get_object_or_404(Member, id=member_id)
    return render(request, 'profile.html', context)


def startswith(request, letter):
    context = _get_base_context()
    context['persons'] = Member.objects.filter(surname__istartswith=letter) # TODO: not all members!
    return render(request, 'browse.html', context)