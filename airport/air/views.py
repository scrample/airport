from os import times
from pyexpat import model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, request, HttpResponseForbidden
from django.template import context
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'air/base.html')


def client(request):
    return render(request, 'air/client.html')


class AuthenticatedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)


class ManagerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name = 'manager').exists():
            return HttpResponseForbidden()
        return super(ManagerMixin, self).dispatch(request, *args, **kwargs)


class RegisterClientView(CreateView):
    model = User
    template_name = 'air/registr.html'
    success_url = reverse_lazy('login')
    form_class = ClientRegistrationForm
    

class UserLoginView(LoginView):
    template_name = 'air/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('userprofile')
    def get_success_url(self):
        return self.success_url


class Logout(AuthenticatedMixin, LogoutView):
    next_page = reverse_lazy('home')


class ProfileListView(AuthenticatedMixin, ListView):
    model = Ticket
    template_name = 'air/userprofile.html'
    context_object_name = 'tickets'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['AvailableTickets'] = Ticket.objects.filter(available = True)
        context['SoldTickets'] = Ticket.objects.filter(available = False)
        context['ClientTickets'] = Ticket.objects.filter(buyer = self.request.user)
        """ flight = Tickets.objects.select_related('flight')
        flights = []
        for f in flight:
            flights.append({'id': f.flight.id, 'startTime': f.flight.startTime, 'Race': f.flight.Race, 'f_id': f.id})
        
        context['times'] = flights
        print(flights) """
        return context
    

class AddTicket(AuthenticatedMixin, ManagerMixin,  CreateView):
    model = Ticket
    form_class = AddTicketForm
    template_name = 'air/addticket.html'
    success_url = reverse_lazy('userprofile')


class AddFlight(AuthenticatedMixin, ManagerMixin, CreateView):
    model = Flight
    form_class = AddFlightForm
    template_name = 'air/addticket.html'
    success_url = reverse_lazy('userprofile')


class AddRace(AuthenticatedMixin, ManagerMixin, CreateView):
    model = FlightRace
    form_class = AddRaceForm
    template_name = 'air/addticket.html'
    success_url = reverse_lazy('userprofile')


class ChartView(AuthenticatedMixin, ManagerMixin, ListView):
    model = Flight
    template_name = 'air/chart.html'
    context_object_name = 'flights'
    
    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        context['counts'] = Ticket.objects.values('flight').annotate(total=Count('flight')).order_by('flight')
        #print(context['faultcount'])
        return context


class StatisticView(AuthenticatedMixin, ManagerMixin, ListView):
    model = Flight
    template_name = 'air/statistic.html'
    context_object_name = 'flights'
    
    def get_context_data(self, **kwargs):
        context = super(StatisticView, self).get_context_data(**kwargs)
        context['counts'] = Ticket.objects.filter(available = False).values('flight').annotate(total=Count('flight')).order_by('flight')
        summary = Ticket.objects.filter(available = False).values('flight').annotate(total=Count('flight')).order_by('flight')
        s = Flight.objects.all()
        prices = []
        total = []
        for i in s:
            prices.append({'id': i.id, 'Name':i.get_Name(), 'price': i.get_Price()})
            
        for i in s:
            for f in summary:
                if i.pk == f['flight']:
                    sum = i.get_Price() * f['total']
                    print(sum)
                    total.append({ 'Name':i.get_Name(), 'sum': sum})

        context['result'] = total
        """ print(summary)
        print(prices)
        print(total) """
        #print(context['faultcount'])
        print(context['result'])
        return context


class BuyTicket(AuthenticatedMixin, UpdateView):
    model = Ticket
    form_class = AddTicketForm
    template_name = 'air/buy.html'
    success_url = reverse_lazy('userprofile')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.buyer = self.request.user
        self.object.available = False
        self.object.save()
        return super().form_valid(form)


class GameView(AuthenticatedMixin, ListView):
    model = Ticket
    template_name = 'air/game.html'
    context_object_name = 'tickets'