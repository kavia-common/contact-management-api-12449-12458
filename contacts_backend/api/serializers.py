from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model. Handles validation and (de)serialization.
    """

    class Meta:
        model = Contact
        fields = ["id", "name", "phone", "email"]

    def validate_name(self, value: str):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def validate_phone(self, value: str):
        if not value or not value.strip():
            raise serializers.ValidationError("Phone is required.")
        return value.strip()

    def validate_email(self, value: str):
        # EmailField already does format validation; ensure non-empty
        if not value or not str(value).strip():
            raise serializers.ValidationError("Email is required.")
        return value
