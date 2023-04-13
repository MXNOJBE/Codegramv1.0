from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login


from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from authy.models import Profile,ChooseForm,Choose
from .forms import EditProfileForm, UserRegisterForm,ProfileUpdateForm,R_UpdateForm
from django.urls import resolve
from comment.models import Comment

def UserProfile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile':profile,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'profile.html', context)

def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        r_form = R_UpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if form.is_valid():
            '''
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()'''
            
            form.save()
            if request.user.is_staff:
                r_form.save()
            else:
                profile_form.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
        profile_form = ProfileUpdateForm(instance=request.user.profile) #"userprofile" model -> OneToOneField relatinon with user
        r_form = R_UpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
    context = {
        'form':form,'r_form':r_form,
            'profile_form': profile_form
    }
    return render(request, 'editprofile.html', context)

def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


def choose(request):
    if request.method=='POST':
        form=ChooseForm(request.POST)
        if form.is_valid():
            c=Choose()
            c.c_id=form.cleaned_data['c_id']
            c.save()
            print(c.c_id)
            if c.c_id == 1:
                return HttpResponseRedirect('/users/sign-up/1')
            elif c.c_id == 2:
                return HttpResponseRedirect('/users/sign-up/2')
            else:
                return HttpResponseRedirect('/users/sign-up/3')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/choose')
    form=ChooseForm()
    return render(request,'userauths/choose.html',{'form':form})


def register(request,c_id):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            user=User.objects.filter(username=username).first()
            if c_id == 1:
                user.is_staff=True
            user.save()
            login(request, new_user)
            # return redirect('editprofile')
            
            return redirect('/users/profile/edit')
            


    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)