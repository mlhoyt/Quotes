from __future__ import unicode_literals

from django.db import models
from ..models_view.models import ModelsViewMixin

import datetime

import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
dob_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')


import bcrypt

def get_pw_hash( pw, salt = bcrypt.gensalt() ):
    return( bcrypt.hashpw( pw, salt ) )


class UsersManager( models.Manager ):
    def register( self, postData ):
        errors = []

        # validate email (raw content)
        if len( postData['email'] ) < 1:
            errors.append( "The email field is empty." )
        elif not email_regex.match( postData['email'] ):
            errors.append( "Incorrectly formatted email." )
        # validate email (not in DB)
        elif len( self.filter( email = postData['email'] ) ) > 0:
            errors.append( "The email ({}) is already used.".format( postData['email'] ) )

        # validate name (raw content)
        if len( postData['name'] ) < 1:
            errors.append( "The name field is empty." )
        # elif not postData['name'].isalpha():
        #     errors.append( "The name field can only contain letters." )

        # validate alias (raw content)
        if len( postData['alias'] ) < 1:
            errors.append( "The alias field is empty." )
        # elif not postData['alias'].isalpha():
        #     errors.append( "The alias field can only contain letters." )

        # validate dob (raw content)
        if len( postData['dob'] ) < 1:
            errors.append( "The date of birth field is empty." )
        elif not dob_regex.match( postData['dob'] ):
            errors.append( "Incorrectly formatted date of birth: " + postData['dob'] )
        # validate dob (in past)
        else:
            dob_dt = datetime.datetime.strptime( postData['dob'], "%Y-%m-%d" )
            # print "Debug: login.models: dob:{} now:{}".format( dob_dt, datetime.datetime.now() )
            if dob_dt >= datetime.datetime.now():
                errors.append( "The date of birth field must be in the past" )

        # validate pw_1 (raw content)
        if len( postData['pw_1'] ) < 1:
            errors.append( "The password field is empty." )
        elif len( postData['pw_1'] ) < 8:
            errors.append( "The password field MUST be AT LEAST 8 characters!" )
        # elif not re.match( r'^.*[A-Z]+.*$', postData['pw_1'] ):
        #     errors.append( "The password field MUST contain AT LEAST 1 capital letter!" )
        # elif not re.match( r'^.*\d+.*$', postData['pw_1'] ):
        #     errors.append( "The password field MUST contain AT LEAST 1 number!" )

        # validate pw_1 against pw_2
        if postData['pw_1'] != postData['pw_2']:
            errors.append( "The password and confirm password fields MUST match!" )

        # return
        if len( errors ):
            return {
                'status': False,
                'errors': errors
            }
        else:
            return {
                'status': True,
                'user': self.create(
                    email = postData['email'],
                    name = postData['name'],
                    alias = postData['alias'],
                    dob = datetime.datetime.strptime( postData['dob'], "%Y-%m-%d" ),
                    password = get_pw_hash( postData['pw_1'].encode() ),
                )
            }

    def login( self, postData ):
        errors = []

        # validate email (raw content)
        if len( postData['email'] ) < 1:
            errors.append( "The email field is empty." )
        elif not email_regex.match( postData['email'] ):
            errors.append( "Incorrectly formatted email." )

        # validate email (in DB)
        elif len( self.filter( email = postData['email'] ) ) < 1:
            errors.append( "Unknown email." )

        # validate password (raw content)
        elif len( postData['pw'] ) < 1:
            errors.append( "The password field is empty." )

        # validate password (matches DB)
        else:
            user = self.get( email = postData['email'] )
            if get_pw_hash( postData['pw'].encode(), user.password.encode() ) != user.password:
                errors.append( "Incorrect email or password." )

        # return
        if len( errors ):
            return {
                'status': False,
                'errors': errors
            }
        else:
            return {
                'status': True,
                'user': self.get( email = postData['email'] )
            }

class Users( models.Model, ModelsViewMixin ):
    name = models.CharField( max_length = 255 )
    alias = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    password = models.CharField( max_length = 40 )
    dob = models.DateField()
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    objects = UsersManager()
