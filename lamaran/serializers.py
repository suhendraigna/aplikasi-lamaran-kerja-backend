from rest_framework import serializers



class AjukanLamaranSerializer(serializers.Serializer):
    pelamar_id = serializers.UUIDField()
    lowongan_id = serializers.UUIDField()


class ProsesLamaranSerializer(serializers.Serializer):
    perusahaan_id = serializers.UUIDField()


class PutuskanLamaranSerializer(serializers.Serializer):
    perusahaan_id = serializers.UUIDField()
    keputusan = serializers.ChoiceField(
        choices=["DITERIMA", "DITOLAK"]
    )