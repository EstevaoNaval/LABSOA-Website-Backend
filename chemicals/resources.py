from import_export_extensions.resources import CeleryModelResource
from import_export_extensions.fields import Field
from import_export_extensions.widgets import ManyToManyWidget
from django.db.models.fields import reverse_related
from django.db.models.fields import related

from .models import Chemical
from .filters import ChemicalAdvancedSearchFilter

class ChemicalResource(CeleryModelResource):
    filterset_class = ChemicalAdvancedSearchFilter
    
    def __init__(self, filter_kwargs = None, **kwargs):
        super().__init__(filter_kwargs, **kwargs)
        self._add_reverse_related_fields()
        self._add_many_to_many_fields()

    def _add_many_to_many_fields(self):
        model = self.Meta.model

        # Itera sobre todos os campos do modelo
        for field in model._meta.get_fields():
            # Identifica relações reversas (ManyToOneRel ou ManyToManyRel)
            if isinstance(field, (related.ManyToManyField)):
                # Itera pelos campos do modelo relacionado
                for related_field in field.related_model._meta.get_fields():
                    if not related_field.is_relation and related_field.name not in ['id', 'created_at','update_at', 'api_id']:
                        field_name = f"{field.name}__{related_field.name}"
                        self.fields[field_name] = Field(
                            attribute=field.name,
                            column_name=related_field.name,
                            widget=ManyToManyWidget(
                                model=field.related_model,
                                field=related_field.name,
                                separator=';'
                            )
                        )

    def _add_reverse_related_fields(self):
        model = self.Meta.model

        # Itera sobre todos os campos do modelo
        for field in model._meta.get_fields():
            # Identifica relações reversas (ManyToOneRel ou ManyToManyRel)
            if isinstance(field, (reverse_related.OneToOneRel)):
                related_model = field.related_model
                related_name = field.related_name or field.name

                # Itera pelos campos do modelo relacionado
                for related_field in related_model._meta.get_fields():
                    if not related_field.is_relation and related_field.name not in ['id', 'created_at','update_at', 'slug', 'api_id']:
                        field_name = f"{related_name}__{related_field.name}"
                        self.fields[field_name] = Field(
                            attribute=field_name,
                            column_name=related_field.name
                        )

    class Meta:
        model = Chemical
        fields = ('api_id', 'created_at', 'update_at',)