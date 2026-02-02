from django.urls import path
from lamaran.views import (
    AjukanLamaranAPIView,
    ProsesLamaranAPIView,
    PutuskanLamaranAPIView
)

urlpatterns = [
    path("ajukan/", AjukanLamaranAPIView.as_view(), name="ajukan-lamaran"),
    path("<uuid:lamaran_id>/proses/", ProsesLamaranAPIView.as_view()),
    path("<uuid:lamaran_id>/putusan/", PutuskanLamaranAPIView.as_view()),
]