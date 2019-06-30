#!/usr/bin/python3.6
import urllib.request
import sys

#takes a player string and a substring, returns a substring from the end of the input substring to the next quotation mark.
def getValue(player, splitter):
    startIndex = player.index(splitter) + len(splitter)    
    endIndex = player.index('"', startIndex)
    return player[startIndex:endIndex]

#options for year are WIP
def main(year=0):
    if not year:
        r=urllib.request.urlopen('https://baseballsavant.mlb.com/poptime')
    else:
        s='https://baseballsavant.mlb.com/poptime?year=' + str(year)
        r=urllib.request.urlopen(s)
    l = r.readline().decode('utf-8')
    #all the data is in a single line.
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
    l = l.split('"catcher":"')
    #arr[0] has no useful data, and has a different format from every other index
    arr = [""] * (len(l) - 1)
    for i in range(1, len(l)):
        player=l[i]
        #missing string values are set to ''. missing numerical values are set to -1
        try:
            name = player[:player.index('"')]
        except ValueError:
            name = ""
        try:
            team=getValue(player, 'team_name_abbrev":"') 
        except ValueError:
            team = ""
        try:
            pop2b=float(getValue(player, 'pop_2b_sba":"'))
        except ValueError:
            pop2b = -1 
        try: 
            exchange2b=float(getValue(player, 'exchange_2b_sba":"'))
        except ValueError:
            exchange2b = -1 
        try:
            vel2b=float(getValue(player, 'maxeff_arm_2b_sba":"'))
        except ValueError:
            vel2b = -1

        arr[i-1]=(name, pop2b, team, vel2b, exchange2b)
        units = ['name', 's',    '', 'mph',        's']#under their corresponding entry
    #when finished, returns a large array of all the players with their data in the same index/tuple, and an array of units for each player-tuple index
    return (arr, units)
    #useful to have the full string format available: Carson Kelly","team_name":"Cardinals","team_name_abbrev":"STL","team_id":138,"pop_2b_sba_count":"1","pop_2b_sba":"2.26","pop_2b_sb":"2.26","pop_2b_cs":"-.--","exchange_2b_sba_count":"2","exchange_2b_sba":"0.92","exchange_2b_sb":"0.92","exchange_2b_cs":null,"maxeff_arm_2b_sba_count":"1","maxeff_arm_2b_sba":"80.6","maxeff_arm_2b_sb":"80.6","maxeff_arm_2b_cs":null,"pop_3b_sba_count":"0","pop_3b_sba":"-.--","pop_3b_sb":"-.--","pop_3b_cs":"-.--","exchange_3b_sba_count":"0","exchange_3b_sba":null,"exchange_3b_sb":null,"exchange_3b_cs":null,"maxeff_arm_3b_sba_count":"0","maxeff_arm_3b_sba":null,"maxeff_arm_3b_sb":null,"maxeff_arm_3b_cs":null,"exchange_2b_3b_sba":"0.92","maxeff_arm_2b_3b_sba":"80.6","p_2b_cs":"0","p_3b_cs":"0","p_2b_sb":"1","p_3b_sb":"0","p_2b_cs_per":"0.0000000000000000","p_3b_cs_per":null,"p_2b_sb_per":"1.0000000000000000","p_3b_sb_per":null},{"year":2018,"age":34,"player_id":446192,
