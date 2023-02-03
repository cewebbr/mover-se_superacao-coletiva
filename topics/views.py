from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import BadRequest
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, View
from django_filters.views import FilterView

from topics.filters import MessageOrderByFilter
from topics.forms import MessageCreateForm, TopicCreateForm
from topics.models import Message, MessageVote, Topic

MESSAGES_PAGINATE_BY = 5


@method_decorator(login_required, name='dispatch')
class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicCreateForm

    def get_success_url(self) -> str:
        return reverse("topics:topic_detail", kwargs={'pk_topic': self.object.id})

    def get(self, request):
        raise Http404

    def form_valid(self, form):
        if form.cleaned_data.get('user') != self.request.user:
            raise BadRequest('Invalid request.')

        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session['form'] = self.request.POST
        return redirect(reverse("projects:project_detail", kwargs={'slug': form.cleaned_data['project'].slug}))


@method_decorator(login_required, name='dispatch')
class TopicDeleteView(UserPassesTestMixin, DeleteView):
    model = Topic
    template_name = 'topics/pages/topic_delete.html'

    def test_func(self):
        return (
            self.request.user.is_staff or
            self.request.user == self.get_object().user or
            self.request.user == self.get_object().project.owner
        )

    def get_success_url(self) -> str:
        return reverse("projects:project_detail", kwargs={'slug': self.get_object().project.slug})


class TopicView(FilterView):
    model = Message
    context_object_name = 'msgs'
    ordering = ['-created']
    template_name = 'topics/pages/topic.html'
    paginate_by = MESSAGES_PAGINATE_BY
    filterset_class = MessageOrderByFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(
            topic__pk=self.kwargs['pk_topic'],
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx['topic'] = get_object_or_404(
            Topic,
            pk=self.kwargs['pk_topic'],
        )

        for message in ctx['msgs']:
            message.upvotes = message.messagevote_set.filter(
                value=True).count()
            message.downvotes = message.messagevote_set.filter(
                value=False).count()

            if self.request.user.is_authenticated:
                try:
                    message.vote = message.messagevote_set.get(
                        user=self.request.user)
                except:
                    pass

        form_data = self.request.session.get('message_form')
        if form_data is not None:
            ctx['message_form'] = MessageCreateForm(form_data)
            del self.request.session['message_form']
        else:
            ctx['message_form'] = MessageCreateForm(
                initial={
                    'user': self.request.user,
                    'topic': ctx['topic'],
                })

        return ctx


@method_decorator(login_required, name='dispatch')
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm

    def get_success_url(self) -> str:
        return reverse("topics:topic_detail", kwargs={'pk_topic': self.object.topic.id})

    def get(self, request):
        raise Http404

    def form_valid(self, form):
        if form.cleaned_data.get('user') != self.request.user:
            raise BadRequest('Invalid request.')

        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session['message_form'] = self.request.POST
        return redirect(reverse("topics:topic_detail", kwargs={'pk_topic': form.cleaned_data['topic'].id}))


@method_decorator(login_required, name='dispatch')
class VoteMessageView(UserPassesTestMixin, View):

    def test_func(self):
        message_id = self.request.POST['message']
        user = self.request.POST['user']

        try:
            Message.objects.get(pk=message_id)
        except:
            return False

        return str(self.request.user.id) == user

    def post(self, request, *args, **kwargs):
        message_id = self.request.POST['message']
        value = request.POST['value']

        message = Message.objects.get(pk=message_id)

        vote = None
        try:
            vote = MessageVote.objects.get(
                user=self.request.user,
                message=message,
            )
        except:
            vote = MessageVote()
            vote.user = self.request.user
            vote.message = message
            vote.value = None

        if value == "True":
            if vote.value == True:
                vote.delete()
            else:
                vote.value = True
                vote.save()

        elif value == "False":
            if vote.value == False:
                vote.delete()
            else:
                vote.value = False
                vote.save()

        next_url = request.POST.get(
            'next',
            reverse('topics:topic_detail', kwargs={
                'pk_topic': message.topic.id,
            })
        )

        return HttpResponseRedirect(next_url)
