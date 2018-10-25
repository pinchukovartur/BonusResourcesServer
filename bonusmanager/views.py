import json
import time
from django.shortcuts import render, redirect

from .constant import local_server_url

import requests


def index(request):
    if not request.user.is_authenticated:
        return redirect('/admin')

    return render(request, 'bonusmanager/index.html', {})


def find_game_state_bonuses(request):
    if not request.user.is_authenticated:
        return redirect('/admin')

    if request.method != "POST":
        return render(request, 'bonusmanager/index.html', {})

    if not "game_state_id" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "game state id param can't be null!"})

    if not request.POST["game_state_id"]:
        return render(request, 'bonusmanager/index.html', {"error": "game state id can't be null!"})

    game_state_id = request.POST["game_state_id"]
    r = requests.get(local_server_url + "get_bonus_resource?game_state_id=" + game_state_id + "&all_bonuses=true")

    response = json.loads(r.text)

    if response["complete"] != "complete":
        return render(request, 'bonusmanager/bonus_table.html', {})

    return render(request, 'bonusmanager/bonus_table.html', {"resources": response["resources"],
                                                             "game_state_id": game_state_id})


def add_bonus(request):
    if not request.user.is_authenticated:
        return redirect('/admin')

    if request.method != "POST":
        return render(request, 'bonusmanager/index.html', {})

    if not "game_state_id" in request.POST.keys() or not "count" in request.POST.keys() or not "type_bonus" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    if not request.POST["game_state_id"] or not request.POST["count"] or not request.POST["type_bonus"]:
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    game_state_id = request.POST["game_state_id"]
    count = request.POST["count"]
    type_bonus = request.POST["type_bonus"]

    requests.get(local_server_url + "save_bonus_resource?game_state_id=" + game_state_id +
                 "&bonus_resources_type=" + type_bonus + "&bonus_resources_count=" + count)
    time.sleep(1)
    return find_game_state_bonuses(request)


def del_bonus(request):
    if not request.user.is_authenticated:
        return redirect('/admin')

    if request.method != "POST":
        return render(request, 'bonusmanager/index.html', {})

    if not "game_state_id" in request.POST.keys() or not "create_at" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    if not request.POST["game_state_id"] or not request.POST["create_at"]:
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    game_state_id = request.POST["game_state_id"]
    create_at = request.POST["create_at"]

    requests.get(local_server_url + "del_bonus_resource?game_state_id=" + game_state_id +
                 "&create_at_bonus=" + create_at)
    time.sleep(1)
    return find_game_state_bonuses(request)