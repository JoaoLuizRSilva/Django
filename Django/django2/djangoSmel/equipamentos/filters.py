import django_filters

from .models import UsoEspaco

class FiltroUsoEspaco(django_filters.FilterSet):

    class Meta:
        model  = UsoEspaco
        fields = [
            'equipamentos_horario',
            'usuario',
        ]