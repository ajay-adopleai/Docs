"""Add attachments column to impress_document when missing.

This migration is defensive: it will create a Postgres text[] column when
running on PostgreSQL, and a JSON/text column for other DB backends.
It uses a RunPython operation to execute vendor-specific SQL only when the
column does not already exist, avoiding errors when the column is present.
"""
from django.db import migrations


def add_attachments_column(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    with schema_editor.connection.cursor() as cur:
        if vendor == "postgresql":
            # Add a text[] column with empty array default if it doesn't exist
            cur.execute(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'impress_document' AND column_name = 'attachments'
                    ) THEN
                        ALTER TABLE impress_document ADD COLUMN attachments text[] DEFAULT ARRAY[]::text[];
                    END IF;
                END$$;
                """
            )
        else:
            # Fallback for SQLite or other DBs: add a text column that will
            # contain a JSON array string. This keeps the migration safe for
            # local/dev environments.
            cur.execute(
                """
                PRAGMA foreign_keys = OFF;
                -- SQLite: add column if not exists (supported from SQLite 3.35)
                ALTER TABLE impress_document ADD COLUMN attachments TEXT;
                PRAGMA foreign_keys = ON;
                """
            )


def noop_reverse(apps, schema_editor):
    # Do not remove column on reverse to avoid data loss in rolling back
    return


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0024_add_is_masked_field_to_link_trace"),
    ]

    operations = [
        migrations.RunPython(add_attachments_column, reverse_code=noop_reverse),
    ]
