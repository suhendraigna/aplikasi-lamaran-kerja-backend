import uuid
from django.test import TestCase
from rest_framework.test import APIClient

from akun.models import AkunPengguna
from pelamar.models import Pelamar
from perusahaan.models import Perusahaan
from lowongan.models import Lowongan
from lamaran.models import Lamaran
from lamaran.services import LayananLamaran
from lamaran.constants import StatusLamaran
from common.exceptions import DomainException



class LayananLamaranTest(TestCase):

    def setUp(self):
        # Akun pelamar
        self.akun_pelamar = AkunPengguna.objects.create(
            email="pelamar@test.com",
            kata_sandi="password",
            peran="PELAMAR"
        )

        self.pelamar = Pelamar.objects.create(
            akun=self.akun_pelamar,
            nama_lengkap="Hen"
        )

        # Akun perusahaan
        self.akun_perusahaan = AkunPengguna.objects.create(
            email="perusahaan@test.com",
            kata_sandi="password",
            peran="PERUSAHAAN"
        )

        self.perusahaan = Perusahaan.objects.create(
            akun=self.akun_perusahaan,
            nama_perusahaan="PT Maju Jaya"
        )

        self.lowongan = Lowongan.objects.create(
            perusahaan=self.perusahaan,
            judul="Backend Developer",
            deskripsi="Mencari backend engineer",
            aktif=True
        )

        self.layanan = LayananLamaran()

    
    def test_pelamar_berhasil_melamar_lowongan(self):
        lamaran = self.layanan.ajukan_lamaran(
            pelamar=self.pelamar,
            lowongan=self.lowongan
        )

        self.assertIsInstance(lamaran, Lamaran)
        self.assertEqual(lamaran.status, StatusLamaran.DIKIRIM)


    def test_gagal_melamar_jika_lowongan_tidak_aktif(self):
        self.lowongan.aktif = False
        self.lowongan.save()

        with self.assertRaises(DomainException) as konteks:
            self.layanan.ajukan_lamaran(
                pelamar=self.pelamar,
                lowongan=self.lowongan
            )

        self.assertEqual(
            str(konteks.exception),
            "Lowongan sudah ditutup."
        )

    def test_gagal_melamar_jika_sudah_pernah_melamar(self):
        Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DIKIRIM
        )

        with self.assertRaises(DomainException) as konteks:
            self.layanan.ajukan_lamaran(
                pelamar=self.pelamar,
                lowongan=self.lowongan
            )
        
        self.assertEqual(
            str(konteks.exception),
            "Pelamar sudah pernah melamar lowongan ini."
        )

    def test_perusahaan_bisa_memproses_lamaran(self):
        lamaran = Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DIKIRIM
        )

        hasil = self.layanan.proses_lamaran(
            lamaran=lamaran,
            perusahaan=self.perusahaan
        )

        self.assertEqual(hasil.status, StatusLamaran.DIPROSES)

    def test_lamaran_tidak_bisa_diproses_jika_status_salah(self):
        lamaran = Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DITERIMA
        )

        with self.assertRaises(DomainException):
            self.layanan.proses_lamaran(
                lamaran=lamaran,
                perusahaan=self.perusahaan
            )

    def test_perusahaan_bisa_menerima_lamaran(self):
        lamaran = Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DIPROSES
        )

        hasil = self.layanan.putuskan_lamaran(
            lamaran=lamaran,
            perusahaan=self.perusahaan,
            keputusan=StatusLamaran.DITERIMA
        )

        self.assertEqual(hasil.status, StatusLamaran.DITERIMA)

class AjukanLamaranAPITest(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        # Akun & pelamar
        self.akun_pelamar = AkunPengguna.objects.create(
            email="pelamar@test.com",
            kata_sandi="password",
            peran="PELAMAR"
        )

        self.pelamar = Pelamar.objects.create(
            akun=self.akun_pelamar,
            nama_lengkap="Hen"
        )

        # Akun & perusahaan
        self.akun_perusahaan = AkunPengguna.objects.create(
            email="perusahaan@test.com",
            kata_sandi="password",
            peran="PERUSAHAAN"
        )

        self.perusahaan = Perusahaan.objects.create(
            akun=self.akun_perusahaan,
            nama_perusahaan="PT Maju Jaya"
        )

        self.lowongan = Lowongan.objects.create(
            perusahaan = self.perusahaan,
            judul="Backend Developer",
            deskripsi="Mencari backend engineer",
            aktif=True
        )

        self.url = "/api/lamaran/ajukan/"


    def test_api_ajukan_lamaran_berhasil(self):
        response = self.client.post(
            self.url,
            data={
                "pelamar_id": str(self.pelamar.id),
                "lowongan_id": str(self.lowongan.id)
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["status"], StatusLamaran.DIKIRIM)
        self.assertEqual(Lamaran.objects.count(), 1)

    def test_api_gagal_jika_lowongan_tidak_aktif(self):
        self.lowongan.aktif = False
        self.lowongan.save()

        response = self.client.post(
            self.url,
            data={
                "pelamar_id": str(self.pelamar.id),
                "lowongan_id": str(self.lowongan.id)
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"],
            "Lowongan sudah ditutup."
        )

        self.assertEqual(Lamaran.objects.count(), 0)

    def test_api_gagal_jika_pelamar_sudah_pernah_melamar(self):
        Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DIKIRIM
        )

        response = self.client.post(
            self.url,
            data={
                "pelamar_id": str(self.pelamar.id),
                "lowongan_id": str(self.lowongan.id)
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"],
            "Pelamar sudah pernah melamar lowongan ini."
        )
        self.assertEqual(Lamaran.objects.count(), 1)


    def test_api_gagal_jika_payload_tidak_lengkap(self):
        response = self.client.post(
            self.url,
            data={
                "pelamar_id": str(self.pelamar.id)
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)


    def test_api_perusahaan_memproses_lamaran(self):
        lamaran = Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DIKIRIM
        )

        response = self.client.post(
            f"/api/lamaran/{lamaran.id}/proses/",
            data={
                "perusahaan_id": str(self.perusahaan.id)
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], StatusLamaran.DIPROSES)

    def test_api_perusahaan_menerima_lamaran(self):
        lamaran = Lamaran.objects.create(
            pelamar=self.pelamar,
            lowongan=self.lowongan,
            status=StatusLamaran.DIPROSES
        )

        response = self.client.post(
            f"/api/lamaran/{lamaran.id}/putusan/",
            data={
                "perusahaan_id": str(self.perusahaan.id),
                "keputusan": StatusLamaran.DITERIMA
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], StatusLamaran.DITERIMA)

