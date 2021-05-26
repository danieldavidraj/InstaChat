from django.shortcuts import render
import json
from user.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def room(request, room_name):
    name=request.GET["name"] # receiver
    username=request.GET["user"] # sender
    UserData = UserProfile.objects.all()
    users_list=""
    messages_list=""
    for user in UserData:
        # ignore same username and receiver
        if username!=user.username and user.username!=name:
            # create unique room name by lexicographic order
            words=[username,user.username]
            words.sort()
            users_list+='<a href="/chat/'+words[0]+'_'+words[1]+'/?name='+user.username+'&user='+username+'"><div class="chat_list active_chat"><div class="chat_people"><div class="chat_img"> <img src="https://iconape.com/wp-content/png_logo_vector/android-messages.png" alt="sunil"> </div><div class="chat_ib"><h5>'+user.username+'</h5></div></div></div></a>'
        # get messages of user and not null and should not be displayed in lobby
        if username==user.username and user.Messages and name!="lobby":
            dict_messages=json.loads(user.Messages) # convert to dictionary
            if dict_messages and name in dict_messages.keys(): # if dict is not empty and messages from the receiver is available
                for info in dict_messages[name]:
                    messages_list+='<div class="incoming_msg"><div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="user"> </div><div class="received_msg"><div class="received_withd_msg"><p>'+info["message"]+'</p><span class="time_date">'+info["time"]+'</span></div></div></div>'
    return render(request, 'room.html', {'room_name': room_name,'name' : name,'user': username,'users_list':users_list,'messages_list':messages_list})
