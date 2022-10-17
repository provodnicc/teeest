from django.urls import path
from .views import *

urlpatterns = [
    path('notes', GetNotesView.as_view()),
    path('', homePage),
    path('create', createNoteView.as_view()),
    path('update', updateNotesView.as_view()),
    path('delete', deleteNoteView.as_view())
]