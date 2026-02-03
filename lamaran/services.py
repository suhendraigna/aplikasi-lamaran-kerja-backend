from common.exceptions import DomainException
from lamaran.models import Lamaran
from lamaran.constants import StatusLamaran
from lamaran.error_codes import ErrorLamaran


class LayananLamaran:
    """
    Service untuk menangani logika domain terkait lamaran.
    """

    def ajukan_lamaran(self, pelamar, lowongan):
        """
        Pelamar mengajukan lamaran ke lowongan tertentu.
        """

        #1. Validasi lowongan aktif
        if not lowongan.aktif:
            raise DomainException(
                    ErrorLamaran.LOWONGAN_TUTUP,
                    "Lowongan sudah ditutup."
                                  )
        

        #2. Validasi belum pernah melamar
        sudah_ada = Lamaran.objects.filter(
            pelamar=pelamar,
            lowongan=lowongan
        ).exists()

        if sudah_ada:
            raise DomainException(
                    ErrorLamaran.DUPLIKAT_LAMARAN,
                    "Pelamar sudah pernah melamar lowongan ini."
                    )
        
        
        #3. Buat lamaran baru
        lamaran = Lamaran.objects.create(
            pelamar=pelamar,
            lowongan=lowongan,
            status=StatusLamaran.DIKIRIM
        )

        return lamaran
    

    def proses_lamaran(self, lamaran, perusahaan):
        if lamaran.lowongan.perusahaan != perusahaan:
            raise DomainException(
                    ErrorLamaran.TIDAK_BERHAK,
                    "Perusahaan tidak berhak memproses lamaran ini."
                    )
        
        if lamaran.status != StatusLamaran.DIKIRIM:
            raise DomainException(
                    ErrorLamaran.STATUS_TIDAK_VALID,
                    "Lamaran tidak bisa diproses."
                    )
        
        lamaran.status = StatusLamaran.DIPROSES
        lamaran.save()
        return lamaran
    
    def putuskan_lamaran(self, lamaran, perusahaan, keputusan):
        if lamaran.lowongan.perusahaan != perusahaan:
            raise DomainException(
                    ErrorLamaran.TIDAK_BERHAK,
                    "Perusahaan tidak berhak memproses lamaran ini."
                    )
        
        if lamaran.status != StatusLamaran.DIPROSES:
            raise DomainException(
                    ErrorLamaran.STATUS_TIDAK_VALID,
                    "Lamaran belum diproses."
                    )
        
        if keputusan not in ["DITERIMA", "DITOLAK"]:
            raise DomainException(
                    ErrorLamaran.KEPUTUSAN_TIDAK_VALID,
                    "Keputusan lamaran tidak valid."
                    )
        
        lamaran.status = keputusan
        lamaran.save()
        return lamaran
