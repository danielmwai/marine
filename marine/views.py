"""Insurity main views."""
from django.shortcuts import render


def home(request):
    """Some default page for home page."""
    try:

        return render(request, 'index.html', {'status': 200})
    except Exception, e:
        raise e
