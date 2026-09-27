from django.contrib import admin
from django.urls import path

from rag_assistant import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("knowledge/add/", views.add_document, name="add_document"),
    path(
        "knowledge/<int:document_id>/",
        views.document_detail,
        name="document_detail",
    ),
    path(
        "knowledge/<int:document_id>/delete/",
        views.delete_document,
        name="delete_document",
    ),
    path("health/", views.health, name="health"),
]
