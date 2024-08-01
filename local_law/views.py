from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LocalLaw, LocalLawField, LocalLawDates, LocalLawContacts, LocalLawNote
from .serializers import LocalLawSerializer, LocalLawFieldSerializer, LocalLawDatesSerializer, LocalLawContactsSerializer, LocalLawNoteSerializer

# LocalLaw CRUD
class LocalLawListCreate(APIView):
    def get(self, request):
        laws = LocalLaw.objects.all()
        serializer = LocalLawSerializer(laws, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocalLawSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalLawDetail(APIView):
    def get_object(self, pk):
        try:
            return LocalLaw.objects.get(pk=pk)
        except LocalLaw.DoesNotExist:
            return None

    def get(self, request, pk):
        law = self.get_object(pk)
        if law is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawSerializer(law)
        return Response(serializer.data)

    def put(self, request, pk):
        law = self.get_object(pk)
        if law is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawSerializer(law, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        law = self.get_object(pk)
        if law is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        law.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# LocalLawField CRUD
class LocalLawFieldListCreate(APIView):
    def get(self, request):
        fields = LocalLawField.objects.all()
        serializer = LocalLawFieldSerializer(fields, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocalLawFieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalLawFieldDetail(APIView):
    def get_object(self, pk):
        try:
            return LocalLawField.objects.get(pk=pk)
        except LocalLawField.DoesNotExist:
            return None

    def get(self, request, pk):
        field = self.get_object(pk)
        if field is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawFieldSerializer(field)
        return Response(serializer.data)

    def put(self, request, pk):
        field = self.get_object(pk)
        if field is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawFieldSerializer(field, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        field = self.get_object(pk)
        if field is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# LocalLawDates CRUD
class LocalLawDatesListCreate(APIView):
    def get(self, request):
        dates = LocalLawDates.objects.all()
        serializer = LocalLawDatesSerializer(dates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocalLawDatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalLawDatesDetail(APIView):
    def get_object(self, pk):
        try:
            return LocalLawDates.objects.get(pk=pk)
        except LocalLawDates.DoesNotExist:
            return None

    def get(self, request, pk):
        date = self.get_object(pk)
        if date is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawDatesSerializer(date)
        return Response(serializer.data)

    def put(self, request, pk):
        date = self.get_object(pk)
        if date is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawDatesSerializer(date, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        date = self.get_object(pk)
        if date is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        date.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# LocalLawContacts CRUD
class LocalLawContactsListCreate(APIView):
    def get(self, request):
        contacts = LocalLawContacts.objects.all()
        serializer = LocalLawContactsSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocalLawContactsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalLawContactsDetail(APIView):
    def get_object(self, pk):
        try:
            return LocalLawContacts.objects.get(pk=pk)
        except LocalLawContacts.DoesNotExist:
            return None

    def get(self, request, pk):
        contact = self.get_object(pk)
        if contact is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawContactsSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk):
        contact = self.get_object(pk)
        if contact is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawContactsSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = self.get_object(pk)
        if contact is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# LocalLawNote CRUD
class LocalLawNoteListCreate(APIView):
    def get(self, request):
        notes = LocalLawNote.objects.all()
        serializer = LocalLawNoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocalLawNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalLawNoteDetail(APIView):
    def get_object(self, pk):
        try:
            return LocalLawNote.objects.get(pk=pk)
        except LocalLawNote.DoesNotExist:
            return None

    def get(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawNoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LocalLawNoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
