import uuid
from django.db import models
from perusahaan.models import Perusahaan



class Lowongan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    perusahaan = models.ForeignKey(
        Perusahaan,
        on_delete=models.CASCADE
    )

    judul = models.CharField(
        max_length=255
    )

    deskripsi = models.TextField()

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
        db_table = "lowongan"

    def __str__(self):
        return self.judul