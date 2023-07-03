from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('userprofile/', ProfileListView.as_view(), name='userprofile'),
    path('registr', RegisterClientView.as_view(), name='registr'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('addticket', AddTicket.as_view(), name='addticket'),
    path('addflight', AddFlight.as_view(), name='addflight'),
    path('addrace', AddRace.as_view(), name='addrace'),
    path('chart', ChartView.as_view(), name='chart'),
    path('statistic', StatisticView.as_view(), name='statistic'),
    path('buy/<int:pk>', BuyTicket.as_view(), name='buy'),
    path('game', GameView.as_view(), name='game'),
]