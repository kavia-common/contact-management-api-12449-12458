from django.urls import path
from .views import health, contacts_collection, contact_detail

urlpatterns = [
    path("health/", health, name="Health"),
    path("contacts", contacts_collection, name="contacts_collection"),  # matches /api/contacts
    path("contacts/<int:contact_id>", contact_detail, name="contact_detail"),  # matches /api/contacts/{id}
]
