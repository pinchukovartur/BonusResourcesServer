import json
import time
from django.shortcuts import render, redirect

from .constant import local_server_url, server_prod_url, server_dev_url, server_key

import requests


def index(request):
    if not request.user.is_authenticated:
        return redirect('/admin')

    return render(request, 'bonusmanager/index.html', {})


def find_game_state_bonuses(request):
    """
    find  player bonus state by PlayerID on the server
    if game state is not find, that we are not added bonuses for this player
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('/admin')

    if request.method != "POST":
        return render(request, 'bonusmanager/index.html', {})

    if not "game_state_id" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "game state id param can't be null!"})

    if not request.POST["game_state_id"]:
        return render(request, 'bonusmanager/index.html', {"error": "game state id can't be null!"})

    if not "server" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "server param can't be null!"})

    if not request.POST["server"]:
        return render(request, 'bonusmanager/index.html', {"error": "server can't be null!"})

    server_url = local_server_url
    if request.POST["server"] == "prod":
        server_url = server_prod_url
    elif request.POST["server"] == "dev":
        server_url = server_dev_url

    game_state_id = request.POST["game_state_id"]
    r = requests.get(server_url + "get_bonus_resource?game_state_id=" + game_state_id + "&all_bonuses=true&key=" + server_key)

    print(r.text)
    print()
    print()
    print()
    print()
    response = json.loads(str(r.text))

    if "error" in response.keys():
        return render(request, 'bonusmanager/index.html', {"error": response["error"]})

    if response["complete"] != "complete":
        return render(request, 'bonusmanager/bonus_table.html', {"game_state_id": game_state_id,
                                                                 "server": request.POST["server"]})

    return render(request, 'bonusmanager/bonus_table.html', {"resources": response["resources"],
                                                             "game_state_id": game_state_id,
                                                             "server": request.POST["server"]})


def add_bonus(request):
    """
    Create state and add bonuses for player by  ID
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('/admin')

    if request.method != "POST":
        return render(request, 'bonusmanager/index.html', {})

    if not "game_state_id" in request.POST.keys() or not "count" in request.POST.keys() or not "type_bonus" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    if not request.POST["game_state_id"] or not request.POST["count"] or not request.POST["type_bonus"]:
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    if not "server" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "server param can't be null!"})

    if not request.POST["server"]:
        return render(request, 'bonusmanager/index.html', {"error": "server can't be null!"})

    server_url = local_server_url
    if request.POST["server"] == "prod":
        server_url = server_prod_url
    elif request.POST["server"] == "dev":
        server_url = server_dev_url

    game_state_id = request.POST["game_state_id"]
    count = request.POST["count"]
    type_bonus = request.POST["type_bonus"]

    requests.get(server_url + "save_bonus_resource?game_state_id=" + game_state_id +
                 "&bonus_resources_type=" + type_bonus + "&bonus_resources_count=" + count + "&key=" + server_key)
    time.sleep(1)
    return find_game_state_bonuses(request)


def del_bonus(request):
    """
    Remove player state  from server
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('/admin')

    if request.method != "POST":
        return render(request, 'bonusmanager/index.html', {})

    if not "game_state_id" in request.POST.keys() or not "create_at" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    if not request.POST["game_state_id"] or not request.POST["create_at"]:
        return render(request, 'bonusmanager/index.html', {"error": "param can't be null!"})

    if not "server" in request.POST.keys():
        return render(request, 'bonusmanager/index.html', {"error": "server param can't be null!"})

    if not request.POST["server"]:
        return render(request, 'bonusmanager/index.html', {"error": "server can't be null!"})

    server_url = local_server_url
    if request.POST["server"] == "prod":
        server_url = server_prod_url
    elif request.POST["server"] == "dev":
        server_url = server_dev_url

    game_state_id = request.POST["game_state_id"]
    create_at = request.POST["create_at"]

    requests.get(server_url + "del_bonus_resource?game_state_id=" + game_state_id +
                 "&create_at_bonus=" + create_at+ "&key=" + server_key)
    time.sleep(1)
    return find_game_state_bonuses(request)
