from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from content.models import Video, Like, Comment, Subscribe, Detail
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
# Create your views here.


def home_page(request, *args, **kwargs):
    data = Video.objects.values('title', 'url', 'uploaded_by__username', 'video_id')
    detail = {}
    if (request.user.id is not None):
        detail = Detail.objects.get(user=request.user)

    return render(request, 'home.html', {'data': data, 'detail': detail})


def signup_page(request, *args, **kwargs):
    if (request.POST):
        if(User.objects.filter(username=request.POST['name'])):
            return render(request, 'signup.html', {'error': 'user with this username already exists!!'})
        else:
            curr_user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
            curr_user.save()
            Detail(user=curr_user).save()
            return redirect(home_page)
    else:
        return render(request, 'signup.html')


def login_page(request, *args, **kwargs):
    if (request.POST):
        user = authenticate(username=request.POST['name'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(home_page)
        else:
            return render(request, 'login.html', {'error': 'invalid username or password!!'})
    else:
        return render(request, 'login.html')


def create_page(request, *args, **kwargs):
    if request.method == 'POST':
        myfile = request.FILES['filename']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        user = User.objects.get(username=request.user)
        new_video = Video(title=request.POST['title'], description=request.POST['desc'], url=fs.url(filename), uploaded_by=user)
        new_video.save()
        return redirect(home_page)

    else:
        if (request.user.id is not None):
            return render(request, 'create.html')
        else:
            return redirect(login_page)


def update_page(request, *args, **kwargs):
    if request.method == 'POST':
        detail = Detail.objects.get(user=request.user)
        if (request.FILES.get('profile_pic') is not None):
            detail.profile_pic = FileSystemStorage().url(FileSystemStorage().save(request.FILES['profile_pic'].name, request.FILES['profile_pic']))
        if (request.FILES.get('profile_cover') is not None):
            detail.profile_cover = FileSystemStorage().url(FileSystemStorage().save(request.FILES['profile_cover'].name, request.FILES['profile_cover']))
        if (request.POST.get('user_desc') is not None):
            detail.user_description = request.POST['user_desc']
        detail.save()
        return redirect('/user?uname='+request.user.username)
    else:
        return render(request, 'update.html')


def video_page(request, *args, **kwargs):
    id = request.GET.get('id')
    video = Video.objects.get(video_id=id)
    like_query = Like.objects.filter(like_video=video, liked_by__username=request.user)
    subscribe_query = Subscribe.objects.filter(subscribee=video.uploaded_by, subscriber__username=request.user)
    likes_count = Like.objects.filter(like_video=video).count
    subscribers_count = Subscribe.objects.filter(subscribee=video.uploaded_by).count
    comment_data = Comment.objects.filter(comment_video=video).values('content', 'commented_by__username')
    comment_arr = []
    for row in comment_data:
        curr = {}
        curr['content'] = row['content']
        curr['commented_by__username'] = row['commented_by__username']
        curr['profile_pic'] = Detail.objects.get(user=User.objects.get(username=row['commented_by__username'])).profile_pic
        comment_arr.append(curr)

    video_data = Video.objects.values('title', 'url', 'uploaded_by__username', 'video_id')
    detail = Detail.objects.get(user=video.uploaded_by)
    login_user_detail = {}

    if (request.user.id is not None):
        login_user_detail = Detail.objects.get(user=request.user)

    liked = True
    subscribed = True

    if not like_query:
        liked = False
    if not subscribe_query:
        subscribed = False

    return render(request, 'video.html', {'video': video, 'liked': liked, 'subscribed': subscribed, 'videos_data': video_data, 'comments_data': comment_arr, 'likes_count': likes_count, 'subscribers_count': subscribers_count, 'detail': detail, 'login_user_detail': login_user_detail})


def user_page(request, *args, **kwargs):
    user_videos = Video.objects.filter(uploaded_by__username=request.GET.get('uname')).values()
    curr_user = User.objects.get(username=request.GET.get('uname'))
    user_subscribers = Subscribe.objects.filter(subscribee=curr_user)
    detail = Detail.objects.get(user=curr_user)
    subscribe_query = Subscribe.objects.filter(subscribee=curr_user, subscriber__username=request.user)
    subscribed = True
    if not subscribe_query:
        subscribed = False

    return render(request, 'user.html', {'data': user_videos, 'subscribers_count': user_subscribers.count, 'curr_user': curr_user, 'detail': detail, 'subscribed': subscribed})


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect(home_page)


def like_view(request, *args, **kwargs):
    if (request.user.id is not None):
        video = Video.objects.get(video_id=request.GET.get('video'))
        user = User.objects.get(username=request.user)
        allready_liked = Like.objects.filter(like_video=video, liked_by=user)

        if not allready_liked:
            new_like = Like(like_video=video, liked_by=user)
            new_like.save()

        else:
            allready_liked.delete()

        url = "/video?id="+request.GET.get('video')
        return redirect(url)
    else:
        return redirect(login_page)


def comment_view(request, *args, **kwargs):
    if (request.user.id is not None):
        video = Video.objects.get(video_id=request.GET.get('id'))
        user = User.objects.get(username=request.user)
        comment_content = request.POST['comment']
        new_comment = Comment(comment_video=video, commented_by=user, content=comment_content)
        new_comment.save()

        url = "/video?id="+request.GET.get('id')
        return redirect(url)
    else:
        return redirect(login_page)


def subscribe_view(request, *args, **kwargs):
    if (request.user.id is not None):
        user_subscribee = User.objects.get(username=request.GET.get('subscribee'))
        user_subscriber = User.objects.get(username=request.GET.get('subscriber'))
        allready_subscribed = Subscribe.objects.filter(subscriber=user_subscriber, subscribee=user_subscribee)

        if not allready_subscribed:
            new_connection = Subscribe(subscriber=user_subscriber, subscribee=user_subscribee)
            new_connection.save()

        else:
            allready_subscribed.delete()

        if (request.GET.get('video') is not None):
            url = "/video?id="+request.GET.get('video')
        else:
            url = "/user?uname="+request.GET.get('uname')

        return redirect(url)
    else:
        return redirect(login_page)
