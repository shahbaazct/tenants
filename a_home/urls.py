from django.urls import path
from . import views

# URL patterns for task-related APIs
urlpatterns = [
	# URL for retrieving a list of items (optional filtering by assignee_id)
	path("item-list/", views.ItemListView.as_view(), name="item-summary"), 
	# URL for creating a new item or updating an existing task
	path("item-view/", views.ItemView.as_view(), name="item-view"),
	# URL for retrieving details of a specific item based on its item_id
	path(
	"ticket-detail/",
	views.ItemDetailView.as_view(),
	name="item-detail",
	),
    
]