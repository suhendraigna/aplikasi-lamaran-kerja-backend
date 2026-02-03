import uuid
from django.db import models
from pelamar.models import Pelamar
from lowongan.models import Lowongan
from lamaran.constants import StatusLamaran


class Lamaran(models.Model):
    id =  models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    pelamar = models.ForeignKey(
        Pelamar,
        on_delete=models.CASCADE
    )

    lowongan = models.ForeignKey(
        Lowongan,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=StatusLamaran.PILIHAN
    )

    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )

    diubah_pada = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "lamaran"
        constraints = [
            models.UniqueConstraint(
                fields=["pelamar", "lowongan"],
                name="unik_pelamar_lowongan"
            )
        ]
    
    def __str__(self):
        return f"{self.pelamar} - {self.lowongan}"
