from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *
from app.views import GeneratePDF

router = DefaultRouter()
router.register(r'user', UserView)
router.register(r"currency", CurrencyView)
router.register(r"item", ItemView)
router.register(r"watch-list", WatchListView)
router.register(r"offer", OfferView)
router.register(r"inventory", InventoryViewSet)
router.register(r'statisticsitem', SatisticsItemView)
router.register(r'userinventory', UserInventoryView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('table/', GeneratePDF.as_view()),
]
