from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollowersCount
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    
    user_profile=Profile.objects.get(user=user_object)

    user_following_list=[]
    feed=[]

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users)
    
    for usernames in user_following_list:
        feed_lists=Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    #user suggestion
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestion_list = [x for x in list(all_users) if x not in list(user_following_all)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if x not in list(current_user)]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    
    sugggestion_username_profile_list=list(chain(*username_profile_list))


    return render(request,'index.html',{'user_profile': user_profile, 'posts': feed_list,'sugggestion_username_profile_list':sugggestion_username_profile_list[:4]})

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method=="POST":
        username = request.POST["username"]
        username_object = User.objects.filter(username__icontains=username)
        
        if username_object:

            username_profile = []
            username_profile_list = []

            for users in username_object:
                username_profile.append(users.id)
        
            for ids in username_profile:
                profile_lists = Profile.objects.filter(id_user=ids)    
                username_profile_list.append(profile_lists)
        
            username_profile_list = list(chain(*username_profile_list))

            return render(request,'search.html',{'user_profile':user_profile, 'username_profile_list':username_profile_list,'username':username })

        else:
            return render(request,'search.html',{'user_profile':user_profile})

    return render(request,'search.html',{'user_profile':user_profile})

def signup(request):

    

    if request.method=='POST':
        username=request.POST['username']
        email2=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        print(email2)

        if password==password2:
            
            if User.objects.filter(email=email2).exists():
                messages.info(request,'Email is already registered')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is already taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email2,password=password)
                user.save()
                
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
 
                #create a profile for the user
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')


        else:
            messages.info(request,'Password Not Matching')
            return redirect('signup')
    else:
        return render(request,'signup.html')

def signin(request):


    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('signin')
    else:
        return render(request,'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def upload(request):
   # return render(request,.html')
    if request.method=="POST":
        user_object=User.objects.get(username=request.user.username)
    
        user_profile=Profile.objects.get(user=user_object)
        user_profile_img=user_profile.profileimg
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post= Post.objects.create(user=user,user_profile_img=user_profile_img,image=image,caption=caption)
        new_post.save()
        return redirect('/')

    else:
        return redirect('/')


@login_required(login_url='signin')
def profile(request,pk):
    user_object= User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_posts_length=len(user_posts)
    user_followers=len(FollowersCount.objects.filter(user=pk))
    user_following=len(FollowersCount.objects.filter(follower=pk))

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_posts_length':user_posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    return render(request,'profile.html',context)


    
@login_required(login_url='signin')
def like_post(request):
    user_object=User.objects.get(username=request.user.username)
    
    user_profile=Profile.objects.get(user=user_object)
    user_profile_img=user_profile.profileimg
    username = request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like=LikePost.objects.create(post_id=post_id,username=username,profileimg=user_profile_img)
        new_like.save()
        post.no_of_likes+=1
        post.liked_user.add(user_profile)
        post.save()
        return redirect('/')
    
    else:
        like_filter.delete()
        post.no_of_likes-=1
        post.liked_user.remove(user_profile)
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def follow(request):
    if request.method=="POST":
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.filter(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)

    else:
        return redirect('/')


@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method =="POST":
        
        if request.FILES.get('profile_img')==None:
            image=user_profile.profileimg
           
        
        if request.FILES.get('profile_img')!=None:
            image=request.FILES.get('profile_img')
        
        if request.FILES.get('cover_photo')==None:
            cover_image=user_profile.cover_photo
           
        
        if request.FILES.get('cover_photo')!=None:
            cover_image=request.FILES.get('cover_photo')



        bio=request.POST['bio']
        location= request.POST['location']

        user_profile.profileimg=image
        user_profile.cover_photo=cover_image
        user_profile.bio=bio
        user_profile.location=location
        user_profile.save()
        return redirect('setting')
         

    return render(request,'setting.html',{'user_profile': user_profile})