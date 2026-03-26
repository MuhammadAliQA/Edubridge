from __future__ import annotations

from django.shortcuts import render


def csrf_failure(request, reason: str = ""):
    return render(
        request,
        "csrf_failure.html",
        {"reason": reason},
        status=403,
    )

