from flask_login import current_user
import math as math
import numpy as np

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def is_consume_over(consume, needed):
    if consume > needed:
        return "w3-red"
    else:
        return "w3-green"

def is_neg_score(score, low, high):
    if score < low or score > high:
        return "w3-red"
    else:
        return "w3-green"

def cal_healthscore(health_score):
    if current_user.cal_consume == 0:
        return health_score

    score_bias = [0.01,0.5,0.5,0.25,1,1.25]
    health_score[0] = (health_score[0] + (current_user.cal_consume - current_user.cal_needed) * score_bias[0]) * 0.5
    health_score[1] = (health_score[1] + (current_user.protein_consume - current_user.protein_needed) * score_bias[1]) * 0.5
    health_score[2] = (health_score[2] + (current_user.fat_consume - current_user.fat_needed) * score_bias[2]) * 0.5
    health_score[3] = (health_score[3] + (current_user.carb_consume - current_user.carb_needed) * score_bias[3]) * 0.5    
    health_score[4] = (health_score[4] + (current_user.sugar_consume - current_user.sugar_needed) * score_bias[4]) * 0.5
    health_score[5] = (health_score[5] + (current_user.sodium_consume - current_user.sodium_needed) * score_bias[5]) * 0.5
    for i in range(6):
        health_score[6] = health_score[6] + abs(health_score[i])
    health_score[6] = health_score[6] * 0.5
    print(health_score[6])
    return health_score

def write_note(item):
    if current_user.cal_consume + item.calories > current_user.cal_needed:
        item.note = item.note + "over_calories, "
    if current_user.protein_consume + item.protein > current_user.protein_needed:
        item.note = item.note + "over_protein, "
    if current_user.fat_consume + item.fat > current_user.fat_needed:
        item.note = item.note + "over_fat, "
    if current_user.carb_consume + item.carb > current_user.carb_needed:
        item.note = item.note + "over_carb, "
    if current_user.sugar_consume + item.sugar > current_user.sugar_needed:
        item.note = item.note + "over_sugar, "
    if current_user.sodium_consume + item.sodium > current_user.sodium_needed:
        item.note = item.note + "over_sodium, "
    
    if len(item.note) > 4:
        item.note = item.note.replace('none','')
    return item

def in_restrict(item):
    user_rest = current_user.restrict.split(';')
    item_rest = item.restrict.split(';')
    n = len(user_rest)
    m = len(item_rest)
    if len(item_rest) == 1 or len(item_rest) == 1:
        return False
    i = 1
    j = 1
    while i < n and j < m:
        if user_rest[i] == item_rest[j]:
            return True
        elif user_rest[i] < item_rest[j]:
            i = i + 1
        elif user_rest[i] > item_rest[j]:
            j = j + 1
    return False

def foodlist_filter(items):
    new_item = []
    for item in items:
        if not in_restrict(item) and fooditem_score(item) < 300:
            new_item.append(item)
    return new_item

def fooditem_score(item):
    health_score = [float(x) for x in current_user.health_score.split(';')]

    score = 0
    score = score + health_score[6]
    score = score + abs(current_user.prefer_salty - item.salty)
    score = score + abs(current_user.prefer_sweet - item.sweet)
    score = score + abs(current_user.prefer_sour - item.sour)
    score = score + abs(current_user.prefer_bitter - item.bitter)
    score = score + abs(current_user.prefer_spicy - item.spicy)

    if current_user.cal_consume + item.calories > current_user.cal_needed:
        score = score + 50 
    if current_user.protein_consume + item.protein > current_user.protein_needed:
        score = score + 50
    if current_user.fat_consume + item.fat > current_user.fat_needed:
        score = score + 50
    if current_user.carb_consume + item.carb > current_user.carb_needed:
        score = score + 50
    if current_user.sugar_consume + item.sugar > current_user.sugar_needed:
        score = score + 50
    if current_user.sodium_consume + item.sodium > current_user.sodium_needed:
        score = score + 50

    return score