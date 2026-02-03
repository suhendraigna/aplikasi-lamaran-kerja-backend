from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lamaran.serializers import (
    AjukanLamaranSerializer,
    ProsesLamaranSerializer,
    PutuskanLamaranSerializer,
)
from lamaran.services import LayananLamaran
from common.exceptions import DomainException
from pelamar.models import Pelamar
from lowongan.models import Lowongan
from perusahaan.models import Perusahaan
from lamaran.models import Lamaran
from lamaran.error_codes import ErrorLamaran


class AjukanLamaranAPIView(APIView):

    def post(self, request):
        serializer = AjukanLamaranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pelamar_id = serializer.validated_data["pelamar_id"]
        lowongan_id = serializer.validated_data["lowongan_id"]

        pelamar = Pelamar.objects.get(id=pelamar_id)
        lowongan = Lowongan.objects.get(id=lowongan_id)

        layanan = LayananLamaran()

        try:
            lamaran = layanan.ajukan_lamaran(
                pelamar=pelamar,
                lowongan=lowongan
            )
        except DomainException as e:
            return Response(
                {"error":{ 
                    "kode": e.kode,
                    "pesan": e.pesan
                          }
                 },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                "id": str(lamaran.id),
                "status": lamaran.status
            },
            status=status.HTTP_201_CREATED
        )
    

class ProsesLamaranAPIView(APIView):

    def post(self, request, lamaran_id):
        serializer = ProsesLamaranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        perusahaan_id = serializer.validated_data["perusahaan_id"]

        lamaran = Lamaran.objects.get(id=lamaran_id)
        perusahaan = Perusahaan.objects.get(id=perusahaan_id)

        layanan = LayananLamaran()
        
        try:
            lamaran = layanan.proses_lamaran(
                lamaran=lamaran,
                perusahaan=perusahaan
            )
        except DomainException as e:
            return Response(
                {"error": {
                    "kode": e.kode,
                    "pesan": e.pesan
                    }
                 },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                "id": str(lamaran.id),
                "status": lamaran.status
            },
            status=status.HTTP_200_OK
        )
    
class PutuskanLamaranAPIView(APIView):

    def post(self, request, lamaran_id):
        serializer = PutuskanLamaranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        perusahaan_id = serializer.validated_data["perusahaan_id"]
        keputusan = serializer.validated_data["keputusan"]

        lamaran = Lamaran.objects.get(id=lamaran_id)
        perusahaan = Perusahaan.objects.get(id=perusahaan_id)

        layanan = LayananLamaran()

        try:
            lamaran = layanan.putuskan_lamaran(
                lamaran=lamaran,
                perusahaan=perusahaan,
                keputusan=keputusan
            )
        except DomainException as e:
            return Response(
                {"error": {
                    "kode": e.kode,
                    "pesan": e.pesan
                    }
                 },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                "id" : str(lamaran.id),
                "status": lamaran.status
            },
            status=status.HTTP_200_OK
        )
