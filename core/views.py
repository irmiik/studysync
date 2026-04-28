from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import StudyRoom, Message, Note
from .forms import RoomForm


def home(request):
    return render(request, 'home.html')


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


def room_list(request):
    query = request.GET.get('q')

    if query:
        rooms = StudyRoom.objects.filter(title__icontains=query)
    else:
        rooms = StudyRoom.objects.all()

    return render(request, 'rooms.html', {'rooms': rooms})


def create_room(request):

    if not request.user.is_authenticated:
        return render(request, 'must_login.html')

    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            return redirect('rooms')

    return render(request, 'create_room.html', {'form': form})


# 🔥 ROOM DETAIL (CHAT + NOTES)
def room_detail(request, pk):
    room = get_object_or_404(StudyRoom, id=pk)

    if not request.user.is_authenticated:
        return render(request, 'must_login.html')

    # kullanıcıyı ekle
    room.participants.add(request.user)

    # note oluştur / getir
    note, created = Note.objects.get_or_create(room=room)

    # 🔥 CHAT AJAX
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            msg = Message.objects.create(
                user=request.user,
                room=room,
                content=content
            )

            return JsonResponse({
                "username": request.user.username,
                "content": msg.content
            })

    messages = Message.objects.filter(room=room)

    return render(request, 'room_detail.html', {
        'room': room,
        'messages': messages,
        'participants': room.participants.all(),
        'notes': note.content
    })


# 🔥 NOTES SAVE (BU EKSİKTİ)
def save_notes(request, pk):
    room = get_object_or_404(StudyRoom, id=pk)
    note, created = Note.objects.get_or_create(room=room)

    if request.method == "POST":
        content = request.POST.get("content")
        note.content = content
        note.save()
        return JsonResponse({"status": "ok"})