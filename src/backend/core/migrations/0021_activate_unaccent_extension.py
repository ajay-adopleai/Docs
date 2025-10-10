from django.db import migrations


def activate_unaccent_if_postgres(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        # Use raw SQL to create extension since UnaccentExtension is Postgres-specific
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")


def drop_unaccent_if_postgres(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("DROP EXTENSION IF EXISTS unaccent;")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_remove_is_public_add_field_attachments_and_duplicated_from"),
    ]

    operations = [
        migrations.RunPython(activate_unaccent_if_postgres, reverse_code=drop_unaccent_if_postgres)
    ]
