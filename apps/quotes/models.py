from __future__ import unicode_literals

from django.db import models
# from django.db.models import Count
from ..models_view.models import ModelsViewMixin
from ..login.models import Users

class QuoteManager( models.Manager ):
    def add_quote( self, u_id, postData ):
        errors = []

        # validate quoted_by
        if len( postData['quoted_by'] ) < 3:
            errors.append( "The Quoted By field is too short (at least 3 characters).")

        # validate content
        if len( postData['content'] ) < 10:
            errors.append( "The Message field is too short (at least 10 characters).")

        # return
        if len( errors ):
            return {
                'status': False,
                'errors': errors
            }
        else:
            return {
                'status': True,
                'quote': self.create(
                    author = postData['quoted_by'],
                    content = postData['content'],
                    posted_by = Users.objects.get( id = u_id ),
                )
            }

    def add_favored_by( self, u_id, q_id ):
        # Should verify that u_id has not already favored q_id
        self.get( id = q_id ).favored_by.add( Users.objects.get( id = u_id ) )

    def remove_favored_by( self, u_id, q_id ):
        # Should verify that u_id has not already favored q_id
        self.get( id = q_id ).favored_by.remove( Users.objects.get( id = u_id ) )

class Quote( models.Model, ModelsViewMixin ):
    author = models.CharField( max_length = 255 )
    content = models.TextField()
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    posted_by = models.ForeignKey( Users, related_name = "posted_quotes" )
    favored_by = models.ManyToManyField( Users, related_name = "favorite_quotes" )

    objects = QuoteManager()
