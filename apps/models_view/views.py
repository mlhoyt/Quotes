from django.shortcuts import render

from ..login.models import Users
from ..quotes.models import Quote

def index( request ):
    context = {
        'models': {
            'Users': Users.objects.all(),
            'Quote': Quote.objects.all(),
        }
    }
    return render( request, "models_view/index.html", context )
