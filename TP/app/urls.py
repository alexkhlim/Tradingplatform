from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter()
router.register(r"user", UserListCreateDetailUpdateView)
router.register(r"currency", CurrencyListCreateView)
router.register(r"item", ItemCreateListDetailView)
router.register(r"watch-list", WatchListCreateListDetailUpdateView)
router.register(r"offer", OfferListCreateView)

urlpatterns = [path('api/', include(router.urls)),
               path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
               path('auth/', include('djoser.urls')),
               path('auth/', include('djoser.urls.jwt')),
               ]
