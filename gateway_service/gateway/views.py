import httpx
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

SERVICE_MAP = {
    "auth": "http://localhost:8000",
    "appointment": "http://localhost:8002",
    "medical": "http://localhost:8003",
    "pharmacist": "http://localhost:8004",
    "chatbot": "http://localhost:8005",
}


@csrf_exempt
def proxy_view(request, service, path):
    if service not in SERVICE_MAP:
        return JsonResponse({"error": "Service not found"}, status=404)

    url = f"{SERVICE_MAP[service]}/{path}"

    # Lọc các headers hợp lệ (bỏ Content-Length, Host,...)
    headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in ["host", "content-length"]
    }

    try:
        # Gửi request với đúng method + body
        with httpx.Client() as client:
            response = client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=request.body,  # body cần giữ nguyên
                timeout=10.0
            )

        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("content-type", "application/json")
        )

    except httpx.RequestError as e:
        return JsonResponse({"error": str(e)}, status=502)
