from django.shortcuts import render
from members.models import Member

# Create your views here.

def home(request):
    context = {}
    context['persons'] = Member.objects.all() # TODO: not all!
    context['abc'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    return render(request, 'browse.html', context)