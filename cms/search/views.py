from cms.atlascasestudies.models import AtlasCaseStudy
from cms.publications.models import Publication
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.core.models import Page
from wagtail.search.models import Query

from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.pages.models import BasePage


def search(request):
    """
    sample query
    ?
    query=nursing&
    order=pub_date_asc&
    content_type=pages&
    date_from=2020-11-01&
    date_to=2020-11-29
    """

    query = request.GET.get("query", None)
    search_ordering = request.GET.get("order", "-latest_revision_created_at")
    search_type = request.GET.get("content_type", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    page = request.GET.get("page", 1)
    search_results_count = None
    search_type = request.GET.get("content_type", "")

    def search(_class):
        queryset = _class.objects.live().order_by(search_ordering)
        if date_from and date_to:
            queryset = queryset.filter(
                latest_revision_created_at__range=[
                    date_from,
                    date_to,
                ]
            )
        return queryset.search(query)

    # Search
    if query:
        if search_type == "news":
            search_results = search(Post)
        elif search_type == "blogs":
            search_results = search(Blog)
        elif search_type == "pages":
            search_results = search(BasePage)
        elif search_type == "publications":
            search_results = search(Publication)
        else:
            search_results = search(Page)

        search_results_count = search_results.count()

        query = Query.get(query)
        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    search_params = "&query={}&order={}&content_type={}&date_from={}&date_to={}".format(
        query, search_ordering, search_type, date_from, date_to
    )

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "query": query,
            "search_results": search_results,
            "results_count": search_results_count,
            "page": page,
            "search_params": search_params,
            "content_type": search_type,
            "order": search_ordering,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
