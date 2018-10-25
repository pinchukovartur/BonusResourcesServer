from django.contrib import admin
from django.urls import path
from bonusmanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.index, name='index'),
    path(r'bonus_table', views.find_game_state_bonuses, name='find_game_state_bonuses'),
    path(r'add_bonus', views.add_bonus, name='add_bonus'),
    path(r'del_bonus', views.del_bonus, name='del_bonus'),
]
