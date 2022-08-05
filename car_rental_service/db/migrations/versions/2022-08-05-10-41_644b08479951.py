"""empty message

Revision ID: 644b08479951
Revises: ca446aa5716c
Create Date: 2022-08-05 10:41:39.300364

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "644b08479951"
down_revision = "ca446aa5716c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Seed data into car availability zones table
    op.execute(
        """
        INSERT INTO "public"."car_availability_zones" ("id", "uuid", "created_at", "updated_at", "is_active", "name") VALUES
        (1, '10f10b20-6a74-49f4-b61a-e469f16c3b48', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone A'),
        (2, 'dc8437ee-f466-457c-9374-5f39cbe51701', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone B'),
        (3, '580e5b94-aaac-49ea-bf99-d889e08cb319', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone C'),
        (4, '504a3f31-6f2c-4755-ab61-db7ebe05b1c0', '2022-08-04 22:33:50.886581', '2022-08-04 22:33:50.886581', 't', 'Zone D');
        """,
    )
    # Seed data into categories table
    op.execute(
        """
        INSERT INTO "public"."categories" ("id", "uuid", "created_at", "updated_at", "is_active", "name") VALUES
        (1, 'a341c07d-706b-44a2-bcbf-cee47749e7d2', '2022-08-04 22:34:59.317978', '2022-08-04 22:34:59.317978', 't', 'Sedan'),
        (2, 'cb877048-9fd1-457a-b7ce-cac8c94eb6f4', '2022-08-04 22:34:59.317978', '2022-08-04 22:34:59.317978', 't', 'SUV'),
        (3, 'eb7ff701-1677-4cfc-98a1-aec10ff9370e', '2022-08-04 22:34:59.317978', '2022-08-04 22:34:59.317978', 't', 'Hatchback');
        """,
    )
    # Seed data into cars table
    op.execute(
        """
        INSERT INTO "public"."cars" ("id", "uuid", "created_at", "updated_at", "is_active", "name", "brand", "registered_number", "category_id") VALUES
        (1, '754bb404-90a9-423c-b512-513f25374eb0', '2022-08-04 22:36:55.150335', '2022-08-04 22:36:55.150335', 't', 'Car A', 'Brand A', 'HR26AZ1234', 1),
        (2, '5bf40d50-d32b-4019-806b-8ec4b83c6764', '2022-08-04 22:36:55.150335', '2022-08-04 22:36:55.150335', 't', 'Car B', 'Brand B', 'HR26AZ5678', 2),
        (3, '9d0aa319-8bbe-4ac7-955b-9271d15480b0', '2022-08-04 22:36:55.150335', '2022-08-04 22:36:55.150335', 't', 'Car C', 'Brand C', 'HR26AZ7891', 3);
        """,
    )
    # Seed data into users table
    op.execute(
        """
        INSERT INTO "public"."users" ("id", "uuid", "created_at", "updated_at", "is_active", "name", "email", "mobile") VALUES
        (1, 'a12be027-484c-42e0-a972-c3d0069d4a5d', '2022-08-05 03:04:17.427032', '2022-08-05 03:04:17.427032', 't', 'Saurabh Sharma', 'saurabhpysharma@gmail.com', '9654198036'),
        (2, '3d6ca315-5a0e-4a6d-b791-46eef1fca882', '2022-08-05 03:04:17.427032', '2022-08-05 03:04:17.427032', 't', 'Sammy', 'sammy@gmail.com', '9999999999'),
        (3, '372a7b8e-390c-4061-b8cc-4186c2da32ed', '2022-08-05 03:04:17.427032', '2022-08-05 03:04:17.427032', 't', 'John', 'john@gmail.com', '9999999991');
        """,
    )
    # Seed data into reservations table
    op.execute(
        """
        INSERT INTO "public"."reservations" ("id", "uuid", "created_at", "updated_at", "is_active", "car_id", "start_date", "end_date", "status", "user_id") VALUES
        (23, 'fcf85714-a228-4a0c-b128-cc0adcb1b43e', '2022-08-05 00:41:42.46016', '2022-08-05 00:41:42.46016', 't', 1, '2022-08-04', '2022-08-04', 'SUCCESS', 1),
        (24, 'fd5c5ee5-ddc5-422a-8bcf-7b131bca5f78', '2022-08-05 01:17:53.427526', '2022-08-05 01:17:53.427526', 't', 1, '2022-08-05', '2022-08-05', 'SUCCESS', 2);
        """,
    )


def downgrade() -> None:
    op.execute("""TRUNCATE reservations;""")
    op.execute("""TRUNCATE users;""")
    op.execute("""TRUNCATE cars;""")
    op.execute("""TRUNCATE categories;""")
    op.execute("""TRUNCATE car_availability_zones;""")
