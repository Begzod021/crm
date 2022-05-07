from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from account.models import *
from account.models import Employe
from contact.models import Contact
from .models import Dialog_chat, Message
from .forms import MessageForm
from task.models import *
from django.contrib.auth.decorators import login_required




@login_required(login_url='user_login')
def chat(request, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user1 = User.objects.get(username=username)
        employe = Employe.objects.get(user=user1)
        position1 = Postion.objects.get(id=employe.position.id)
        employes = Employe.objects.all()
        users = User.objects.all()
        task_count = Task.objects.filter(employe=employe).order_by('-id')
        user = request.user
        employee = Employe.objects.get(user=user)
        ctx = {
            'employee': employee,
            'employe':employe,
            'position1':position1,
            'employes':employes,
            'users':users,
            'task_count':task_count,
        }

        if request.GET.get('contact', None):
            
            contact = Contact.objects.get(id=request.GET.get('contact_id'))
            receiver_id = contact.add_contact_id
            receiver = Employe.objects.get(id=receiver_id)
            
            if receiver.avatar:
                receiver_avatar_url = receiver.avatar.url
            else:
                receiver_avatar_url = None
                
            try:
                dialog_room = Dialog_chat.objects.get(
                    Q(sender_id=receiver_id, receiver_id=employee.id) |
                    Q(sender_id=employee.id, receiver_id=receiver_id)
                    )

                
                messages = list(Message.objects.filter(dialog_id=dialog_room.id).values())
                
                
                
                for message in messages:
                    message['time'] = str(Message.objects.get(id=message['id']).time())
                    
                return JsonResponse({
                    'receiver_avatar_url': receiver_avatar_url,
                    'receiver_name': contact.__str__(),
                    'receiver_id': receiver_id,
                    'messages': messages,
                    })

            except:
                return JsonResponse({
                    'receiver_avatar_url': receiver_avatar_url,
                    'receiver_name': contact.__str__(),
                    'receiver_id': receiver_id,
                    'messages': [],
                    })
                    
                    
        return render(request, 'chat.html', ctx)


def send_message(request):
    user = request.user
    employee = Employe.objects.get(user=user)
    
    if request.POST:
        receiver_id = request.POST['receiver']
        
        try:
            dialog_room = Dialog_chat.objects.get(
                Q(sender_id=receiver_id, receiver_id=employee.id) |
                Q(sender_id=employee.id, receiver_id=receiver_id)
                )

        except:
            dialog_room = Dialog_chat.objects.create(
                sender_id = employee.id,
                receiver_id = receiver_id,
            )

        
        message = request.POST['message']
        author_id = employee.id
        dialog_id = dialog_room.id
        
        new_message = Message.objects.create(
            message = message,
            author_id = author_id,
            dialog_id = dialog_id,
        )
        
        return JsonResponse({
            'message': message, 
            'receiver_id': receiver_id, 
            'author_id': author_id,
            'message_time': new_message.time(),
            })