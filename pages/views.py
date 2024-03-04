from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from content.models import Video, Like, Comment, Subscribe
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
# Create your views here.


def home_page(request, *args, **kwargs):
    data = Video.objects.values('title', 'url', 'uploaded_by__username', 'video_id')
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user, 'data': data})
    else:
        return render(request, 'home.html', {'user': 'null', 'data': data})


def signup_page(request, *args, **kwargs):
    if (request.POST):
        user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
        user.save()
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
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def create_page(request, *args, **kwargs):
    if request.method == 'POST':
        myfile = request.FILES['filename']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        user = User.objects.get(username=request.user.username)
        print(filename)
        new_video = Video(title=request.POST['title'], description=request.POST['desc'], url=fs.url(filename), uploaded_by=user)
        new_video.save()
        return redirect(home_page)

    else:
        return render(request, 'create.html')


def video_page(request, *args, **kwargs):
    id = request.GET.get('id')
    video = Video.objects.get(video_id=id)
    like_query = Like.objects.filter(like_video=video, liked_by__username=request.user)
    subscribe_query = Subscribe.objects.filter(subscribee=video.uploaded_by, subscriber__username=request.user)
    comment_data = Comment.objects.filter(comment_video=video).values('content', 'commented_by__username')
    video_data = Video.objects.values('title', 'url', 'uploaded_by__username', 'video_id')

    liked = True
    subscribed = True

    if not like_query:
        liked = False
    if not subscribe_query:
        subscribed = False

    return render(request, 'video.html', {'user': request.user, 'video': video, 'liked': liked, 'subscribed': subscribed, 'videos_data': video_data, 'comments_data': comment_data})


def user_page(request, *args, **kwargs):
    return render(request, 'user.html')


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect(home_page)


def like_view(request, *args, **kwargs):
    # print(request)
    video = Video.objects.get(video_id=request.GET.get('video'))
    user = User.objects.get(username=request.user)
    
    new_like = Like(like_video=video, liked_by=user)
    new_like.save()

    url = "/video?id="+request.GET.get('video')
    return redirect(url)

    # return redirect("/video?"+request.GET.get('video'))


def comment_view(request, *args, **kwargs):
    # print(request.POST, request.GET)
    video = Video.objects.get(video_id=request.GET.get('id'))
    user = User.objects.get(username=request.user)
    comment_content = request.POST['comment']
    
    new_comment = Comment(comment_video=video, commented_by=user, content=comment_content)
    new_comment.save()
    url = "/video?id="+request.GET.get('id')
    return redirect(url)


def subscribe_view(request, *args, **kwargs):
    user_subscribee = User.objects.get(username=request.GET.get('subscribee'))
    user_subscriber = User.objects.get(username=request.GET.get('subscriber'))
    
    new_connection = Subscribe(subscriber=user_subscriber, subscribee=user_subscribee)
    new_connection.save()

    url = "/video?id="+request.GET.get('video')

    return redirect(url)
