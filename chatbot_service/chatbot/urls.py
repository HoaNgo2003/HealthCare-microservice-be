from django.urls import path
from .views import (
    ChatbotVer1View,
    BuildMemoryView,
    ScrapeToPDFView,
    PredictDiseaseChatbotView,
)

urlpatterns = [
    path(
        "chatbot/ver1/build-memory",
        BuildMemoryView.as_view(),
        name="chatbot-build-memory",
    ),
    path("chatbot/ver1/ask", ChatbotVer1View.as_view(), name="chatbot-ver1-chat"),
    path(
        "chatbot/ver1/scrape-to-pdf",
        ScrapeToPDFView.as_view(),
        name="chatbot-scrape-to-pdf",
    ),
    path(
        "chatbot/ver2/ask",
        PredictDiseaseChatbotView.as_view(),
        name="chatbot-ver2-chat",
    ),
]
