from import_export import resources, fields

from utils.translations import get_field_verbose_name

from .models import Journal


class JournalResource(resources.ModelResource):
    key = fields.Field(
        column_name=get_field_verbose_name(Journal, 'key'),
        attribute='key',
    )
    membership = fields.Field(
        column_name=get_field_verbose_name(Journal, 'membership'),
        attribute='membership',
    )
    membership_type = fields.Field(
        column_name=get_field_verbose_name(Journal, 'membership_type'),
        attribute='membership_type',
    )
    trainer = fields.Field(
        column_name=get_field_verbose_name(Journal, 'trainer'),
        attribute='trainer',
    )
    entry_time = fields.Field(
        column_name=get_field_verbose_name(Journal, 'entry_time'),
        attribute='entry_time',
    )
    exit_time = fields.Field(
        column_name=get_field_verbose_name(Journal, 'exit_time'),
        attribute='exit_time',
    )
    actual_exit_time = fields.Field(
        column_name=get_field_verbose_name(Journal, 'actual_exit_time'),
        attribute='actual_exit_time',
    )
    create_date = fields.Field(
        column_name=get_field_verbose_name(Journal, 'create_date'),
        attribute='create_date',
    )

    class Meta:
        model = Journal
        fields = (
            'id',
            'key',
            'membership',
            'membership_type',
            'trainer',
            'entry_time',
            'exit_time',
            'actual_exit_time',
            'create_date',
        )
