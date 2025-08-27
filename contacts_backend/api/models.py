from django.db import models


class Contact(models.Model):
    """
    Contact model representing a simple contact record.

    Fields:
    - name: The full name of the contact.
    - phone: The phone number of the contact.
    - email: The email address of the contact.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=False)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
