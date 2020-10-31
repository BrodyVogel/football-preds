import numpy as np
import pandas as pd

#reload(pd)

def get_data(date, attributes):

    output = pd.DataFrame({'team': []})
    output = output.set_index('team')

    for attribute in list(attributes.keys()):
        if 'predictive' in attribute:
            url = 'https://www.teamrankings.com/college-football/ranking/' + attribute + '?date=' + date
        else:
            url = 'https://www.teamrankings.com/college-football/stat/' + attribute + '?date=' + date

        z = pd.read_html(url, flavor = 'html5lib')[0]

        z = z.iloc[:, 0:3]

        z.columns = [attribute + '_rank', 'team', attribute]

        if 'predictive' in attribute:
            z['team'] = [x.split(' (')[0] for x in z['team']]

        z = z.set_index('team')

        output = pd.merge(z, output, how = 'left', on = ['team'])

    output = output.replace('--', np.nan)

    for column in output.columns:
        output[column] = pd.to_numeric(output[column])

    for column in output.columns:
        if 'rank' in column:
            key = column.split('_rank')[0]
            if attributes[key] == 'desc':
                output[column] = output[key].rank(ascending = False)
            else:
                output[column] = output[key].rank(ascending = True)

    return output

def evaluate(data, teamA, teamB):
    teamA_stats = data.loc[teamA]

    teamB_stats = data.loc[teamB]

    final_score = 0

    # Passing Offense - Home Team
    if teamA_stats['yards-per-pass-attempt_rank'] + 10 < teamB_stats['opponent-yards-per-pass-attempt_rank']:
        print(teamA, "has an advantage passing against the ", teamB, " defense. (YPP/Rank: ",
              str(teamA_stats['yards-per-pass-attempt']), '/', str(teamA_stats['yards-per-pass-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamB_stats['opponent-yards-per-pass-attempt']),
              str(teamB_stats['opponent-yards-per-pass-attempt_rank']))

        final_score += 1

    elif teamB_stats['opponent-yards-per-pass-attempt_rank'] + 10 < teamA_stats['yards-per-pass-attempt_rank']:
        print(teamB, "has an advantage DEFENDING the pass against the ", teamA, " offense. (Defense YPP/Rank: ",
              str(teamB_stats['opponent-yards-per-pass-attempt']), '/',
              str(teamB_stats['opponent-yards-per-pass-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamA_stats['yards-per-pass-attempt']), str(teamA_stats['yards-per-pass-attempt_rank']))

        final_score -=1

    else:
        a = 0
        #print("Neither team has an advantage when", teamA, "passes.")

    # Passing Offense - Away Team
    if teamB_stats['yards-per-pass-attempt_rank'] + 10 < teamA_stats['opponent-yards-per-pass-attempt_rank']:
        print(teamB, "has an advantage passing against the ", teamA, " defense. (YPP/Rank: ",
              str(teamB_stats['yards-per-pass-attempt']), '/', str(teamB_stats['yards-per-pass-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamA_stats['opponent-yards-per-pass-attempt']),
              str(teamA_stats['opponent-yards-per-pass-attempt_rank']))

        final_score -= 1

    elif teamA_stats['opponent-yards-per-pass-attempt_rank'] + 10 < teamB_stats['yards-per-pass-attempt_rank']:
        print(teamA, "has an advantage DEFENDING the pass against the ", teamB, " offense. (Defense YPP/Rank: ",
              str(teamA_stats['opponent-yards-per-pass-attempt']), '/',
              str(teamA_stats['opponent-yards-per-pass-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamB_stats['yards-per-pass-attempt']), str(teamB_stats['yards-per-pass-attempt_rank']))

        final_score += 1

    else:
        a = 0
        #print("Neither team has an advantage when", teamB, "passes.")
        
    # Rushing Offense - Home Team
    if teamA_stats['yards-per-rush-attempt_rank'] + 10 < teamB_stats['opponent-yards-per-rush-attempt_rank']:
        print(teamA, "has an advantage rushing against the ", teamB, " defense. (YPP/Rank: ",
              str(teamA_stats['yards-per-rush-attempt']), '/', str(teamA_stats['yards-per-rush-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamB_stats['opponent-yards-per-rush-attempt']),
              str(teamB_stats['opponent-yards-per-rush-attempt_rank']))

        final_score += 1

    elif teamB_stats['opponent-yards-per-rush-attempt_rank'] + 10 < teamA_stats['yards-per-rush-attempt_rank']:
        print(teamB, "has an advantage DEFENDING the rush against the ", teamA, " offense. (Defense YPP/Rank: ",
              str(teamB_stats['opponent-yards-per-rush-attempt']), '/',
              str(teamB_stats['opponent-yards-per-rush-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamA_stats['yards-per-rush-attempt']), str(teamA_stats['yards-per-rush-attempt_rank']))

        final_score -=1

    else:
        a = 0
        #print("Neither team has an advantage when", teamA, "rushes.")

    # Rushing Offense - Away Team
    if teamB_stats['yards-per-rush-attempt_rank'] + 10 < teamA_stats['opponent-yards-per-rush-attempt_rank']:
        print(teamB, "has an advantage rushing against the ", teamA, " defense. (YPP/Rank: ",
              str(teamB_stats['yards-per-rush-attempt']), '/', str(teamB_stats['yards-per-rush-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamA_stats['opponent-yards-per-rush-attempt']),
              str(teamA_stats['opponent-yards-per-rush-attempt_rank']))

        final_score -= 1

    elif teamA_stats['opponent-yards-per-rush-attempt_rank'] + 10 < teamB_stats['yards-per-rush-attempt_rank']:
        print(teamA, "has an advantage DEFENDING the rush against the ", teamB, " offense. (Defense YPP/Rank: ",
              str(teamA_stats['opponent-yards-per-rush-attempt']), '/',
              str(teamA_stats['opponent-yards-per-rush-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamB_stats['yards-per-rush-attempt']), str(teamB_stats['yards-per-rush-attempt_rank']))

        final_score += 1

    else:
        a = 0
        #print("Neither team has an advantage when", teamB, "rushes.")

    # Total Offense - Home Team
    if teamA_stats['offensive-points-per-game_rank'] + 10 < teamB_stats['opponent-offensive-points-per-game_rank']:
        print(teamA, "has an overall offensive advantage against the ", teamB, " defense. (OPPG/Rank: ",
              str(teamA_stats['offensive-points-per-game']), '/', str(teamA_stats['offensive-points-per-game_rank']),
              " vs Defense's OPPG/Rank: ", str(teamB_stats['opponent-offensive-points-per-game']),
              str(teamB_stats['opponent-offensive-points-per-game_rank']))

        final_score += 1

    elif teamB_stats['opponent-offensive-points-per-game_rank'] + 10 < teamA_stats['offensive-points-per-game_rank']:
        print(teamB, "has an overall advantage DEFENDING against the ", teamA, " offense. (Defense OPPG/Rank: ",
              str(teamB_stats['opponent-offensive-points-per-game']), '/',
              str(teamB_stats['opponent-offensive-points-per-game_rank']), " vs Opponent OPPG/Rank: ",
              str(teamA_stats['offensive-points-per-game']), str(teamA_stats['offensive-points-per-game_rank']))

        final_score -=1

    else:
        a = 0
        #print("Neither team has an overall advantage when", teamA, "is on offense.")

    # Total Offense - Away Team
    if teamB_stats['offensive-points-per-game_rank'] + 10 < teamA_stats['opponent-offensive-points-per-game_rank']:
        print(teamB, "has an overall offensive advantage against the ", teamA, " defense. (OPPG/Rank: ",
              str(teamB_stats['offensive-points-per-game']), '/', str(teamB_stats['offensive-points-per-game_rank']),
              " vs Defense's OPPG/Rank: ", str(teamA_stats['opponent-offensive-points-per-game']),
              str(teamA_stats['opponent-offensive-points-per-game_rank']))

        final_score -= 1

    elif teamA_stats['opponent-offensive-points-per-game_rank'] + 10 < teamB_stats['offensive-points-per-game_rank']:
        print(teamA, "has an overall advantage DEFENDING against the ", teamB, " offense. (Defense OPPG/Rank: ",
              str(teamA_stats['opponent-offensive-points-per-game']), '/',
              str(teamA_stats['opponent-offensive-points-per-game_rank']), " vs Opponent OPPG/Rank: ",
              str(teamB_stats['offensive-points-per-game']), str(teamB_stats['offensive-points-per-game_rank']))

        final_score += 1

    else:
        a = 0
        #print("Neither team has an overall advantage when", teamB, "is on offense.")
        
    # Turnovers
    if teamA_stats['turnover-margin-per-game_rank'] + 10 < teamB_stats['turnover-margin-per-game_rank']:
        print(teamA, "has the turnover advantage against ", teamB, ". (TOMPG/Rank: ",
              str(teamA_stats['turnover-margin-per-game']), '/', str(teamA_stats['turnover-margin-per-game_rank']),
              " vs Opponent TOMPG/Rank: ", str(teamB_stats['turnover-margin-per-game']),
              str(teamB_stats['turnover-margin-per-game_rank']))

        final_score += 1

    elif teamB_stats['turnover-margin-per-game_rank'] + 10 < teamA_stats['turnover-margin-per-game_rank']:
        print(teamB, "has the turnover advantage against ", teamA, ". (TOMPG/Rank: ",
              str(teamB_stats['turnover-margin-per-game']), '/',
              str(teamB_stats['turnover-margin-per-game_rank']), " vs Opponent TOMPG/Rank: ",
              str(teamA_stats['turnover-margin-per-game']), str(teamA_stats['turnover-margin-per-game_rank']))

        final_score -=1

    else:
        a = 0
        #print("Neither team has a turnover advantage.")

    # TeamRankings Rank
    if teamA_stats['predictive-by-other_rank'] < teamB_stats['predictive-by-other_rank']:
        print(teamA, "has a better TR rating than", teamB, ". (Rating/Rank: ",
              str(teamA_stats['predictive-by-other']), '/', str(teamA_stats['predictive-by-other_rank']),
              " vs Opponent Rating/Rank: ", str(teamB_stats['predictive-by-other']),
              str(teamB_stats['predictive-by-other_rank']))

        final_score += 1

    else:
        print(teamB, "has a better TR rating than ", teamA, ". (Rating/Rank: ",
              str(teamB_stats['predictive-by-other']), '/',
              str(teamB_stats['predictive-by-other_rank']), " vs Opponent Rating/Rank: ",
              str(teamA_stats['predictive-by-other']), str(teamA_stats['predictive-by-other_rank']))

        final_score -=1

    if final_score > 0:
        print(teamA, " is likely to win, with a score of ", str(final_score), " (on a scale of -8 to 8)")

    elif final_score < 0:
        print(teamB, " is likely to win, with a score of ", str(-1 * final_score), " (on a scale of -8 to 8)")

    else:
        print("Neither team has a clear advantage.")

def get_data_nfl(date, attributes):

    output = pd.DataFrame({'team': []})
    output = output.set_index('team')

    for attribute in list(attributes.keys()):
        if 'predictive' in attribute:
            url = 'https://www.teamrankings.com/nfl/ranking/' + attribute + '?date=' + date
        else:
            url = 'https://www.teamrankings.com/nfl/stat/' + attribute + '?date=' + date

        z = pd.read_html(url, flavor = 'html5lib')[0]

        z = z.iloc[:, 0:3]

        z.columns = [attribute + '_rank', 'team', attribute]

        if 'predictive' in attribute:
            z['team'] = [x.split(' (')[0] for x in z['team']]

        z = z.set_index('team')

        output = pd.merge(z, output, how = 'left', on = ['team'])

    output = output.replace('--', np.nan)

    for column in output.columns:
        output[column] = pd.to_numeric(output[column])

    for column in output.columns:
        if 'rank' in column:
            key = column.split('_rank')[0]
            if attributes[key] == 'desc':
                output[column] = output[key].rank(ascending = False)
            else:
                output[column] = output[key].rank(ascending = True)

    return output

def get_schedule(week):
    url = "https://www.teamrankings.com/nfl/schedules/season/" + '?week=' + str(week + 501)

    games = pd.read_html(url, flavor='html5lib')[0]

    games.columns = ['Teams', 'Times', 'Location']

    games = games[['Teams', 'Times']]

    games[['Away_Team', 'Home_Team']] = games['Teams'].str.split("@", n = 1, expand = True)

    games = games.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    games['Week'] = week

    games = games[['Week', 'Away_Team', 'Home_Team']]

    return(games)

## 21-6
## 1 [5-3] | 2 [2-1] | 3 [5-0] | 4 [5-1] | 5 [0-1] | 6 [3-0] | 7 [0-0] | 8 [1-0]
## Week 5 (10-24)
# Kansas State > Kansas (6) [W by 41]
# Coastal Carolina > GA Southen (1) [W by 14]
# North Carolina > NC State (4) [W by 27]
# Clemson > Syracuse (4) [W by 26]
# Charlotte > UTEP (3) [W by 10]
# Louisville > Florida State (2) [W by 32]
# Memphis > Temple (3) [W by 12]
# Auburn > Ole Miss (4) [W by 7]
# Oklahoma > TCU (1) [W by 19]
# Liberty > Southern Miss (6) [W by 21]
# UCF > Tulane (1) [W by 17]
# Marshall > FAU (2) [W by 11]
# Oklahoma St > Iowa St (3) -- [W by 3]
# Notre Dame > Pittsburgh (3) [W by 42]
# VA Tech > Wake Forest (1) [L by 7]
# Houston > Navy (4) [W by 16]
# Rice > MTU (1) [L by 6 in OT]
# Alabama > Tennessee (6) [W by 31]
# Texas > Baylor (1) [W by 11]
# Kentucky > Missouri (5) -- [L by 10]
# Georgia State > Troy (3) -- [W by 2]
# Boston College > GA Tech (4) -- [W by 21]
# WVU > TTU (4) -- [L by 7]
# LSU  > South Carolina (1) [W by 28]
# SMU > Cinn (2) [L by 29]
# AFA > SJSU (1) [L by 11]
# BYU > Texas St (8) [W by 38]

## (10-31)
# Marshall > FIU (5)
# Minnesota > Maryland (1)
# Tulsa > ECU (8)
# Hawaii > Wyoming (4)
# KSU > WVU (2) --
# Wake Forest > Syracuse (4)
# Clemson > BC (8)
# ISU > Kansas (8)
# Georgia = Kentucky (0)
# Purdue > Illinois (4)
# CCU > GA State (2)
# Michigan > MSU (6)
# Cincinnati > Memphis (5)
# FAU > UTSA (2)
# Tulane > Temple (3)
# UCF > Houston (2)
# North Texas > UTEP (1)
# Troy > Ark St (2) --
# Rice > SMU (2)
# Notre Dame > GA Tech (8)
# LSU > Auburn (3)
# NW > Iowa (5)
# Indiana = Rutgers (0)
# Baylor > TCU (4) --
# Ole Miss > Vanderbilt (3)
# App St > ULM (7)
# OK St == Texas (0)
# VA Tech > Louisville (2)
# Boise St > AFA (4) --
# SJSU > UNM (1)
# Arkansas == Texas A&M --
# Florida > Missouri (5)
# OSU > Penn St (1)
# SMU > Navy (4)
# UNC > Virginia (6) --
# ULL > Texas St (6)
# Oklahoma > TTU (1)
# SDSU > Utah St (7)
# BYU > WKU (8)
# Nevada > UNLV (3)

#z = pd.read_html('https://www.vegasinsider.com/college-football/scoreboard/', flavor = 'html5lib')