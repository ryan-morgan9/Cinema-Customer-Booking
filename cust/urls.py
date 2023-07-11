from django.urls import path
from cust import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),

    path("selectDate/", views.selectDate, name="selectDate"),
    path("selectDate/booking/<str:selectedDate>", views.booking, name="booking"),
    path("payment/<int:adultQuantity>-<int:studentQuantity>-<int:childQuantity>-<int:selectedShowing>", views.payment, name="payment"),

    path("getPayment_Modify/", views.getPayment_Modify, name="getPayment_Modify"),
    path("modifyBooking/<int:payment_id>", views.modifyBooking, name="modifyBooking"),
    path("changeShowing/<int:selectedBooking>", views.changeShowing, name="changeShowing"),
    path("getPayment_Delete/", views.getPayment_Delete, name="getPayment_Delete"),
    path("deleteBooking/<int:payment_id>", views.deleteBooking, name="deleteBooking"),
    path("getPayment_View/", views.getPayment_View, name="getPayment_View"),
    path("viewBooking/<int:payment_id>", views.viewBooking, name="viewBooking"),
    path("viewShowing/<int:selectedBooking>", views.viewShowing, name="viewShowing"),

    path("sampleData/", views.sampleData, name="sampleData"),
]

