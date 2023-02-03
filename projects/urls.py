from django.urls import path

from projects import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectsListView.as_view(), name="projects_list"),
    path("owned-projects/", views.ProjectsOwnedListView.as_view(),
         name="projects_owned"),
    path("review/", views.ProjectsReviewListView.as_view(),
         name="projects_review_list"),
    path("create-project/", views.ProjetCreateView.as_view(), name="project_create"),
    path("delete-project/<slug:slug>/",
         views.ProjectDeleteView.as_view(), name="project_delete"),
    path("update-project/<slug:slug>/",
         views.ProjectUpdateView.as_view(), name="project_update"),
    path("details/<slug:slug>/",
         views.ProjectDetailView.as_view(), name="project_detail"),
    path("reprove/<slug:slug>/",
         views.ReviewProjectView.as_view(), name="project_review"),

    path("withdrawal-request/create/<slug:slug>/",
         views.WithdrawalRequestCreateView.as_view(), name="withdrawal_request_create"),
    path("withdrawal-request/update/<int:pk>/",
         views.WithdrawalRequestUpdateView.as_view(), name="withdrawal_request_update"),
    path("withdrawal-request/reply/<int:pk>/",
         views.WithdrawalRequestReplyView.as_view(), name="withdrawal_request_reply"),
    path("withdrawal-requests/", views.WithdrawalRequestListView.as_view(),
         name="withdrawal_requests_list"),
    path("withdrawal-requests/staff/", views.WithdrawalRequestStaffListView.as_view(),
         name="withdrawal_requests_staff_list"),
    path("withdrawal-request/details/<int:pk>/",
         views.WithdrawalRequestDetailView.as_view(), name="withdrawal_request_detail"),

    path("project-donations/<slug:slug>", views.DonationsProjectListView.as_view(),
         name="donations_project"),
    path("owned-donations/", views.DonationsOwnedListView.as_view(),
         name="donations_owned"),
    path("donate-project/<slug:slug>/",
         views.DonateProjectView.as_view(), name="donate_project"),
    path("donation/details/<int:pk>/",
         views.DonationDetailView.as_view(), name="donation_detail"),

    path("donation/webhook/", views.webhook, name="donation_webhook"),
]
