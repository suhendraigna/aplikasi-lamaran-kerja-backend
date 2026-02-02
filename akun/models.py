import uuid
from django.db import models



class AkunPengguna(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(
        unique=True
    )

    kata_sandi = models.CharField(
        max_length=255
    )

    peran = models.CharField(
        max_length=20
    )

    aktif = models.BooleanField(
        default=True
    )

    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )

    diubah_pada = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "akun_pengguna"

    def __str__(self):
        return self.email

