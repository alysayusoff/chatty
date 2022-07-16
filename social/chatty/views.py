from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import *
from .models import *

def register(request):
    # global var that determines whether a new user has been registered
    registered = False
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # request user_form data
        user_form = UserForm(data=request.POST)
        # request profile_form data
        profile_form = UserProfileForm(data=request.POST)
        # verify the forms
        if user_form.is_valid() and profile_form.is_valid():
            # save user_form data
            user = user_form.save()
            # set user password and save
            user.set_password(user.password)
            user.save()
            # get model object
            profile = profile_form.save(commit=False)
            # set user
            profile.user = user
            # populate data
            if 'first_name' in user_form.cleaned_data:
                profile.first_name = request.DATA['first_name']
            if 'last_name' in user_form.cleaned_data:
                profile.first_name = request.DATA['last_name']
            # save profile data
            profile.save()
            # set registered to True
            registered = True
        else:
            # print errors if unsuccessful
            print(user_form.errors, profile_form.errors)
    else:
        # render the forms when register.html is accessed
        user_form = UserForm()
        profile_form = UserProfileForm()
    # return render register.html with context data
    return render(request, 'chatty/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        })

def user_login(request):
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # request username data
        username = request.POST['username']
        # request password data
        password = request.POST['password']
        # authenticate the user
        user = authenticate(username=username, password=password)
        # if user has been authenticated
        if user:
            if user.is_active:
                # log user in
                login(request, user)
                # redirect to home page
                return HttpResponseRedirect('../home/')
            else:
                return HttpResponse("Your account is disabled.")
        # if user authentication has failed
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'chatty/login.html')

def user_logout(request):
    # log user out
    logout(request)
    # redirect to login page
    return HttpResponseRedirect('../login/')

def profile(request):
    # get user
    user_info = AppUser.objects.get(user=request.user)
    # get all requests that have yet to be accepted by user
    friendrequest = FriendRequest.objects.filter(receiver=user_info, status='sent')
    # get total number of requests
    num_requests = FriendRequest.objects.filter(receiver=user_info, status='sent').count()
    # return render profile.html with context data
    return render(request, 'chatty/profile.html', {
        'profile' : user_info,
        'friend_requests' : friendrequest,
        'num_requests' : num_requests
    })

def edit(request):
    # get user
    user_info = AppUser.objects.get(user=request.user)
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # get POST data for user_form with instance of user
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        # get POST data for profile_form with instance of user
        profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user_info)
        # verify form
        if user_form.is_valid() and profile_form.is_valid():
            # save and redirect
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            print("user_form: ", user_form.errors)
            print("profile_form: ", profile_form.errors)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=user_info)

    return render(request, 'chatty/edit.html', {
        'profile' : user_info,
        'user_form' : user_form,
        'profile_form' : profile_form
    })

def search(request):
    # get user
    user_info = AppUser.objects.get(user=request.user)
    # get all other users
    users = AppUser.objects.all().exclude(user=request.user)
    # get all friend requests where user is the sender
    receive_req = FriendRequest.objects.filter(sender=user_info)
    # get all friend requests where user is the receiver
    send_req = FriendRequest.objects.filter(receiver=user_info)
    # lists to be passed as context
    receiver_req = []
    sender_req = []
    # for each request (where user is sender)
    for r in receive_req:
        # append with receiver's user object
        receiver_req.append(r.receiver.user)
    # for each request (where user is receiver)
    for r in send_req:
        # append with sender's user object
        sender_req.append(r.sender.user)
    
    return render(request, 'chatty/search.html', {
        'profile' : user_info,
        'users' : users,
        'receiver_req' : receiver_req,
        'sender_req' : sender_req
    })

def view(request):
    # if request.method == 'GET' =====> form has been submitted
    if request.method == 'GET':
        # get user
        user_info = AppUser.objects.get(user=request.user)
        # get user you are trying to see the profile of
        requested_user = AppUser.objects.get(pk=request.GET.get('user_pk'))

    return render(request, 'chatty/view.html', {
        'profile' : user_info,
        'requested_user' : requested_user
    })

def home(request):
    # superuser has not account on the website, but access to django admin site, so super users will be 
    # redirected to the admin site instead
    if request.user.is_superuser:
        return HttpResponseRedirect('../admin/')
    else:
        # get all posts
        posts = Post.objects.all()
        # get user
        user = AppUser.objects.get(user=request.user)
        # global var that determines whether a new post has been made
        posted = False
        # if request.method == 'POST' =====> form has been submitted
        if request.method == 'POST':
            # retrieve form data
            # request.POST or None =====> in the case some data is missing
            # request.FILES or None =====> in the case some files are missing, i.e. image that can be left blank
            post_form = PostForm(request.POST or None, request.FILES or None)
            # verify the form
            if post_form.is_valid():
                # save data
                post = post_form.save(commit=False)
                post.author = user
                post.save()
                posted = True
                # clear the form
                post_form = PostForm()
        else:
            post_form = PostForm()
        # return context data
        return render(request, 'chatty/home.html', {
            'posts' : posts,
            'profile' : user,
            'post_form' : post_form,
            'posted' : posted
        })

def send_request(request):
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # get sender (user)
        sender = AppUser.objects.get(user=request.user)
        # get receiver by using pk data from POST
        receiver = AppUser.objects.get(pk=request.POST.get('user_pk'))
        # create new FriendRequest object and set status to 'sent'
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver, status='sent')
        # redirect back to referer page
        return redirect(request.META.get('HTTP_REFERER'))

def accept_request(request):
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # get friendrequest, or if does not exist, throw 404 error
        friend_request = get_object_or_404(FriendRequest, pk=request.POST.get('request_pk'))
        # change status from 'sent' to 'accept' and save
        if friend_request.status == 'sent':
            friend_request.status = 'accepted'
            friend_request.save()
    # redirect back to profile page
    return redirect('profile')

def remove_request(request):
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # get friendrequest, or if does not exist, throw 404 error
        friend_request = get_object_or_404(FriendRequest, pk=request.POST.get('request_pk'))
        # delete field
        friend_request.delete()
    # redirect back to profile page
    return redirect('profile')

def remove_friend(request):
    # if request.method == 'POST' =====> form has been submitted
    if request.method == 'POST':
        # get sender (user)
        sender = AppUser.objects.get(user=request.user)
        # get receiver by using pk data from POST
        receiver = AppUser.objects.get(pk=request.POST.get('user_pk'))
        # when deleting a friend, in the model, a user could possibly be a sender or a receiver
        # hence we use Q to initiate an instance as such
        friend_request = FriendRequest.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        # delete friend
        friend_request.delete()
        return redirect(request.META.get('HTTP_REFERER'))