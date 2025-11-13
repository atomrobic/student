from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import Student, SupportDocument
from .forms import StudentForm


# ----------------------------
# Admin Authentication Views
# ----------------------------
class AdminLoginView(View):
    template_name = 'students_app/admin_login.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('student_list')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('student_list')
        messages.error(request, "Invalid credentials or not staff.")
        return render(request, self.template_name)





# ----------------------------
# Student Views
# ----------------------------
@method_decorator(staff_member_required(login_url='admin_login'), name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'students_app/student_list.html'
    context_object_name = 'students'


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students_app/student_form.html'

    def form_valid(self, form):
        student = form.save()

        # Save uploaded documents
        files = self.request.FILES.getlist('documents')
        for f in files:
            SupportDocument.objects.create(student=student, document=f)

        return redirect('student_detail', pk=student.pk)


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students_app/student_form.html'

    def form_valid(self, form):
        student = form.save()

        # Save any newly uploaded documents
        files = self.request.FILES.getlist('documents')
        for f in files:
            SupportDocument.objects.create(student=student, document=f)

        return redirect('student_detail', pk=student.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass existing documents to template
        context['existing_documents'] = self.object.documents.all()
        return context


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student_add')
    template_name = 'students_app/student_from'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'students_app/student_detail.html'
    context_object_name = 'student'
