import discord
import random
import math
import emojis
from discord.ext import commands

def kirbo_roll(loop, kirbo):
    converters = [kirbo[3]+1, kirbo[3]*1.5+1, kirbo[3]*2+1] # chances affected by kirbo converters
    c, dc, gc = converters[0], converters[1], converters[2]

    cluster_chances = [[100, 0, 0, 0, 0], [92, 8, 0, 0, 0], [80, 15, 5, 0, 0], [70, 20, 8, 2, 0], [60, 25, 10, 5, 0],
                       [42, 35, 15, 8, 0], [19, 50, 20, 10, 1], [3, 55, 25, 15, 2], [0, 40, 35, 20, 5]] # chance ratio of clusters, changes with cluster research
    upgrade_chances = [[100, 0, 0, 0], [90, 10, 0, 0], [80, 15, 5, 0], [68, 20, 10, 2]] # chance ratio of normal:silver:gold:ultra, changes with quality upgraders
    item_chances = [19000, 2000*c, 600*c, 200*c, 180*c, 160*c, 140*c, 120*c, 60*dc, 50*dc, 40*dc, 20*dc, 10*dc, gc] # chance ratio of what item is rolled

    cluster_names = ["", "2x ", "3x ", "4x ", "5x "] # prefix before upgrade name
    upgrade_names = ["", "silver ", "gold ", "ultra "] # prefix before item name
    item_names = ["kirbo", "green kirbo", "pink kirbo",
                  "easy", "normal", "hard", "harder", "insane",
                  "easy demon", "medium demon", "hard demon", "insane demon", "extreme demon",
                  "grandpa demon"]
    item_emojis = [emojis.item_emojis, emojis.silver_item_emojis, emojis.gold_item_emojis, emojis.ultra_item_emojis]
    cluster_emojis = emojis.cluster_emojis
    
    cluster_values = [1, 2, 3, 4, 5] # value to multiply the item value and item count by when in clusters
    upgrade_values = [1, 1.5, 3, 10] # value to multiply the item value by when the quality is higher
    item_values = [1, 3, 5, 8, 10, 12, 14, 16, 25, 35, 50, 70, 100, 500] # kirbo value of the items
    


    rolled_items = [] # the store of all the items rolled
    item_count = [kirbo[5], kirbo[8][0], kirbo[8][1], kirbo[8][2]] # the count of how many of each item were rolled for list of rolled items
    rolled_item_emojis = ["# "] # the store of the emojis of all the items rolled
    total_value = 0 # the total kirbos earned

    for i in range(loop): # getting the items for each roll
        cluster = cluster_names.index(random.choices(cluster_names, weights=cluster_chances[kirbo[7][2]])[0])
        quality = upgrade_names.index(random.choices(upgrade_names, weights=upgrade_chances[kirbo[7][1]])[0])
        item = item_names.index(random.choices(population=item_names, weights=item_chances)[0])

        rolled_items.append(f"{cluster_names[cluster]}{upgrade_names[quality]}{item_names[item]}")
        item_count[quality][item] += cluster_values[cluster]
        rolled_item_emojis.append(item_emojis[quality][item])
        rolled_item_emojis.append(cluster_emojis[cluster])
        total_value += math.ceil(item_values[item] * upgrade_values[quality] * cluster_values[cluster])
    
    reply_message = "".join(rolled_item_emojis) # getting the emojis to reply with
    reply = discord.Embed(description=reply_message, color=0xffd057) # creating the embed for the reply
    reply.set_footer(text=f"{total_value} kirbos rolled") # adding the footer on the embed

    kirbo[0] += total_value # adding rolled kirbos to kirbo store
    kirbo[4] += total_value # adding rolled kirbos to total kirbo store
    kirbo[1] += -loop # removing number of rolled items from roll store
    kirbo[5] = item_count[0] # setting normal item count to new value
    kirbo[8][0] = item_count[1] # setting silver item count to new value
    kirbo[8][1] = item_count[2] # setting gold item count to new value
    kirbo[8][2] = item_count[3] # setting ultra item count to new value

    return [kirbo, reply]