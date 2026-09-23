from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('tickets/', views.tickets_view, name='tickets'),
    path('create-ticket/', views.create_ticket_view, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('einstellungen/', views.einstellungen_view, name='einstellungen'),
]