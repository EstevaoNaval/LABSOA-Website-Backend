from typing import Any
from django.db.models import Func, BooleanField
from django.core.exceptions import ValidationError

class BingoSearch(Func):
    output_field = BooleanField()
    
    def __init__(self, expression, function, query, parameters, **extra):
        self.__validate_input(query, parameters)
        
        super().__init__(expression, **extra)
        
        self.extra = {
            'query': query,
            'parameters': parameters
        }
        
        self.function = function
    
    def as_sql(self, compiler, connection, **extra_context):
        placeholders = ', '.join(['%s'] * len(self.extra))
        
        sql_template = "%(expressions)s @ (%(placeholders)s)::%(function)s"
        
        sql = sql_template % {
            'expressions': self.source_expressions[0].as_sql(compiler, connection)[0],
            'placeholders': placeholders,
            'function': self.function
        }
        
        params = list(self.extra.values())
        
        return sql, params
    
    def __validate_input(self, query, parameters):
        if not isinstance(query, str) or not isinstance(parameters, str):
            raise ValidationError("Invalid input types")  

class BingoSimilaritySearch(BingoSearch):
    function = 'bingo.sim'

    def __init__(self, expression, bottom, top, query, metric, **extra):
        self.__validate_input(bottom, top, query, metric)
        
        parameters = ''
        
        super().__init__(expression, self.function, query, parameters, **extra)
        
        self.extra = {
            'bottom': bottom,
            'top': top,
            'query': query,
            'metric': metric
        }
    
    def __validate_input(self, bottom, top, query, metric):
        if not isinstance(bottom, float) or \
        not isinstance(top, float) or \
        not isinstance(query, str) or \
        not isinstance(metric, str):
            raise ValidationError("Invalid input types")
    