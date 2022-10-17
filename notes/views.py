from urllib import response
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework.response import Response 
from rest_framework.views import APIView

from django.shortcuts import render
from django.utils import timezone

from .serialize import NoteSerializer
# from django.http import HttpResponse, JsonResponse

from .models import Notes, UserNote
from customer.methods import getPayload, getToken
from customer.models import User
import jwt, uuid, json

def homePage(request):
    return render(request, 'Home.html')
def errorPage(request):
    return render(request, 'Error.html')


class GetNotesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed('Log in please')
        try:
            payload = getPayload(token)
        except:
            raise AuthenticationFailed('Auth error')

        user = User.objects.filter(id=payload['id']).first()
        usernotes = UserNote.objects.filter(user_id=user) 
        if not usernotes: 
            return Response('Заметок пока нет', status=201)
        notes = []

        for index in usernotes:
            notes.append(Notes.objects.get(pk=index.note_id.id))
        notes_dict = {}

        for note in notes:
            notes_dict[note.note_id] = {
                "header": note.header,
                "text" : note.text,
                "time": {
                    'Y': note.time.year,
                    'M': note.time.month,
                    'D': note.time.day,
                    'h': note.time.hour,
                    'm': note.time.minute,
                    's': note.time.second
                }
            } 
        token = getToken(user)
        response = Response(data=notes_dict, status=200)
        response.set_cookie(key='token', value=token, httponly=True)
        return response

class updateNotesView(APIView):
    def post(self, request):

        token = request.COOKIES.get('token')
        try:
            payload = getPayload(token)
        except:
            raise AuthenticationFailed('Auth error')
        user = User.objects.filter(id=payload['id']).first()

        if not token:
            raise AuthenticationFailed('login first')

        note = NoteSerializer(request.data).data

        if note:
            note_id = request.data['nid']
            header = note['header']
            text = note['text']


        note = Notes.objects.get(note_id=note_id)
        note.header = header
        note.text = text
        note.time=timezone.now()
        note.save()
        
        response = Response()
        response.data = NoteSerializer(note).data

        token = getToken(user)
        response.set_cookie(key='token', value=token, httponly=True)

        return response

class deleteNoteView(APIView):
    def get(self, request):

        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed('ligon first')
        try:
            payload = getPayload(token)
        except:
            raise AuthenticationFailed('ligon first')
            
        try:
            note_id = request.GET['note_id']
        except:
            raise APIException("note is undefined")
            
        user = User.objects.filter(pk=payload['id']).first()
        note = Notes.objects.filter(note_id=note_id).first()
        
        usernote = UserNote.objects.filter(note_id=note, user_id=user)
        if usernote:
            note.delete()
        else:
            raise APIException('unknown error')

        token = getToken(user)
        res = Response()
        res.data = NoteSerializer(note).data
        res.set_cookie(key='token', value=token, httponly=True)
        return res



class createNoteView(APIView):
    def post(self, request):
        data = NoteSerializer(request.data).data
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed('ligon first')
        try:
            payload = getPayload(token)
        except:
            raise AuthenticationFailed('login first')

        if data:
            header = data['header']
            text = data['text']
        

        note = Notes(text=text, header=header, note_id=uuid.uuid4(), time=timezone.now())
        note.save()
        notes = Notes.objects.all()
        print(notes)
        user = User.objects.filter(id=payload['id']).first()
        usernote = UserNote(note_id=note, user_id=user)
        usernote.save()
        
        response = Response()
        data = NoteSerializer(note)
        response.data = data.data
        return response
