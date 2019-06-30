#!/usr/bin/python3.6
import urllib.request
import sys
#options for year are WIP
def main(year=0):
    if not year:
        r=urllib.request.urlopen('https://baseballsavant.mlb.com/sprint_speed_leaderboard')  
    else:
        s = 'https://baseballsavant.mlb.com/sprint_speed_leaderboard?year=' + str(year)
        r=urllib.request.urlopen(s)
        
    l = r.readline().decode('utf-8')
    #all the data is in a single line
    while l:
        if '<!-- main content -->' in l:
            break
        
        l = r.readline().decode('utf-8')

    l = r.readline().decode('utf-8')
    #this line contains all the player data
    while l:
        if 'var data' in l:
            break
        l = r.readline().decode('utf-8')

    #splits the data line into strings for individual players
    l = l.split('"name_display_last_first":"')
    arr = [""] * (len(l) - 1)
    #arr[0] has no useful data, and has a different format from every other index
    for i in range(1, len(l)):
        player=l[i]
        n = player[0:player.index('"')]
        j = n.index(',')
        name = n[j+2:] + " " + n[0:j]
        
        #finds the unrounded sprint speed
        splitter='"r_sprint_speed_top50percent":"'
        startIndex = player.index(splitter) + len(splitter) 
        endIndex = player.index('","', startIndex) 
        speed=player[startIndex:endIndex]
        #finds the name 
        splitter='name_abbrev":"'
        startIndex = player.index(splitter) + len(splitter)
        team=player[startIndex: (startIndex + 3)]
        #finds the position
        splitter = 'position_name":"'
        startIndex = player.index(splitter) + len(splitter)
        endIndex = player.index('","', startIndex)
        pos=player[startIndex:endIndex]
        arr[i-1]=(name, float(speed), team, pos)
    units =      [  '',       'ft/s',   '',  '']#under their corresponding entry
    #when finished, returns a large array of all the players with their data in the same index/tuple, and an array of the units for each player-tuple index
    return (arr, units)
