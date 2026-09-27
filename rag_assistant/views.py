from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import DocumentForm
from .models import Document
from .services import answer_question, index_document


def home(request):
    documents = Document.objects.order_by("-created_at")
    question = ""
    answer = None
    sources = []

    if request.method == "POST":
        question = request.POST.get("question", "").strip()

        if question:
            answer, sources = answer_question(question)

    return render(
        request,
        "rag_assistant/home.html",
        {
            "documents": documents,
            "question": question,
            "answer": answer,
            "sources": sources,
        },
    )


def add_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                document = form.save()
                index_document(document)

            return redirect("home")
    else:
        form = DocumentForm()

    return render(
        request,
        "rag_assistant/add_document.html",
        {"form": form},
    )


def document_detail(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    return render(
        request,
        "rag_assistant/document_detail.html",
        {"document": document},
    )


@require_POST
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()

    return redirect("home")


def health(request):
    return HttpResponse("OK", content_type="text/plain")
