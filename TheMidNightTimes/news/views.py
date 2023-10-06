from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.http import HttpResponse, JsonResponse
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Search, SearchResults


class UserLogin(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/search')

        else:
            messages.error(request, 'Login Failed. Incorect Credentials.')
            return render(request, 'login.html')


# @login_required
class SearchAPI(View):
    def get(self, request):
        return render(request, 'search.html')

    def post(self, request):
        user = request.user
        search_keyword = request.POST['search']
        from_param = datetime.now() - timedelta(days=1)
        search_history = Search.objects.filter(user=user, keyword=search_keyword)

        if search_history:
            search_id = search_history.first().id
            search_result = (SearchResults.objects.filter(user=request.user, search_id=search_id).order_by
                             ('-date_published'))
            data = serializers.serialize('json', search_result)
            return HttpResponse(data, content_type='application/json')

        newsapi = NewsApiClient(api_key='490b2374231d45a6afe10c9774d87e1c')
        all_articles = newsapi.get_everything(q=search_keyword,
                                              from_param=from_param.date(),
                                              sort_by='relevancy',
                                              page=2)

        if all_articles is not None:
            search = Search.objects.create(user=user, keyword=search_keyword, created_at=datetime.now())

            for article in all_articles["articles"]:
                SearchResults.objects.create(
                    user=user,
                    search=search,
                    name=article["source"]["name"],
                    author=article["author"],
                    title=article["title"],
                    description=article["description"],
                    date_published=article["publishedAt"]
                )
            messages.success(request, "Search history saved successfully.")

            return JsonResponse(all_articles)
        messages.success(request, "No result found for your search.")
        return render(request, 'search.html')


class SearchResult(View):

    def get(self, request):
        search_result = SearchResults.objects.filter(user=request.user).order_by('-date_published')
        data = serializers.serialize('json', search_result)
        return HttpResponse(data, content_type='application/json')


class RefreshSearchResul(View):
    def get(self, request, search_id):
        search = Search.objects.filter(search_id=search_id)
        if search:
            last_update_date = search.created_at
            trigger_date = datetime.now() - timedelta(hours=24)


