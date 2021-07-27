from django.contrib.auth.models import User
from blog.models import amberuser, comment, post, resetpassword, temperoryaccount
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from random import randint
from django.contrib.auth import authenticate
from django.conf import settings
# Create your views here.
# generate random string


def random_string(num):
    final = ''
    li = 'abcdefghijklmnopqrstuxwzyABCDEFJHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(1,num+1):
        random_index = randint(1,60)
        final += li[random_index]
    return final



def home(request):
    
    posts = post.objects.all().order_by('-date')
    context = {
        'posts' : posts
    }
    return render(request , 'blog/homepage/home.html' , context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    context = {
        'usernameerror' : '',
        'passworderror' : '',
        'passwordagainerror' : '',
        'emailerror' : ''
    }
    if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST and 'passwordagain' in request.POST:
        password = request.POST['password']
        passwordagain = request.POST['passwordagain']
        username = request.POST['username']
        email = request.POST['email']
        haserror = False
        if password != passwordagain :
            context['passwordagainerror'] = 'passwords are not the same'
            haserror = True
        sameusers = amberuser.objects.filter(username = username).count()
        if sameusers != 0 :
            context['usernameerror'] = 'this username is not unique'
            haserror = True
        sameuserseamil = amberuser.objects.filter(email = email).count()
        if sameuserseamil != 0 :
            context['emailerror'] = 'email should be unique'
            haserror = True
        
        if haserror:
            return render(request , 'blog/signup/signup.html' , context)
        
        code = random_string(50)
        temp_account = temperoryaccount.objects.create(username = username , password = password , email = email , code = code)
        temp_account.save()

        subject = 'amber signup'
        message = 'here is the famous link.  {}?code={}'.format(request.build_absolute_uri('/signup/'), code)
        recepient = email
        send_mail(subject, 
        message, settings.EMAIL_HOST_USER, [recepient], fail_silently = False)
        context = {
            'header' : 'activation link just sent !',
            'body' : 'activate your account with open it :|'
        }
        return render(request , 'alert.html' , context)
    elif 'code' in request.GET :
        code = request.GET['code']
        # check if link is true and we sent it
        user_exist = temperoryaccount.objects.filter(code = code)
        if user_exist.count() == 0 :
            context = {
                'header' : 'wrong code !',
                'body' : 'the code is wrong !'
            }
            return render(request , 'alert.html' , context )  
        
        this_user = user_exist.get()
        password = user_exist[0].password 

        # managing data
        username = user_exist[0].username
        email = user_exist[0].email

        # check if this user is unique or not
        sameusr = amberuser.objects.filter(username = username , email = email)
        if sameusr.count() != 0 :
            # oops! some asshole wants to use activate their account twice !123
            context = {
                    'header' : 'this account has been activated before !',
                    'body' : 'this account has been activated before !'
                }
            return render(request , 'alert.html' , context ) 

        # creating the activated user here
        newuser = amberuser.objects.create(username = username , password = make_password(password) , email = email )
        newuser.save()
        login(request , newuser)
        return redirect('blog-home')
    else:
        return render(request , 'blog/signup/signup.html')

def about(request):
    context = {
        'header' : 'About the project',
        'body' : 'still working on this project.<br>if you don\'t like this webiste, you can easily fuck yourself in few simple steps.<br>if there is anything cringe about this website, put it in your ass cause no one cares about it.<br>oh BTW, share this website if you are not <strong>gay!</strong><br>(I can see who didn\'t share)',
    }
    return render(request , 'alert.html' , context)

def loginuser(request):
    if request.user.is_authenticated:
        context = {
                'header' : 'silly error',
                'body' : 'already logged in !',
            }
        return render(request , 'alert.html' , context)
    elif 'username' in request.POST and 'password' in request.POST :
        print(request.POST['username'] , request.POST['password'])
        thisuser = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(thisuser)
        if thisuser is None :
            context = {
                'usernameerror' : 'username or password is wrong !',
            }
            return render(request , 'blog/login/login.html' , context)
        login(request ,thisuser)
        return redirect('blog-home')
    else:
        return render(request , 'blog/login/login.html')

def newpost(request):
    if request.user.is_authenticated:
        if 'title' in request.POST and 'summary' in request.POST and 'content' in request.POST :
            title = request.POST['title']
            summary = request.POST['summary']
            content = request.POST['content']
            if 'enablecomment' in request.POST:
                enablecontentbool = True
            else:
                enablecontentbool = False
            thisamberuser = amberuser.objects.get(username = request.user.username)
            newpost = post.objects.create(author = thisamberuser , title = title , summary = summary , content = content , hascomment = enablecontentbool )
            newpost.save()
            
            return redirect('postpage' , newpost.id)
        else:
            return render(request , 'blog/newpost/newpost.html')
    else:
        return redirect('login')

def profile(request , username):
    
    thisuser = get_object_or_404(amberuser , username = username)
    related_posts = post.objects.filter(author = thisuser).order_by('-date')
    context = {
        'thisuser' : thisuser,
        'posts' : related_posts,
    }
    return render(request , 'blog/profilepage/profilepage.html' , context)
    
    

def editprofile(request , username):
    
    if request.user.is_authenticated:
        context = {}
        context['usernameerror'] = ''
        thisuser = get_object_or_404(amberuser , username = username)
        if thisuser.username != request.user.username:
            context = {
                'header' : 'hmmm',
                'body' : 'you think you are samrt ha ?',
            }
            return render( request , 'alert.html' , context)
        if 'username' in request.POST and 'bio' in request.POST:
            newusername = request.POST['username']
            bio = request.POST['bio']
            
            if 'image' in request.FILES:
                image = request.FILES['image']
                thisuser.avatar = image
                thisuser.save()
                print(newusername , bio , image)
            print(newusername , bio)
            if newusername != thisuser.username :
                sameusername = amberuser.objects.filter(username = newusername).count()
                if sameusername != 0:
                    context['usernameerror'] = 'the user name exist before'
                    context['thisuser'] = thisuser
                    return render(request ,'blog/editprofile/editprofile.html' , context )
                else:
                    thisuser.username = newusername
                    thisuser.save()
            
            if bio != thisuser.bio :
                thisuser.bio = bio
                thisuser.save()


            context['thisuser'] = thisuser
            
            return redirect('profile' , thisuser.username)
        else:
            context['usernameerror'] = ''
            context['thisuser'] = thisuser
            return render(request , 'blog/editprofile/editprofile.html' , context)
    else:
        return redirect('login')




def deletepost(request , id):
    if request.user.is_authenticated:
        this_post = get_object_or_404(post , id=id)
        thisamberuser = amberuser.objects.get(username = request.user.username)
        if thisamberuser == this_post.author:
            this_post.delete()
            return redirect('blog-home')
        else:
            context = {
                'header' : 'you asshole',
                'body' : 'what the fuck  did you just want to do ?! you little shit ...',
            }
            return render(request , 'alert.html' , context)
    else:
        return redirect('login')
def postpage(request , id):
    
    if 'comment' in request.POST:
        this_post = get_object_or_404(post , id=id)
        thisamberuser = amberuser.objects.get( username = request.user.username)
        newcomment = comment.objects.create(author = thisamberuser , content = request.POST['comment'] , related_post = this_post)
        newcomment.save()
        return redirect('postpage' , id)
    else:
        this_post = get_object_or_404(post , id=id)
        comments =comment.objects.filter(related_post = this_post).order_by('-date')
        context = {
            'post' : this_post ,
            'comments' : comments,
        }
        return render(request , 'blog/postpage/postpage.html' , context)


def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('blog-home')
    else:
        context = {
                'header' : 'silly error',
                'body' : 'already logged out !',
            }
        return render(request , 'alert.html' , context)


def editpost(request , id):
    if request.user.is_authenticated:
        this_post = get_object_or_404(post , id = id)
        if request.user.username != this_post.author.username:
            context = {
                'header' : 'hmmm',
                'body' : 'you think you are samrt ha ?',
            }
            return render( request , 'alert.html' , context)
        
        if request.method == "POST":
            if request.POST['title'] != this_post.title :
                this_post.title = request.POST['title']
            if request.POST['summary'] != this_post.summary:
                this_post.summary = request.POST['summary']

            if request.POST['content'] != this_post.content:
                this_post.content = request.POST['content']

            if 'enablecomment' in request.POST:
                enablecontentbool = True
            else:
                enablecontentbool = False
            this_post.hascomment = enablecontentbool
            this_post.save()

            return redirect('postpage' , this_post.id)
        else:
            context = {'post' : this_post}
            return render(request , 'blog/editpost/editpost.html' , context)
    else:
        return redirect('login')


def resetpasswords(request):
    context = {'usernameerror' : ''}
    if 'username' in request.POST :
        sameusers = amberuser.objects.filter(username = request.POST['username'])
        sameuser = sameusers.count()
        if sameuser == 0 :
            context = {
                'header' : 'unknown username' ,
                'body' : 'this username doesn\'t exist !'
            }
            return render(request , 'alert.html' , context)
        code = random_string(50)
        RSreq = resetpassword.objects.create(username = request.POST['username'] , code = code)
        RSreq.save()
        subject = 'amber resetpassword'
        message = 'here is the famous link. keep it safe to reset password  {}?code={}'.format(request.build_absolute_uri('/resetpassword/'), code)
        recepient = sameusers[0].email
        send_mail(subject, 
        message, settings.EMAIL_HOST_USER, [recepient], fail_silently = False)
        context = {
            'header' : 'activation link just sent !',
            'body' : 'activate the reset password with open it :|'
        }
        return render(request , 'alert.html' , context)
    elif 'code' in request.GET:
        user = resetpassword.objects.filter(code = request.GET['code'])
        if user.count() == 0 :
            context = {
            'header' : 'wrong link  !',
            'body' : 'the code doesn\'t exist dude.'
            }
            return render(request , 'alert.html' , context)


        if user[0].linkuseronce :
            context = {
            'header' : 'link expired ',
            'body' : 'the link is dead bro.'
            }
            return render(request , 'alert.html' , context)

        context = {
            'token' : request.GET['code'],
        }
        return render(request , 'blog/resetpassword/resetpasswordend.html' , context )
    elif 'newpassword' in request.POST and 'token' in request.POST :
        code = request.POST['token']
        newpass = request.POST['newpassword']
        user = resetpassword.objects.filter(code = code )
        if user.count() == 0 :
            context = {
            'header' : 'wrong link  !',
            'body' : 'the code doesn\'t exist dude.'
            }
            return render(request , 'alert.html' , context)


        if user[0].linkuseronce :
            context = {
            'header' : 'link expired ',
            'body' : 'the link is dead bro.'
            }
            return render(request , 'alert.html' , context)

        user.linkuseronce = True
        AU = amberuser.objects.get(username = user[0].username)
        AU.password = make_password(newpass)
        AU.save()
        context = {
            'header' : 'password changed',
            'body' : 'new password is {}'.format(newpass)
            }
        return render(request , 'alert.html' , context)
    else:
        return render(request , 'blog/resetpassword/resetpassword.html' , context )