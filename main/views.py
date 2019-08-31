from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<b>At the main index.</b>")