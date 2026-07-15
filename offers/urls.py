from django.urls import path

from .views import *

urlpatterns = [

    path(
        "create/",
        OfferLetterCreateView.as_view()
    ),

    path(
        "",
        OfferLetterListView.as_view()
    ),

    path(
        "my-offers/",
        MyOfferLettersView.as_view()
    ),

    path(
        "accept/<int:pk>/",
        AcceptOfferView.as_view()
    ),

    path(
        "decline/<int:pk>/",
        DeclineOfferView.as_view()
    ),

]