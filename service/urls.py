from django.urls import path
from .views import (ProjectCreateView,ProjectUpdateView,ProjectDeleteView,MyProjectsView,ProjectDetailView,BidCreateView,FreelancerBidListView,BidDetailView,ProjectsView,ProjectBidListView,ClientBidListView, AcceptBidView,RejectBidView,ContractListView,ContractDetailView,FinishContractView,ReviewCreateView)

urlpatterns = [
    path("projects/create/", ProjectCreateView.as_view()),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view()),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view()),
    path("my-projects/", MyProjectsView.as_view()),
    path("projects/<int:pk>/", ProjectDetailView.as_view()),
    path("projects/", ProjectsView.as_view()),
    path("projects/<int:pk>/bid/", BidCreateView.as_view()),
    path("my-bids/", FreelancerBidListView.as_view()),
    path("bids/<int:pk>/", BidDetailView.as_view()),
    path("projects/<int:project_id>/bids/", ProjectBidListView.as_view()),
    path("client/bids/", ClientBidListView.as_view()),
    path("bids/<int:bid_id>/accept/", AcceptBidView.as_view()),
    path("bids/<int:bid_id>/reject/", RejectBidView.as_view()),
    path("contracts/", ContractListView.as_view()),
    path("contracts/<int:contract_id>/", ContractDetailView.as_view()),
    path("contracts/<int:contract_id>/finish/", FinishContractView.as_view()),
    path("contracts/<int:contract_id>/review/", ReviewCreateView.as_view()),

]