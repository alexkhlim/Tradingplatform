from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (WatchListViewSet,
                       UserViewSet,
                       CurrencyViewSet,
                       InventoryViewSet,
                       OfferViewSet,
                       PriceViewSet,
                       TradeViewSet,
                       ItemViewSet,
                       CreateUserView,
                       CreateWatchListView,
                       )

router = DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"currency", CurrencyViewSet)
router.register(r"item", ItemViewSet)
router.register(r"watch-list", WatchListViewSet)
router.register(r"price", PriceViewSet)
router.register(r"offer", OfferViewSet)
router.register(r"trade", TradeViewSet)
router.register(r"inventory", InventoryViewSet)

urlpatterns = [path('api/', include(router.urls)),
               path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
               path('users/register', CreateUserView.as_view()),
               path('auth/', include('djoser.urls')),
               path('auth/', include('djoser.urls.jwt')),
               path('user/', CreateWatchListView.as_view()),
               ]
