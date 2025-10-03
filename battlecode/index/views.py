from django.http import HttpRequest
from django.shortcuts import render

from battlecode.pagedata import PageData


current_page = "index"


def index(request: HttpRequest):
    pd = PageData(
        title="Index",
        description="Index page",
        curr_page=current_page,
    )
    return render(request, "index.html", context={"pd": pd})
