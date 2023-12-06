from django.shortcuts import render
from . import settings
import os
from django.http import HttpResponse


def page_not_found_view(request, exception):
    return render(request, 'templates/404.html', status=404)


def read_robots(base_dir):
    robots_file = base_dir + '/robots.txt'
    if os.path.isfile(robots_file):
        file = open(robots_file, 'r')
        data = file.read()
        file.close()
        return data
    return ""


def robots(request):
    robots_file = read_robots(str(settings.BASE_DIR))
    context = robots_file
    return HttpResponse(context, content_type='text/plain')
