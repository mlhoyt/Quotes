from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from .models import Quote
from ..login.models import Users

def index( request ):
    if 'login_id' in request.session:
        context = {
            'non_fav_quotes': Quote.objects.exclude( favored_by__id = request.session['login_id'] ).order_by ( '-created_at' ),
            'fav_quotes': Quote.objects.filter( favored_by__id = request.session['login_id'] ),
        }
        return render( request, "quotes/index.html", context )
    else:
        return redirect( reverse( 'login:index' ) )

def add_quote( request ):
    if 'login_id' in request.session:
        if request.method == "POST":
            db_result = Quote.objects.add_quote( int( request.session['login_id'] ), request.POST )

            if not db_result['status']:
                messages.add_message( request, messages.INFO, "Unable to add quote!" )
                for i in db_result['errors']:
                    messages.add_message( request, messages.INFO, "- " + i )

    return redirect( reverse( "quotes:index" ) )

def add_favorite( request, u_id, q_id ):
    if 'login_id' in request.session:
        Quote.objects.add_favored_by( int( u_id ), int( q_id ) )

    return redirect( reverse( "quotes:index" ) )

def remove_favorite( request, u_id, q_id ):
    if 'login_id' in request.session:
        Quote.objects.remove_favored_by( int( u_id ), int( q_id ) )

    return redirect( reverse( "quotes:index" ) )

def view_user( request, id ):
    if 'login_id' in request.session:
        context = {
            'user': Users.objects.get( id = int( id ) ),
        }
        return render( request, "quotes/view_user.html", context )

    return redirect( reverse( "quotes:index" ) )

def catcher( request ):
    return redirect( reverse( "quotes:index" ) )
