from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, LogoutView, AddApplication, ApplicationUserList, ApplicationAdminList,\
    DashboardPlan, AddPlan, AcceptApplication, EditPlan, DeletePlan, ExportItem, DeclineApplication
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('admin/', admin.site.urls, name="admin"),
    path('export', ExportItem.as_view(), name='export'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard-plan/', DashboardPlan.as_view(), name='dashboard-plan'),
    path('application-user-list/',ApplicationUserList.as_view(), name='application-user-list'),
    path('application-admin-list/', ApplicationAdminList.as_view(), name='application-admin-list'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('add-plan/', AddPlan.as_view(), name='add-plan'),
    path('accept-application/<int:pk>', AcceptApplication.as_view(), name='accept-application'),
    path('decline-application/<int:pk>', DeclineApplication.as_view(), name='decline-application'),
    path('add-application/', AddApplication.as_view(), name='add-application'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('edit-plan/<int:pk>', EditPlan.as_view(), name='edit-plan'),
    path('delete-plan/<int:pk>', DeletePlan.as_view(), name='delete-plan'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]