from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from . import models, forms


class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'task_create.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    template_name = 'task_detail.html'


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Task
    template_name = 'task_update.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')
