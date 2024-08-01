from django.urls import path
from .views import LocalLawListCreate, LocalLawDetail, LocalLawFieldListCreate, LocalLawFieldDetail, LocalLawDatesListCreate, LocalLawDatesDetail, LocalLawContactsListCreate, LocalLawContactsDetail, LocalLawNoteListCreate, LocalLawNoteDetail

urlpatterns = [
    path('', LocalLawListCreate.as_view(), name='local_law-list-create'),
    path('<int:pk>/', LocalLawDetail.as_view(), name='local_law-detail'),
    path('local_law_fields/', LocalLawFieldListCreate.as_view(), name='local_law_field-list-create'),
    path('local_law_fields/<int:pk>/', LocalLawFieldDetail.as_view(), name='local_law_field-detail'),
    path('local_law_dates/', LocalLawDatesListCreate.as_view(), name='local_law_dates-list-create'),
    path('local_law_dates/<int:pk>/', LocalLawDatesDetail.as_view(), name='local_law_dates-detail'),
    path('local_law_contacts/', LocalLawContactsListCreate.as_view(), name='local_law_contacts-list-create'),
    path('local_law_contacts/<int:pk>/', LocalLawContactsDetail.as_view(), name='local_law_contacts-detail'),
    path('local_law_notes/', LocalLawNoteListCreate.as_view(), name='local_law_note-list-create'),
    path('local_law_notes/<int:pk>/', LocalLawNoteDetail.as_view(), name='local_law_note-detail'),
]
