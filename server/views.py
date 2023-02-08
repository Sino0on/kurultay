from django.shortcuts import render, redirect, reverse
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class NewsListView(generic.ListView):
    template_name = 'indexActive.html'
    model = Voting
    queryset = News.objects.all()
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        def get_context_data(self, *, object_list=None, **kwargs):
            context = super(NewsDetailView, self).get_context_data(**kwargs)
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
