from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.views import generic
from kurultai.models import Account
from .forms import UserRegisterForm, RubricForm, CommentForm, Comment_mode_Form
from .models import Account, Rubrics, Post, Comment


def indexActive(request):
    print(Account.objects.all())
    rubrics = Rubrics.objects.all().order_by('-id')
    context = {'rubrics': rubrics, 'register_form': UserRegisterForm, 'login_form': AuthenticationForm}
    return render(request, 'indexActive.html', context)


def security(request):
    return render(request, 'security.html')


def post_list(request, pk):
    post = Post.objects.filter(status=1, id=pk).order_by("-created_on")

    context = {'post_list': post}
    return render(request, template_name='post_list.html', context=context)


def register(request):
    print('kirdi')
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        print(form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegisterForm()
    # return render(request=request, template_name="indexActive.html", context={"register_form": form})
    return redirect('/')


def loginpage(request):
    if request.method == "POST":
        print('login')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('valid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            print(form.errors)
            messages.error(request, "Invalid email or password.")
    form = AuthenticationForm()
    return redirect('/')


def logoutpage(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')


@login_required(login_url='login')
def createrubrics(request):
    form = RubricForm()
    if request.method == 'POST':
        form = RubricForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form = request.user
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'createrubrics.html', context)


def deleterubrics(request, pk):
    teach = get_object_or_404(Rubrics, id=pk)
    teach.delete()
    return redirect('index')


def post_detail(request, pk):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def commentlist(request):
    if request.user.is_superuser:
        comment_list = Comment.objects.filter(active=False)

        context = {'comment_list': comment_list}
        return render(request, 'commentlist.html', context)
    return HttpResponse('Impossible to go ahead!')


def updatecomment(request, pk):
    if request.user.is_superuser:
        data = get_object_or_404(Comment, id=pk)
        form = Comment_mode_Form(instance=data)

        if request.method == "POST":
            form = Comment_mode_Form(request.POST, instance=data)
            if form.is_valid():
                form.save()
                return redirect ('commentlist')
        context = {
            "form":form
        }
        return render(request, 'updatecomment.html', context)
    return HttpResponse('Imposible to ahead')


def deletecomment(pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    return redirect('index')



# During production, the domain, site name, protocol, and from email address will need to be changed.


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Account.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("/password_reset/done/")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form": password_reset_form})


def delegats(request):
    queryset = Account.objects.all()
    context = {'delegats': queryset}
    return render(request, 'delegats.html', context)


def rubrics(request):
    rubrics = Rubrics.objects.all().order_by('-id')

    context = {'rubrics': rubrics}
    return render(request, 'rubrics.html', context)


