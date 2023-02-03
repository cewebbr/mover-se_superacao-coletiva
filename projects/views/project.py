import datetime
from datetime import datetime as dt

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  UpdateView)
from django_filters.views import FilterView

from projects.filters import (ProjectListFilter, ProjectReviewListFilter,
                              ProjectsOwnedListFilter)
from projects.forms import (ProjectCreateForm, ProjectReviewForm,
                            ProjectUpdateForm)
from projects.models import Project
from topics.forms import TopicCreateForm

PROJECTS_PAGINATE_BY = 5
TOPICS_PAGINATE_BY = 5


def generate_project_slug(project):
    project.slug = f'{slugify(project.title)}'
    projects_same_slug = Project.objects.filter(
        slug=project.slug
    )
    if len(projects_same_slug) > 0:
        project.slug = "temp"
        project.save()
        project.slug = "{}_{}".format(
            f'{slugify(project.title)}', project.id)

    project.save()

    return project


@method_decorator(login_required, name='dispatch')
class ProjetCreateView(CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/pages/project_create.html'

    def get_success_url(self) -> str:
        return reverse("projects:project_detail", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user

        self.object = generate_project_slug(self.object)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'projects/pages/project_update.html'
    form_class = ProjectUpdateForm

    def test_func(self):
        return (
            self.request.user == self.get_object().owner and
            self.get_object().is_published == False
        )

    def get_success_url(self):
        return reverse("projects:project_detail", kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.request.user == self.object.owner and not self.object.is_published:
            self.object.is_reproved = False
            self.object.reproval_reason = ""
            self.object = generate_project_slug(self.object)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/pages/project_delete.html'

    def test_func(self):
        return (
            self.request.user == self.get_object().owner and
            self.get_object().is_published == False
        )

    def get_success_url(self) -> str:
        return reverse("projects:projects_owned")


class ProjectDetailView(UserPassesTestMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/pages/project_detail.html'
    paginate_by = TOPICS_PAGINATE_BY

    def test_func(self):
        return (
            self.request.user == self.get_object().owner or
            self.request.user.is_staff or
            self.get_object().is_published == True
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        project = self.get_object()
        ctx['is_finished'] = dt.now().date() > project.deadline
        ctx['progress'] = round(
            (100 * project.collected) / project.goal)

        form_data = self.request.session.get('form')
        if form_data is not None:
            del self.request.session['form']
        if self.request.user.is_authenticated:
            if form_data is not None:
                ctx['form'] = TopicCreateForm(form_data)
            else:
                ctx['form'] = TopicCreateForm(initial={
                    'user': self.request.user,
                    'project': project,
                })

            ctx['is_withdrawal_available'] = project.is_withdrawal_available()

            if not ctx['is_withdrawal_available']:
                ctx['withdrawal_available_date'] = (
                    project.deadline +
                    datetime.timedelta(
                        days=settings.DAYS_FOR_WITHDRAWAL_REQUEST)
                )
                ctx['DAYS_FOR_WITHDRAWAL_REQUEST'] = settings.DAYS_FOR_WITHDRAWAL_REQUEST

        if self.request.user.is_staff and not project.is_published:
            ctx['approve_form'] = ProjectReviewForm(initial={
                'project':  project,
                'approve': True,
            })

        topics = project.topic_set.all().order_by('-created')
        paginator = Paginator(topics, self.paginate_by)
        page = self.request.GET.get('page')
        ctx['topics'] = paginator.get_page(page)

        ctx['page_obj'] = ctx['topics']
        ctx['paginator'] = ctx['topics'].paginator
        ctx['is_paginated'] = ctx['paginator'].num_pages > 1

        return ctx


class ProjectsListView(FilterView):
    model = Project
    context_object_name = 'projects'
    ordering = ['-created']
    template_name = 'projects/pages/project_list.html'
    paginate_by = PROJECTS_PAGINATE_BY
    filterset_class = ProjectListFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        return qs


@method_decorator(login_required, name='dispatch')
class ProjectsOwnedListView(FilterView):
    model = Project
    context_object_name = 'projects'
    ordering = ['-created']
    template_name = 'projects/pages/projects_owned_list.html'
    paginate_by = PROJECTS_PAGINATE_BY
    filterset_class = ProjectsOwnedListFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            owner=self.request.user
        )
        return qs


@method_decorator(login_required, name='dispatch')
class ProjectsReviewListView(UserPassesTestMixin, FilterView):
    model = Project
    context_object_name = 'projects'
    ordering = ['-created']
    template_name = 'projects/pages/projects_review_list.html'
    paginate_by = PROJECTS_PAGINATE_BY
    filterset_class = ProjectReviewListFilter

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=False,
        )
        return qs


@method_decorator(login_required, name='dispatch')
class ReviewProjectView(UserPassesTestMixin, FormView):
    form_class = ProjectReviewForm
    template_name = 'projects/pages/project_reprove.html'

    def test_func(self):
        project = get_object_or_404(
            Project,
            slug=self.kwargs['slug']
        )
        return (
            self.request.user.is_staff and
            not project.is_published
        )

    def get_initial(self):
        project = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )
        return {
            'project':  project,
            'reproval_reason': project.reproval_reason,
            'approve': False,
        }

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['project'] = get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
        )

        return ctx

    def form_valid(self, form):
        project = form.cleaned_data.get('project')
        approve = form.cleaned_data.get('approve')
        reproval_reason = form.cleaned_data.get('reproval_reason')

        if approve:
            if dt.now().date() > project.deadline:
                messages.error(
                    self.request, f"Erro ao aprovar o projeto! O projeto \"{project.title}\" já foi encerrado.")
            else:
                project.is_reproved = False
                project.reproval_reason = ""
                project.is_published = True
                messages.success(
                    self.request, f"O projeto \"{project.title}\" foi aprovado.")
        else:
            if not project.is_reproved:
                messages.error(
                    self.request, f"O projeto \"{project.title}\" foi reprovado.")
            elif project.reproval_reason != reproval_reason:
                messages.error(
                    self.request, f"O motivo da reprovação do projeto \"{project.title}\" foi atualizado.")

            project.is_reproved = True
            project.reproval_reason = reproval_reason

        project.save()

        self.success_url = reverse(
            "projects:project_detail",
            kwargs={
                'slug': project.slug
            }
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
