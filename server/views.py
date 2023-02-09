from django.shortcuts import render, redirect, reverse
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
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


class NewsListView(generic.ListView):
    template_name = 'indexActive.html'
    model = Voting
    queryset = News.objects.all()
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['register_form'] = UserRegisterForm
        print(context['register_form'])
        print('orin')
        context['login_form'] = AuthenticationForm
        return context


class VotingDetailView(generic.DetailView):
    template_name = 'index.html'
    model = Voting
    context_object_name = 'voting'


@login_required(login_url='login')
def vote_question(request):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    for i in question.voting.questions_vote.all():
        if request.user in i.users.all():
            question.users.remove(request.user)
            break

    else:
        question.users.add(request.user)
    return redirect(reverse('chat_detail', args=[str(question.voting.chat.id)]))


@login_required()
def create_news_voting(request, pk):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        das = form.save(commit=False)
        das.voting = get_object_or_404(Voting, id=pk)
        a = das.save()
        return redirect(das.get_absolute_url())
    form = NewsForm
    return render(request, 'create_news.html', {'form': form})


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'post1.html'
    context_object_name = 'news'




def chat_detail(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    messages = Message.objects.filter(chat=chat)
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})


def chat_list(request):
    chats = Chat.objects.filter(users__id__exact=request.user.id)
    return render(request, 'chats.html', {'chats': chats})


def security(request):
    return render(request, 'security.html')


def profile(request, pk):
    account = get_object_or_404(Account, id=pk)
    return render(request, 'profile.html', {'account': account})


def delegats(request):
    users = Account.objects.all()
    return render(request, 'delegats.html', {'users': users})


def settings(request):
    return render(request, 'settings.html')



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
                    return render(request, 'message_send.html')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="resetPassword.html", context={"password_reset_form": password_reset_form})
