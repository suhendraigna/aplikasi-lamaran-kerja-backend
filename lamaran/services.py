from common.exceptions import DomainException
from lamaran.models import Lamaran



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
            raise DomainException("Lowongan sudah ditutup.")
        

        #2. Validasi belum pernah melamar
        sudah_ada = Lamaran.objects.filter(
            pelamar=pelamar,
            lowongan=lowongan
        ).exists()

        if sudah_ada:
            raise DomainException("Pelamar sudah pernah melamar lowongan ini.")
        
        
        #3. Buat lamaran baru
        lamaran = Lamaran.objects.create(
            pelamar=pelamar,
            lowongan=lowongan,
            status="DIKIRIM"
        )

        return lamaran
    

    def proses_lamaran(self, lamaran, perusahaan):
        if lamaran.lowongan.perusahaan != perusahaan:
            raise DomainException("Perusahaan tidak berhak memproses lamaran ini.")
        
        if lamaran.status != "DIKIRIM":
            raise DomainException("Lamaran tidak bisa diproses.")
        
        lamaran.status = "DIPROSES"
        lamaran.save()
        return lamaran
    
    def putuskan_lamaran(self, lamaran, perusahaan, keputusan):
        if lamaran.lowongan.perusahaan != perusahaan:
            raise DomainException("Perusahaan tidak berhak memproses lamaran ini.")
        
        if lamaran.status != "DIPROSES":
            raise DomainException("Lamaran belum diproses.")
        
        if keputusan not in ["DITERIMA", "DITOLAK"]:
            raise DomainException("Keputusan lamaran tidak valid.")
        
        lamaran.status = keputusan
        lamaran.save()
        return lamaran