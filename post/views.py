from django.shortcuts import render,get_object_or_404 , redirect ,reverse
from .models import Post
from django.contrib import messages
from comment.models import Comment
from like.models import LikePost
from django.contrib.auth.models import User
from .forms import AddPostForm , EditPostForm , DeletePostForm , AddCommentForm ,AddReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

def all_posts(request):
    posts=Post.objects.all()
    return render (request , 'post/all_posts.html',context={'posts':posts})

def post_detail(request,year,month,day,slug):
    post = get_object_or_404(Post,created__year=year,created__month=month,created__day=day,slug__exact=slug)
    comment = Comment.objects.filter(post = post , is_reply = False)
    reply = Comment.objects.filter(post = post , is_reply = True , reply = comment)
    count = LikePost.objects.filter(post = post).count()
    user = get_object_or_404(User, id = request.user.id)
    try:
        like = LikePost.objects.get(user = user , post = post)
        tag = 'warning'
        value = 'UnLike'
    except:
        tag = 'primary'
        value = 'Like'        

    if request.user == post.user:
        owner = True
    else:
        owner = False
    return render(request,'post/post_detail.html',context={'post':post , 'owner':owner , 'comments':comment , 'replies':reply , 'count':count , 'tag':tag , 'value':value})


@login_required
def add_post(request , user_id):
    if request.user.id == user_id:
        if request.method =="POST":
            form = AddPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.slug = slugify(form.cleaned_data['body'][:20])
                post.save()
                messages.success(request,'Your post submitted successfully','success')
                return redirect ('account:user_dashboard',user_id)

        else:
            form = AddPostForm
            return render(request,'post/add_post.html',{'form':form})
    else:
        return redirect ('post:all_posts')



@login_required
def edit_post(request , post_id , user_id):
    if request.user.id == user_id:
        post = Post.objects.get(pk = post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST)
            if form.is_valid:
                ep = form.save(commit=False)
                ep.user = post.user
                ep.slug = slugify(form.cleaned_data['body'][:30])
                ep.save()
                post.delete()
                messages.success(request,'Your post edited.',extra_tags='success')
                return redirect('account:user_dashboard' , user_id)
        else:
            form=EditPostForm(instance = post)
            return render(request ,'post/edit_post.html',{'form':form , 'post':post})
    else:
        return redirect ('post:all_posts')

@login_required
def delete_post(request , post_id , user_id):
    post = get_object_or_404(Post , pk = post_id)
    if user_id == post.user.id:
        if request.method == 'POST':
            post.delete()
            messages.success(request,'Your post deleted.',extra_tags='success')
            return redirect('account:user_dashboard' , user_id)
        else:
            post = {'body':post.body , 'id':post.id}
            return render (request , 'post/delete_post.html',{'post':post})
    else:
        return redirect ('post:all_posts')

@login_required
def add_comment(request,post_id,user_id):
    user = get_object_or_404(User , id = user_id)
    post = get_object_or_404(Post ,id=post_id)
    if request.user.id == user_id:
        if request.method=="POST":
            form = AddCommentForm(request.POST)
            if form.is_valid:
                c = form.save(commit=False)
                c.user = user
                c.post = post
                c.save()
                messages.success(request,'Your comment submitted successfully' , extra_tags='success')
                return redirect (Post.get_absolute_url(post))
        else:
            form = AddCommentForm()
            return render (request,'post/add_comment.html',context = { 'form':form , 'post':post , 'user':user }) 


@login_required
def add_reply(request , post_id , comment_id , user_id):
    post_id = post_id
    comment_id = comment_id
    user_id = user_id
    user = get_object_or_404(User,id=user_id)
    comment = get_object_or_404(Comment,id=comment_id)
    post = get_object_or_404(Post,id=post_id)
    if request.method=='POST':
        form = AddReplyForm(request.POST)
        if form.is_valid:
            r = form.save(commit=False)
            r.user = user
            r.post = post
            r.reply = comment
            r.is_reply = True
            r.save()
            messages.success(request,'Your reply submitted','success')
            return redirect (Post.get_absolute_url(post))
    else:
        form = AddReplyForm()
        return render (request,'post/add_reply.html',{'form':form , 'post_id':post_id , 'user_id':user_id , 'comment_id':comment_id})


def like_post(request,post_id,user_id):
    user = get_object_or_404(User, id = user_id)
    post = get_object_or_404(Post,id=post_id)
    try:
        like_post = LikePost.objects.get(user = user , post = post)
        like_post.delete()
        messages.success(request,'Your liked ommited','error')
        return redirect(Post.get_absolute_url(post))
    except:
        like_post = LikePost(user = user , post = post)
        like_post.save()
        messages.success(request,'You liked post' , 'success')
        return redirect(Post.get_absolute_url(post))


        


