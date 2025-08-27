from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Contact
from .serializers import ContactSerializer


@api_view(["GET"])
def health(request):
    """
    Simple health check endpoint.
    """
    return Response({"message": "Server is up!"}, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
@api_view(["GET", "POST"])
def contacts_collection(request):
    """
    Returns list of contacts or creates a new contact.

    Methods:
    - GET /api/contacts: Returns JSON array of contacts with HTTP 200.
    - POST /api/contacts: Creates a contact with provided JSON body and returns
      the created contact with HTTP 201, or validation errors with HTTP 400.

    Request Body (POST):
    {
      "name": "string",
      "phone": "string",
      "email": "user@example.com"
    }

    Responses:
    - 200: [{"id": 1, "name": "...", "phone": "...", "email": "..."}]
    - 201: {"id": 1, "name": "...", "phone": "...", "email": "..."}
    - 400: {"error": "ValidationError", "details": {"field": ["msg", ...], ...}}
    - 500: {"error": "ServerError", "details": "message"}
    """
    try:
        if request.method == "GET":
            contacts = Contact.objects.all().order_by("id")
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "POST":
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                contact = serializer.save()
                return Response(ContactSerializer(contact).data, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "ValidationError", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Should not reach here due to @api_view restriction
        return Response({"error": "MethodNotAllowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as exc:
        return Response(
            {"error": "ServerError", "details": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# PUBLIC_INTERFACE
@api_view(["PUT", "DELETE"])
def contact_detail(request, contact_id: int):
    """
    Updates or deletes a single contact by ID.

    Methods:
    - PUT /api/contacts/{id}: Updates an existing contact with JSON body.
      Returns updated contact with HTTP 200, or errors with HTTP 400/404.
    - DELETE /api/contacts/{id}: Deletes the contact.
      Returns {"message": "Deleted"} with HTTP 204 (no content body per spec, but we return JSON 200/204?).
      We'll return 204 with no body to keep minimal; JSON body when 200 not required.

    Request Body (PUT):
    {
      "name": "string",
      "phone": "string",
      "email": "user@example.com"
    }

    Responses:
    - 200: {"id": 1, "name": "...", "phone": "...", "email": "..."}
    - 204: No content (on successful delete)
    - 400: {"error": "ValidationError", "details": {...}}
    - 404: {"error": "NotFound", "details": "Contact not found"}
    - 500: {"error": "ServerError", "details": "message"}
    """
    try:
        try:
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            return Response(
                {"error": "NotFound", "details": "Contact not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "PUT":
            serializer = ContactSerializer(contact, data=request.data, partial=False)
            if serializer.is_valid():
                updated = serializer.save()
                return Response(ContactSerializer(updated).data, status=status.HTTP_200_OK)
            return Response(
                {"error": "ValidationError", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == "DELETE":
            contact.delete()
            # 204 No Content should not include a response body
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "MethodNotAllowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as exc:
        return Response(
            {"error": "ServerError", "details": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
