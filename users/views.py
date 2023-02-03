from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView

from users.forms import UserChangeForm
from users.models import User


@method_decorator(login_required, name='dispatch')
class UserChange(UpdateView):
    model = User
    template_name = 'users/pages/user_update.html'
    form_class = UserChangeForm

    def get_success_url(self) -> str:
        return reverse("users:user_profile", kwargs={'pk': self.get_object().id})

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.request.user.id == self.object.id:
            self.object.save()
            messages.success(
                self.request, 'Suas alterações foram salvas com sucesso.')
        return super().form_valid(form)


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user_profile'
    template_name = 'users/pages/user_profile.html'
