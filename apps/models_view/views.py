from django.shortcuts import render

# from ..{{OTHER_APP}}.models import {{MODEL}}

def index( request ):
    context = {
        'models': {
            # '{{MODEL}}': {{MODEL}}.objects.all(),
        }
    }
    return render( request, "models_view/index.html", context )
