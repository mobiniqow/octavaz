from django.urls import path
from .views import TicketListView, TicketDetailView, TicketCategoryView
# TicketResponseView,

urlpatterns = [
    path('api/v1/tickets/', TicketListView.as_view(), name='ticket_list'),
    path('api/v1/category/', TicketCategoryView.as_view(), name='categories'),
    path('api/v1/ticket/<int:ticket_id>/', TicketDetailView.as_view(), name='ticket_detail'),
    # path('api/v1/ticket/<int:ticket_id>/response/', TicketResponseView.as_view(), name='ticket_response'),
]
