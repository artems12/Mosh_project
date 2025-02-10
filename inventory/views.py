from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, ApplicationForm, PlanForm
from .models import InventoryItem, Category, ApplicationItem, PlanItem
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.contrib.auth import logout
import datetime
import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import make_naive

class Index(TemplateView):
	template_name = 'inventory/index.html'

class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'inventory/logout.html')
class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.all().order_by('id')

		return render(request, 'inventory/dashboard.html', {'items': items})

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context


class ApplicationUserList(LoginRequiredMixin, View):
	def get(self, request):
		applications = ApplicationItem.objects.filter(user=self.request.user.id).order_by('id')
		return render(request, 'inventory/application_user_list.html', {'applications': applications})

class ApplicationAdminList(LoginRequiredMixin, View):
	def get(self, request):
		applications = ApplicationItem.objects.all().order_by('id')
		return render(request, 'inventory/application_admin_list.html', {'applications': applications})

class AddApplication(LoginRequiredMixin, CreateView):
	model = ApplicationItem
	form_class = ApplicationForm
	template_name = 'inventory/application_form.html'
	success_url = reverse_lazy('application-user-list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class ExportItem(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		data = InventoryItem.objects.all().values()
		df = pd.DataFrame(data)
		# Преобразование временных меток в timezone-unaware
		for column in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]']).columns:
			df[column] = df[column].apply(lambda x: make_naive(x) if x is not None else x)
		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
		df.to_excel(response, index=False)
		return response

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

class AcceptApplication(LoginRequiredMixin, DeleteView):
	model = ApplicationItem
	template_name = 'inventory/accept_application.html'
	success_url = reverse_lazy('application-admin-list')
	context_object_name = 'application'
	def post(self,request,pk):
		ob = ApplicationItem.objects.all().get(id=pk)
		new_object = PlanItem.objects.create(name=ob.name,quantity=ob.quantity,category=ob.category,user=ob.user)
		ob.delete()
		return redirect('application-admin-list')

class DeclineApplication(LoginRequiredMixin, DeleteView):
	model = ApplicationItem
	template_name = 'inventory/decline_application.html'
	success_url = reverse_lazy('application-admin-list')
	context_object_name = 'application'


class DashboardPlan(LoginRequiredMixin, View):
	def get(self, request):
		plans = PlanItem.objects.all().order_by('id')
		return render(request, 'inventory/plan_dashboard.html', {'plans': plans})

class AddPlan(LoginRequiredMixin, CreateView):
	model = PlanItem
	form_class = PlanForm
	template_name = 'inventory/plan_form.html'
	success_url = reverse_lazy('dashboard-plan')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

class EditPlan(LoginRequiredMixin, UpdateView):
	model = PlanItem
	form_class = PlanForm
	template_name = 'inventory/plan_form.html'
	success_url = reverse_lazy('dashboard-plan')

class DeletePlan(LoginRequiredMixin, DeleteView):
	model = PlanItem
	template_name = 'inventory/delete_plan.html'
	success_url = reverse_lazy('dashboard-plan')
	context_object_name = 'plan'
