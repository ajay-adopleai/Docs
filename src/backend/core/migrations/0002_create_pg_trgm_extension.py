from django.db import migrations


def create_trgm_if_postgres(apps, schema_editor):
    # Only run pg_trgm extension creation on PostgreSQL
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def drop_trgm_if_postgres(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute("DROP EXTENSION IF EXISTS pg_trgm;")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_trgm_if_postgres, reverse_code=drop_trgm_if_postgres),
    ]
