from __future__ import unicode_literals

from django.db import models

class ModelsViewMixin( object ):
    def toHTMLTableTHeadRow( self ):
        rv = []
        rv.append( '<tr>' )
        for field in self._meta.get_fields():
            rv.append( '<th>{}</th>'.format( field.name ) )
        rv.append( '</tr>' )
        return "\n".join( rv )

    def toHTMLTableTBodyRow( self ):
        rv = []
        rv.append( '<tr>' )
        for field in self._meta.get_fields():
            rv.append( '<td>{}</td>'.format( getattr( self, field.name ) ) )
        rv.append( '</tr>' )
        return "\n".join( rv )
