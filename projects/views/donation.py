import json
from datetime import datetime as dt

import mercadopago
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import BadRequest
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView

from projects.forms import DonateProjectForm
from projects.models import Donation, Project

DONATIONS_PAGINATE_BY = 5

# Donations and payments using Mercado Pago.

# Mercado Pago
MERCADO_PAGO_TOKEN = settings.MERCADO_PAGO_TOKEN
MERCADO_PAGO_STATUS_API = "https://api.mercadopago.com/v1/payments/{}?access_token={}"
sdk = mercadopago.SDK(MERCADO_PAGO_TOKEN)

# Webhook Mercado Pago.


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        payment_id = data['data']['id']

        response = requests.get(
            MERCADO_PAGO_STATUS_API.format(payment_id, MERCADO_PAGO_TOKEN)
        ).json()

        try:
            donation_id = response['additional_info']['items'][0]['id']
            donation = Donation.objects.get(id=donation_id)
            donation.payment_infos = response
            donation.save()

            if (response['status'] == 'approved'):
                donation.project.collected = donation.project.collected + donation.amount
                donation.project.save()

        except Exception as e:
            pass

        return HttpResponse('Webhook received', status=200)

    else:
        raise Http404


@method_decorator(login_required, name='dispatch')
class DonateProjectView(UserPassesTestMixin, CreateView):
    model = Donation
    form_class = DonateProjectForm
    template_name = 'projects/pages/donate_project.html'

    def test_func(self):
        project = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )
        return (
            project.owner != self.request.user and
            project.is_published and
            project.deadline >= dt.now().date()
        )

    def get_success_url(self) -> str:
        return reverse("projects:donation_detail", kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )
        ctx['progress'] = round(
            (100 * ctx['project'].collected) / ctx['project'].goal)
        ctx['remaining'] = ctx['project'].goal - ctx['project'].collected

        return ctx

    def get_initial(self):
        return {
            'user': self.request.user,
            'project':  get_object_or_404(
                Project,
                slug=self.kwargs['slug'],
            )
        }

    def form_valid(self, form):
        if form.cleaned_data.get('project').slug != self.kwargs['slug'] or form.cleaned_data.get('user') != self.request.user:
            raise BadRequest('Invalid request.')

        donation = form.save()

        request_merc_pago = sdk.preference().create({
            "items": [
                {
                    "id": donation.id,
                    "title": form.cleaned_data.get('project').title,
                    "quantity": 1,
                    "unit_price": form.cleaned_data.get('amount')
                }
            ]
        })["response"]

        id_checkout = request_merc_pago['id']

        donation.id_checkout = id_checkout
        donation.save()

        self.request.session['link_checkout'] = request_merc_pago['sandbox_init_point']

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DonationDetailView(UserPassesTestMixin, DetailView):
    model = Donation
    context_object_name = 'donation'
    template_name = 'projects/pages/donation_detail.html'

    def test_func(self):
        return (
            self.request.user.is_staff or
            self.request.user == self.get_object().user or
            self.request.user == self.get_object().project.owner
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        link_checkout = self.request.session.get('link_checkout')
        if link_checkout is not None:
            del self.request.session['link_checkout']

            ctx['link_checkout'] = link_checkout
        return ctx


@method_decorator(login_required, name='dispatch')
class DonationsProjectListView(UserPassesTestMixin, ListView):
    model = Donation
    context_object_name = 'donations'
    ordering = ['-created']
    template_name = 'projects/pages/donations_project_list.html'
    paginate_by = DONATIONS_PAGINATE_BY

    def test_func(self):
        project = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )
        return (
            self.request.user.is_staff or
            self.request.user == project.owner
        )

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            project__slug=self.kwargs.get('slug'),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )
        return ctx


@method_decorator(login_required, name='dispatch')
class DonationsOwnedListView(ListView):
    model = Donation
    context_object_name = 'donations'
    ordering = ['-created']
    template_name = 'projects/pages/donations_owned_list.html'
    paginate_by = DONATIONS_PAGINATE_BY

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            user=self.request.user
        )
        return qs
