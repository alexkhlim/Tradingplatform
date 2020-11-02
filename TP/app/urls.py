from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter()
router.register(r"user", UserListCreateView)
router.register(r"user", UserDetailUpdateView)
router.register(r"currency", CurrencyListCreateView)
router.register(r"currency", CurrencyDetailUpdate)
router.register(r"item", ItemCreateListView)
router.register(r"item", ItemDetail)
router.register(r"watch-list", WatchListCreateListView)
router.register(r"watch-list", WatchListDetailUpdate)
router.register(r"offer", OfferListCreateView)

urlpatterns = [path('api/', include(router.urls)),
               path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
               path('auth/', include('djoser.urls')),
               path('auth/', include('djoser.urls.jwt')),
               ]
