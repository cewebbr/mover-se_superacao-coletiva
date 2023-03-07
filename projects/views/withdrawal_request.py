from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import BadRequest
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from projects.filters import WithdrawalRequestListFilter
from projects.forms import (WithdrawalRequestCreateForm,
                            WithdrawalRequestReplyForm,
                            WithdrawalRequestUpdateForm)
from projects.models import Project, WithdrawalRequest

WITHDRAWAL_REQUEST_PAGINATE_BY = 5

# Withdrawal requests from project owners.


@method_decorator(login_required, name='dispatch')
class WithdrawalRequestCreateView(UserPassesTestMixin, CreateView):
    model = WithdrawalRequest
    form_class = WithdrawalRequestCreateForm
    template_name = 'projects/pages/withdrawal_request_create.html'

    def test_func(self):
        project = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )
        return (
            project.owner == self.request.user and
            project.is_withdrawal_available() and
            project.collected > 0 and
            not project.withdrawalrequest_set.all().count() > 0
        )

    def get_success_url(self) -> str:
        return reverse("projects:withdrawal_request_detail", kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )

        return ctx

    def get_initial(self):
        return {
            'user': self.request.user,
            'project': get_object_or_404(
                Project,
                slug=self.kwargs['slug'],
            ),
        }

    def form_valid(self, form):
        if form.cleaned_data.get('project').slug != self.kwargs['slug'] or form.cleaned_data.get('user') != self.request.user:
            raise BadRequest('Invalid request.')

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class WithdrawalRequestUpdateView(UserPassesTestMixin, UpdateView):
    model = WithdrawalRequest
    form_class = WithdrawalRequestUpdateForm
    context_object_name = 'w_request'
    template_name = 'projects/pages/withdrawal_request_update.html'

    def test_func(self):
        return (
            self.get_object().project.owner == self.request.user
            and not self.get_object().paid
        )

    def get_success_url(self) -> str:
        return reverse("projects:withdrawal_request_detail", kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class WithdrawalRequestReplyView(UserPassesTestMixin, UpdateView):
    model = WithdrawalRequest
    form_class = WithdrawalRequestReplyForm
    context_object_name = 'w_request'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self) -> str:
        return reverse("projects:withdrawal_request_detail", kwargs={'pk': self.object.id})

    def get(self, request, pk):
        raise Http404

    def form_invalid(self, form):
        self.request.session['reply_form'] = self.request.POST
        return redirect(reverse("projects:withdrawal_request_detail", kwargs={'pk': self.get_object().id}))


class WithdrawalRequestDetailView(UserPassesTestMixin, DetailView):
    model = WithdrawalRequest
    context_object_name = 'w_request'
    template_name = 'projects/pages/withdrawal_request_detail.html'

    def test_func(self):
        return (
            self.request.user == self.get_object().user or
            self.request.user.is_staff
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        if self.request.user.is_staff:
            form_data = self.request.session.get('reply_form')
            if form_data is not None:
                del self.request.session['reply_form']
                ctx['reply_form'] = WithdrawalRequestReplyForm(form_data)
            else:
                ctx['reply_form'] = WithdrawalRequestReplyForm(
                    initial={
                        'paid': self.get_object().paid,
                        'comments': self.get_object().comments,
                        'payment_proof': self.get_object().payment_proof,
                    }
                )

        return ctx


@method_decorator(login_required, name='dispatch')
class WithdrawalRequestListView(FilterView):
    model = WithdrawalRequest
    context_object_name = 'w_requests'
    ordering = ['-created']
    template_name = 'projects/pages/withdrawal_requests_list.html'
    paginate_by = WITHDRAWAL_REQUEST_PAGINATE_BY
    filterset_class = WithdrawalRequestListFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            user=self.request.user
        )
        return qs


@method_decorator(login_required, name='dispatch')
class WithdrawalRequestStaffListView(UserPassesTestMixin, FilterView):
    model = WithdrawalRequest
    context_object_name = 'w_requests'
    ordering = ['-created']
    template_name = 'projects/pages/withdrawal_requests_list.html'
    paginate_by = WITHDRAWAL_REQUEST_PAGINATE_BY
    filterset_class = WithdrawalRequestListFilter

    def test_func(self):
        return self.request.user.is_staff
