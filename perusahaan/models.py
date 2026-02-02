import uuid
from django.db import models
from akun.models import AkunPengguna


class Perusahaan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    akun = models.OneToOneField(
        AkunPengguna,
        on_delete=models.CASCADE
    )

    nama_perusahaan = models.CharField(
        max_length=255
    )

    deskripsi = models.TextField(
        null=True,
        blank=True
    )

    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )

    diubah_pada = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "perusahaan"

    def __str__(self):
        return self.nama_perusahaan