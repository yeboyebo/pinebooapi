"""
    Utilizamos el model para definir los custom lookup al ser esta aplicacion una libreria general
"""
from django.db.models import Lookup
from django.db.models.fields import Field


class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


class BaseContainsLookup(Lookup):

    def get_param_formatter(self):
        return "%{}%"

    def get_sql_opp(self):
        return "NOT LIKE"

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        params[0] = self.get_param_formatter().format(params[0])
        return '%s {} %s'.format(self.get_sql_opp()) % (lhs, rhs), params


class NotContains(BaseContainsLookup):
    lookup_name = 'ncontains'


class NotIContains(NotContains):
    lookup_name = 'nicontains'

    def get_sql_opp(self):
        return "NOT ILIKE"


class NotStartsWith(BaseContainsLookup):
    lookup_name = 'nstartswith'

    def get_param_formatter(self):
        return "{}%"


class NotIStartsWith(NotStartsWith):
    lookup_name = 'nistartswith'

    def get_sql_opp(self):
        return "NOT ILIKE"


class NotEndsWith(BaseContainsLookup):
    lookup_name = 'nendswith'

    def get_param_formatter(self):
        return "%{}"


class NotIEndsWith(NotEndsWith):
    lookup_name = 'niendswith'

    def get_sql_opp(self):
        return "NOT ILIKE"


class NotIn(Lookup):
    lookup_name = 'nin'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        params[0] = params[0][1:-1]
        # Era necesario el ["notinnotinnotin"]
        return '%s NOT IN (%s, {})'.format(",".join(params)) % (lhs, rhs), ["notinnotinnotin"]


Field.register_lookup(NotEqual)
Field.register_lookup(NotStartsWith)
Field.register_lookup(NotIStartsWith)
Field.register_lookup(NotEndsWith)
Field.register_lookup(NotIEndsWith)
Field.register_lookup(NotContains)
Field.register_lookup(NotIContains)
Field.register_lookup(NotIn)
