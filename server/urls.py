from django.urls import path
from .views import *


urlpatterns = [
    path('', NewsListView.as_view(), name='home'),
    path('voting/detail/<int:pk>', VotingDetailView.as_view(), name='voting_detail'),
    path('vote/', vote_question, name='question_vote'),
    path('create/news/<int:pk>', create_news_voting, name='create_news'),
    path('detail/news/<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('chat/<int:pk>', chat_detail, name='chat_detail'),
    path('chats/', chat_list, name='chats'),
    path('security/', security, name='security'),

]
