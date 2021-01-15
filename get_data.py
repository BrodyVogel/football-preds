import numpy as np
import pandas as pd
import datetime
import re
from sklearn import preprocessing

#reload(pd)

def get_data_ncaaf(date, attributes):

    output = pd.DataFrame({'team': []})
    output = output.set_index('team')

    for attribute in list(attributes.keys()):
        if 'by-other' in attribute:
            url = 'https://www.teamrankings.com/college-football/ranking/' + attribute + '?date=' + date
        else:
            url = 'https://www.teamrankings.com/college-football/stat/' + attribute + '?date=' + date

        z = pd.read_html(url, flavor = 'html5lib')[0]

        z = z.iloc[:, 0:3]

        z.columns = [attribute + '_rank', 'team', attribute]

        z = z.replace('Miami (OH)', 'Miami_OH')
        z = z.replace('Miami (FL)', 'Miami_FL')

        if 'by-other' in attribute:
            z['team'] = ['Miami_OH' if 'Miami (OH)' in x
                         else 'Miami_FL' if 'Miami (FL' in x
                         else x.split(' (')[0] for x in z['team']]

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

def adjust_sos(data, sos_column, magnitude, group_columns = []):

    if group_columns == []:
        data[sos_column + '_adj_neg'] = data[sos_column].rank(pct=True)
        data[sos_column + '_adj_pos'] = data[sos_column].rank(pct=True, ascending=False)
    else:
        data[sos_column + '_adj_neg'] = data.groupby(group_columns)[sos_column].rank(pct=True)
        data[sos_column + '_adj_pos'] = data.groupby(group_columns)[sos_column].rank(pct=True, ascending=False)

    data[sos_column + '_adj'] = np.asarray([data[sos_column + '_adj_pos'][x] if data[sos_column + '_adj_pos'][x] > 0.49
                                        else -1 * data[sos_column + '_adj_neg'][x] for x in range(len(data[sos_column]))])

    data[sos_column + '_adj'] = data[sos_column + '_adj'] * magnitude

    data = data.drop(columns=[sos_column + '_adj_neg', sos_column + '_adj_pos'])

    for col in data.columns:
        if 'rank' in col and col not in [sos_column, sos_column + '_adj']:
            data[col] = data[col] - data[sos_column + '_adj']

    return(data)


def evaluate_v2(data, teamA, teamB, magnitude=12, factor_policy={}, store=False, verbose=False, spread_target = None,
                grouping = 'overall'):
    teamA_stats = data.loc[teamA]

    teamB_stats = data.loc[teamB]

    ht = 0
    ht_3s = 0
    ht_2s = 0
    ht_1s = 0
    ht_half = 0
    at = 0
    at_3s = 0
    at_2s = 0
    at_1s = 0
    at_half = 0

    for factor in factor_policy.keys():

        if factor_policy[factor]['two_fac'] != None:
            factor_good = factor_policy[factor]['two_fac'][0]
            factor_bad = factor_policy[factor]['two_fac'][1]

            teamA_good_fac = teamA_stats[factor_good]
            teamB_good_fac = teamB_stats[factor_good]
            teamA_bad_fac = teamA_stats[factor_bad]
            teamB_bad_fac = teamB_stats[factor_bad]

            teamA_status = teamB_bad_fac - teamA_good_fac
            teamB_status = teamA_bad_fac - teamB_good_fac

            if factor_policy[factor]["three_points"] != None:
                if teamA_status > factor_policy[factor]["three_points"][0]:
                    ht += 3
                    ht_3s += 1
                    if verbose == True:
                        print(teamA + " has a +3 advantage on " + factor)
                elif teamA_status > factor_policy[factor]["two_points"][0]:
                    ht += 2
                    ht_2s += 1
                    if verbose == True:
                        print(teamA + " has a +2 advantage on " + factor)
                elif teamA_status > factor_policy[factor]["one_point"][0]:
                    ht += 1
                    ht_1s += 1
                    if verbose == True:
                        print(teamA + " has a +1 advantage on " + factor)
                elif teamA_status > magnitude:
                    ht += 0.5
                    ht_half += 1
                    if verbose == True:
                        print(teamA + " has a +0.5 advantage on " + factor)
                else:
                    ht += 0

                if teamB_status > factor_policy[factor]["three_points"][0]:
                    at += 3
                    at_3s += 1
                    if verbose == True:
                        print(teamB + " has a +3 advantage on " + factor)
                elif teamB_status > factor_policy[factor]["two_points"][0]:
                    at += 2
                    at_2s += 1
                    if verbose == True:
                        print(teamB + " has a +2 advantage on " + factor)
                elif teamB_status > factor_policy[factor]["one_point"][0]:
                    at += 1
                    at_1s += 1
                    if verbose == True:
                        print(teamB + " has a +1 advantage on " + factor)
                elif teamB_status > magnitude:
                    at += 0.5
                    at_half += 1
                    if verbose == True:
                        print(teamB + " has a +0.5 advantage on " + factor)
                else:
                    at += 0

            else:
                if teamA_status > factor_policy[factor]["two_points"][0]:
                    ht += 2
                    ht_2s += 1
                    if verbose == True:
                        print(teamA + " has a +2 advantage on " + factor)
                elif teamA_status > factor_policy[factor]["one_point"][0]:
                    ht += 1
                    ht_1s += 1
                    if verbose == True:
                        print(teamA + " has a +1 advantage on " + factor)
                elif teamA_status > magnitude:
                    ht += 0.5
                    ht_half += 1
                    if verbose == True:
                        print(teamA + " has a +0.5 advantage on " + factor)
                else:
                    ht += 0

                if teamB_status > factor_policy[factor]["two_points"][0]:
                    at += 2
                    at_2s += 1
                    if verbose == True:
                        print(teamB + " has a +2 advantage on " + factor)
                elif teamB_status > factor_policy[factor]["one_point"][0]:
                    at += 1
                    at_1s += 1
                    if verbose == True:
                        print(teamB + " has a +1 advantage on " + factor)
                elif teamB_status > magnitude:
                    at += 0.5
                    at_half += 1
                    if verbose == True:
                        print(teamB + " has a +0.5 advantage on " + factor)
                else:
                    at += 0

        else:

            teamA_status = teamB_stats[factor] - teamA_stats[factor]
            teamB_status = teamA_stats[factor] - teamB_stats[factor]

            if factor_policy[factor]["three_points"] != None:
                if teamA_status > factor_policy[factor]["three_points"][0]:
                    ht += 3
                    ht_3s += 1
                    if verbose == True:
                        print(teamA + " has a +3 advantage on " + factor)
                elif teamA_status > factor_policy[factor]["two_points"][0]:
                    ht += 2
                    ht_2s += 1
                    if verbose == True:
                        print(teamA + " has a +2 advantage on " + factor)
                elif teamA_status > factor_policy[factor]["one_point"][0]:
                    ht += 1
                    ht_1s += 1
                    if verbose == True:
                        print(teamA + " has a +1 advantage on " + factor)
                elif teamA_status > magnitude:
                    ht += 0.5
                    ht_half += 1
                    if verbose == True:
                        print(teamA + " has a +0.5 advantage on " + factor)
                else:
                    ht += 0

                if teamB_status > factor_policy[factor]["three_points"][0]:
                    at += 3
                    at_3s += 1
                    if verbose == True:
                        print(teamB + " has a +3 advantage on " + factor)
                elif teamB_status > factor_policy[factor]["two_points"][0]:
                    at += 2
                    at_2s += 1
                    if verbose == True:
                        print(teamB + " has a +2 advantage on " + factor)
                elif teamB_status > factor_policy[factor]["one_point"][0]:
                    at += 1
                    at_1s += 1
                    if verbose == True:
                        print(teamB + " has a +1 advantage on " + factor)
                elif teamB_status > magnitude:
                    at += 0.5
                    at_half += 1
                    if verbose == True:
                        print(teamB + " has a +0.5 advantage on " + factor)
                else:
                    at += 0

            else:
                if teamA_status > factor_policy[factor]["two_points"][0]:
                    ht += 2
                    ht_2s += 1
                    if verbose == True:
                        print(teamA + " has a +2 advantage on " + factor)
                elif teamA_status > factor_policy[factor]["one_point"][0]:
                    ht += 1
                    ht_1s += 1
                    if verbose == True:
                        print(teamA + " has a +1 advantage on " + factor)
                elif teamA_status > magnitude:
                    ht += 0.5
                    ht_half += 1
                    if verbose == True:
                        print(teamA + " has a +0.5 advantage on " + factor)
                else:
                    ht += 0

                if teamB_status > factor_policy[factor]["two_points"][0]:
                    at += 2
                    at_2s += 1
                    if verbose == True:
                        print(teamB + " has a +2 advantage on " + factor)
                elif teamB_status > factor_policy[factor]["one_point"][0]:
                    at += 1
                    at_1s += 1
                    if verbose == True:
                        print(teamB + " has a +1 advantage on " + factor)
                elif teamB_status > magnitude:
                    at += 0.5
                    at_half += 1
                    if verbose == True:
                        print(teamB + " has a +0.5 advantage on " + factor)
                else:
                    at += 0

    if ht > at:
        print(teamA, " is likely to win, with a score of ", str(ht - at))

    elif ht < at:
        print(teamB, " is likely to win, with a score of ", str(at - ht))

    else:
        print("Neither team has a clear advantage.")

    if store == True:
        if grouping == 'overall':
            if ht > at:
                return([ht, at, ht - at, teamA])
            elif at > ht:
                return([at, ht, at-ht, teamB])
            else:
                return([ht, at, ht-at, 'Neither'])

        elif grouping == 'threes':
            if ht_3s > at_3s:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, teamA])
            elif at_3s > ht_3s:
                return ([at - ht, at_3s - ht_3s, at_2s - ht_2s, at_1s - ht_1s, at_half - ht_half, teamB])
            else:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, 'Neither'])

        elif grouping == 'twos':
            if ht_2s > at_2s:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, teamA])
            elif at_2s > ht_2s:
                return ([at - ht, at_3s - ht_3s, at_2s - ht_2s, at_1s - ht_1s, at_half - ht_half, teamB])
            else:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, 'Neither'])

        elif grouping == 'ones':
            if ht_1s > at_1s:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, teamA])
            elif at_1s > ht_1s:
                return ([at - ht, at_3s - ht_3s, at_2s - ht_2s, at_1s - ht_1s, at_half - ht_half, teamB])
            else:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, 'Neither'])

        elif grouping == 'half':
            if ht_half > at_half:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, teamA])
            elif at_half > ht_half:
                return ([at - ht, at_3s - ht_3s, at_2s - ht_2s, at_1s - ht_1s, at_half - ht_half, teamB])
            else:
                return ([ht - at, ht_3s - at_3s, ht_2s - at_2s, ht_1s - at_1s, ht_half - at_half, 'Neither'])

    if spread_target != None:
        spread_df = spread_target[0]
        zz = 0
        if ht > at:
            diff = ht - at
        elif at > ht:
            diff = at - ht
        else:
            zz = 1
            diff = 1

        found = False
        row = 0
        while found == False:
            if zz == 1:
                found = True
            if (diff >= spread_df.loc[row, 'min']) and (diff <= spread_df.loc[row, 'max']):
                print("No-Brainer: " + str(-1 * spread_df.loc[row, '25%']), ", Good Bet: " + str(-1 * spread_df.loc[row, '40%']),
                      ", Chance: " + str(-1 * spread_df.loc[row, '50%']))
                print("No-Brainer Fade: " + str(-1 * spread_df.loc[row, '90%']), "Good Fade: " + str(-1 * spread_df.loc[row, '75%']))
                found = True
            else:
                row += 1


def evaluate(data, teamA, teamB, size, store = False):
    teamA_stats = data.loc[teamA]

    teamB_stats = data.loc[teamB]

    ht = 0
    at = 0

    # Passing Offense - Home Team
    if teamA_stats['yards-per-pass-attempt_rank'] + size < teamB_stats['opponent-yards-per-pass-attempt_rank']:
        print(teamA, " has an advantage passing against the ", teamB, " defense. (YPP/Rank: ",
              str(teamA_stats['yards-per-pass-attempt']), '/', str(teamA_stats['yards-per-pass-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamB_stats['opponent-yards-per-pass-attempt']),
              str(teamB_stats['opponent-yards-per-pass-attempt_rank']))

        ht += 1

    elif teamB_stats['opponent-yards-per-pass-attempt_rank'] + size < teamA_stats['yards-per-pass-attempt_rank']:
        print(teamB, " has an advantage DEFENDING the pass against the ", teamA, " offense. (Defense YPP/Rank: ",
              str(teamB_stats['opponent-yards-per-pass-attempt']), '/',
              str(teamB_stats['opponent-yards-per-pass-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamA_stats['yards-per-pass-attempt']), str(teamA_stats['yards-per-pass-attempt_rank']))

        at +=1

    else:
        a = 0
        #print("Neither team has an advantage when", teamA, "passes.")

    # Passing Offense - Away Team
    if teamB_stats['yards-per-pass-attempt_rank'] + size < teamA_stats['opponent-yards-per-pass-attempt_rank']:
        print(teamB, " has an advantage passing against the ", teamA, " defense. (YPP/Rank: ",
              str(teamB_stats['yards-per-pass-attempt']), '/', str(teamB_stats['yards-per-pass-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamA_stats['opponent-yards-per-pass-attempt']),
              str(teamA_stats['opponent-yards-per-pass-attempt_rank']))

        at += 1

    elif teamA_stats['opponent-yards-per-pass-attempt_rank'] + size < teamB_stats['yards-per-pass-attempt_rank']:
        print(teamA, " has an advantage DEFENDING the pass against the ", teamB, " offense. (Defense YPP/Rank: ",
              str(teamA_stats['opponent-yards-per-pass-attempt']), '/',
              str(teamA_stats['opponent-yards-per-pass-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamB_stats['yards-per-pass-attempt']), str(teamB_stats['yards-per-pass-attempt_rank']))

        ht += 1

    else:
        a = 0
        #print("Neither team has an advantage when", teamB, "passes.")
        
    # Rushing Offense - Home Team
    if teamA_stats['yards-per-rush-attempt_rank'] + size < teamB_stats['opponent-yards-per-rush-attempt_rank']:
        print(teamA, " has an advantage rushing against the ", teamB, " defense. (YPP/Rank: ",
              str(teamA_stats['yards-per-rush-attempt']), '/', str(teamA_stats['yards-per-rush-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamB_stats['opponent-yards-per-rush-attempt']),
              str(teamB_stats['opponent-yards-per-rush-attempt_rank']))

        ht += 1

    elif teamB_stats['opponent-yards-per-rush-attempt_rank'] + size < teamA_stats['yards-per-rush-attempt_rank']:
        print(teamB, " has an advantage DEFENDING the rush against the ", teamA, " offense. (Defense YPP/Rank: ",
              str(teamB_stats['opponent-yards-per-rush-attempt']), '/',
              str(teamB_stats['opponent-yards-per-rush-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamA_stats['yards-per-rush-attempt']), str(teamA_stats['yards-per-rush-attempt_rank']))

        at +=1

    else:
        a = 0
        #print("Neither team has an advantage when", teamA, "rushes.")

    # Rushing Offense - Away Team
    if teamB_stats['yards-per-rush-attempt_rank'] + size < teamA_stats['opponent-yards-per-rush-attempt_rank']:
        print(teamB, " has an advantage rushing against the ", teamA, " defense. (YPP/Rank: ",
              str(teamB_stats['yards-per-rush-attempt']), '/', str(teamB_stats['yards-per-rush-attempt_rank']),
              " vs Defense's YPP/Rank: ", str(teamA_stats['opponent-yards-per-rush-attempt']),
              str(teamA_stats['opponent-yards-per-rush-attempt_rank']))

        at += 1

    elif teamA_stats['opponent-yards-per-rush-attempt_rank'] + size < teamB_stats['yards-per-rush-attempt_rank']:
        print(teamA, " has an advantage DEFENDING the rush against the ", teamB, " offense. (Defense YPP/Rank: ",
              str(teamA_stats['opponent-yards-per-rush-attempt']), '/',
              str(teamA_stats['opponent-yards-per-rush-attempt_rank']), " vs Opponent YPP/Rank: ",
              str(teamB_stats['yards-per-rush-attempt']), str(teamB_stats['yards-per-rush-attempt_rank']))

        ht += 1

    else:
        a = 0
        #print("Neither team has an advantage when", teamB, "rushes.")

    # Total Offense - Home Team
    if teamA_stats['offensive-points-per-game_rank'] + size < teamB_stats['opponent-offensive-points-per-game_rank']:
        print(teamA, " has an overall offensive advantage against the ", teamB, " defense. (OPPG/Rank: ",
              str(teamA_stats['offensive-points-per-game']), '/', str(teamA_stats['offensive-points-per-game_rank']),
              " vs Defense's OPPG/Rank: ", str(teamB_stats['opponent-offensive-points-per-game']),
              str(teamB_stats['opponent-offensive-points-per-game_rank']))

        ht += 1

    elif teamB_stats['opponent-offensive-points-per-game_rank'] + size < teamA_stats['offensive-points-per-game_rank']:
        print(teamB, " has an overall advantage DEFENDING against the ", teamA, " offense. (Defense OPPG/Rank: ",
              str(teamB_stats['opponent-offensive-points-per-game']), '/',
              str(teamB_stats['opponent-offensive-points-per-game_rank']), " vs Opponent OPPG/Rank: ",
              str(teamA_stats['offensive-points-per-game']), str(teamA_stats['offensive-points-per-game_rank']))

        at +=1

    else:
        a = 0
        #print("Neither team has an overall advantage when", teamA, "is on offense.")

    # Total Offense - Away Team
    if teamB_stats['offensive-points-per-game_rank'] + size < teamA_stats['opponent-offensive-points-per-game_rank']:
        print(teamB, " has an overall offensive advantage against the ", teamA, " defense. (OPPG/Rank: ",
              str(teamB_stats['offensive-points-per-game']), '/', str(teamB_stats['offensive-points-per-game_rank']),
              " vs Defense's OPPG/Rank: ", str(teamA_stats['opponent-offensive-points-per-game']),
              str(teamA_stats['opponent-offensive-points-per-game_rank']))

        at += 1

    elif teamA_stats['opponent-offensive-points-per-game_rank'] + size < teamB_stats['offensive-points-per-game_rank']:
        print(teamA, " has an overall advantage DEFENDING against the ", teamB, " offense. (Defense OPPG/Rank: ",
              str(teamA_stats['opponent-offensive-points-per-game']), '/',
              str(teamA_stats['opponent-offensive-points-per-game_rank']), " vs Opponent OPPG/Rank: ",
              str(teamB_stats['offensive-points-per-game']), str(teamB_stats['offensive-points-per-game_rank']))

        ht += 1

    else:
        a = 0
        #print("Neither team has an overall advantage when", teamB, "is on offense.")
        
    # Turnovers
    if teamA_stats['turnover-margin-per-game_rank'] + size < teamB_stats['turnover-margin-per-game_rank']:
        print(teamA, "has the turnover advantage against ", teamB, ". (TOMPG/Rank: ",
              str(teamA_stats['turnover-margin-per-game']), '/', str(teamA_stats['turnover-margin-per-game_rank']),
              " vs Opponent TOMPG/Rank: ", str(teamB_stats['turnover-margin-per-game']),
              str(teamB_stats['turnover-margin-per-game_rank']))

        ht += 1

    elif teamB_stats['turnover-margin-per-game_rank'] + size < teamA_stats['turnover-margin-per-game_rank']:
        print(teamB, "has the turnover advantage against ", teamA, ". (TOMPG/Rank: ",
              str(teamB_stats['turnover-margin-per-game']), '/',
              str(teamB_stats['turnover-margin-per-game_rank']), " vs Opponent TOMPG/Rank: ",
              str(teamA_stats['turnover-margin-per-game']), str(teamA_stats['turnover-margin-per-game_rank']))

        at +=1

    else:
        a = 0
        #print("Neither team has a turnover advantage.")

    # TeamRankings Rank
    if teamA_stats['predictive-by-other_rank'] < teamB_stats['predictive-by-other_rank']:
        print(teamA, " has a better TR rating than", teamB, ". (Rating/Rank: ",
              str(teamA_stats['predictive-by-other']), '/', str(teamA_stats['predictive-by-other_rank']),
              " vs Opponent Rating/Rank: ", str(teamB_stats['predictive-by-other']),
              str(teamB_stats['predictive-by-other_rank']))

        ht += 1

    else:
        print(teamB, " has a better TR rating than ", teamA, ". (Rating/Rank: ",
              str(teamB_stats['predictive-by-other']), '/',
              str(teamB_stats['predictive-by-other_rank']), " vs Opponent Rating/Rank: ",
              str(teamA_stats['predictive-by-other']), str(teamA_stats['predictive-by-other_rank']))

        at +=1

    if ht > at:
        print(teamA, " is likely to win, with a score of ", str(ht - at), " (on a scale of -8 to 8)")

    elif ht < at:
        print(teamB, " is likely to win, with a score of ", str(at - ht), " (on a scale of -8 to 8)")

    else:
        print("Neither team has a clear advantage.")

    if store == True:
        if ht > at:
            return([ht, at, ht - at, teamA])
        elif at > ht:
            return([at, ht, at-ht, teamB])
        else:
            return([ht, at, ht-at, 'Neither'])

def get_data_nfl(date, attributes):

    output = pd.DataFrame({'team': []})
    output = output.set_index('team')

    for attribute in list(attributes.keys()):
        if 'by-other' in attribute:
            url = 'https://www.teamrankings.com/nfl/ranking/' + attribute + '?date=' + date
        else:
            url = 'https://www.teamrankings.com/nfl/stat/' + attribute + '?date=' + date

        z = pd.read_html(url, flavor = 'html5lib')[0]

        z = z.iloc[:, 0:3]

        z.columns = [attribute + '_rank', 'team', attribute]

        if 'by-other' in attribute:
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

def get_nfl_schedule(week):
    url = "https://www.teamrankings.com/nfl/schedules/season/" + '?week=' + str(week + 501)

    games = pd.read_html(url, flavor='html5lib')[0]

    games.columns = ['Teams', 'Times', 'Location']

    games = games[['Teams', 'Times']]

    games[['Away_Team', 'Home_Team']] = games['Teams'].str.split("@", n = 1, expand = True)

    games = games.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    games['Week'] = week

    games = games[['Week', 'Away_Team', 'Home_Team']]

    return(games)

def get_ncaa_schedule(week):
    z = pd.read_html('https://www.teamrankings.com/ncf/schedules/season/?week=' + str(week + 1183), flavor = 'html5lib')[0]

    z.columns = ['Teams', 'Drop', 'Drop_2']

    z = z[['Teams']]

    z[['Away Team', 'Home Team']] = z['Teams'].str.split("@|vs.", n=1, expand=True)

    z = z.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    z = z.replace('Miami (OH)', 'Miami_OH')
    z = z.replace('Miami (FL)', 'Miami_FL')

    z = z[['Away Team', 'Home Team']]

    return(z)

def get_historical_nfl_results(years):

    final = pd.DataFrame({'Year': [], 'Week': [], 'Winner': [], 'Loser': [], 'Home_Team': [], 'Margin_of_Victory': []})

    for year in years:
        z = pd.read_html('https://www.pro-football-reference.com/years/' + str(year) + '/games.htm', flavor = 'html5lib')[0]

        z.columns = ['Week', 'Day', 'Date', 'Time', 'Winner', 'Location', 'Loser', 'Nothing', 'PtsW', 'PtsL', 'No',
                     'No2', 'TO2', 'YdsL']

        z = z[['Week', 'Winner', 'Loser', 'Location', 'PtsW', 'PtsL']]

        z = z.replace("New York Jets", "NY Jets Jets")
        z = z.replace("New York Giants", "NY Giants Giants")

        z = z.replace("Los Angeles Rams", "LA Rams Rams")
        z = z.replace("Los Angeles Chargers", "LA Chargers Chargers")

        z = z.dropna(subset = ['Winner', 'Loser'])

        z['Winner'] = z['Winner'].apply(lambda x: " ".join(x.split(" ")[:-1]))
        z['Loser'] = z['Loser'].apply(lambda x: " ".join(x.split(" ")[:-1]))

        z = z.loc[~z['Week'].isin(['Week', 'WildCard', 'Division', 'ConfChamp', 'SuperBowl'])]

        z = z.reset_index(drop = True)

        z['Home_Team'] = np.asarray([z['Loser'][x] if z['Location'][x] == '@'
                                     else z['Winner'][x] for x in range(len(z['Winner']))])

        z['PtsW'] = z['PtsW'].astype('int32')
        z['PtsL'] = z['PtsL'].astype('int32')
        z['Margin_of_Victory'] = z['PtsW'] - z['PtsL']

        z['Week'] = z['Week'].astype('int32')

        z = z[['Week', 'Winner', 'Loser', 'Home_Team', 'Margin_of_Victory']]

        z['Year'] = int(year)

        final = pd.concat([final, z])

        final = final.reset_index(drop = True)

    return(final)

def get_historical_nfl_data(start_dates, start_week, attributes):

    df_list = []

    for start_date in start_dates:
        date_list = []
        for x in range(13):
            original_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            next_date_to_add = original_date + datetime.timedelta(days = 7 * x)
            next_date_to_add = next_date_to_add.strftime('%Y-%m-%d')
            date_list.append(next_date_to_add)

        start_week_go = start_week
        for date in date_list:
            print(date)
            to_concat = get_data_nfl(date, attributes)
            to_concat['Week'] = start_week_go
            to_concat['Year'] = date[0:4]

            df_list.append(to_concat)

            start_week_go += 1

    output = pd.concat(df_list)

    output['Week'] = output['Week'].astype('int32')
    output['Year'] = output['Year'].astype('int32')

    return(output)

def get_historical_ncaa_data(start_dates, start_week, attributes):
    df_list = []

    for start_date in start_dates:
        date_list = []
        for x in range(20):
            original_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            next_date_to_add = original_date + datetime.timedelta(days=7 * x)
            next_date_to_add = next_date_to_add.strftime('%Y-%m-%d')
            date_list.append(next_date_to_add)

        start_week_go = start_week
        for date in date_list:
            print(date)
            try:
                to_concat = get_data_ncaaf(date, attributes)
            except:
                new_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                new_date = new_date + datetime.timedelta(days=1)
                new_date = new_date.strftime('%Y-%m-%d')
                print(new_date)
                to_concat = get_data_ncaaf(new_date, attributes)

            to_concat['Week'] = start_week_go
            to_concat['Year'] = date[0:4]
            to_concat['Date'] = date

            df_list.append(to_concat)

            start_week_go += 1

    output = pd.concat(df_list)

    output['Week'] = output['Week'].astype('int32')
    output['Year'] = output['Year'].astype('int32')

    return (output)

def cap_helper(x):
    x = re.sub("[a-z][A-Z]", lambda ele: ele[0][0] + " " + ele[0][1], x)

    return(x)

def date_helper(x, year1, year2):
    x = str(int(x))
    if len(x) > 3:
        first = x[0:2]
    else:
        first = x[0]
    if int(first) < 8:
        x = x + year2
    else:
        x = x + year1

    if int(first) < 10:
        x = '0' + x

    x = datetime.datetime.strptime(x, '%m%d%Y').strftime('%Y-%m-%d')
    return(x)

def process_historical_ncaa_data():

    fin_output = pd.DataFrame({'DATE': [], 'HOME_TEAM': [], 'WINNER': [], 'LOSER': [], 'PTS_WINNER': [],
                               'PTS_LOSER': [], 'OPEN_SPREAD_WINNER': [], 'OPEN_SPREAD_LOSER': [],
                               'CLOSE_SPREAD_WINNER': [], 'CLOSE_SPREAD_LOSER': [], 'MONEY_LINE_WINNER': [],
                               'MONEY_LINE_LOSER': [], 'MARGIN_OF_VICTORY': []})

    years = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
             '2019-20']

    years_dict = {'2007-08': ['2007', '2008'], '2008-09': ['2008', '2009'], '2009-10': ['2009', '2010'],
                  '2010-11': ['2010', '2011'], '2011-12': ['2011', '2012'], '2012-13': ['2012', '2013'],
                  '2013-14': ['2013', '2014'], '2014-15': ['2014', '2015'], '2015-16': ['2015', '2016'],
                  '2016-17': ['2016', '2017'], '2017-18': ['2017', '2018'], '2018-19': ['2018', '2019'],
                  '2019-20': ['2019', '2020']}

    for file in years:
        z = pd.read_excel('/Users/brodyvogel/Downloads/ncaa football ' + file + '.xlsx')

        for x in range(len(z['Date']) - 1):
            if z['Date'][x] > z['Date'][x + 1]:
                z.loc[x, 'Date'] = z['Date'][x + 1]

        years = years_dict[file]
        z['Team'] = z['Team'].apply(cap_helper)
        z['Date'] = z['Date'].apply(date_helper, args=(years[0], years[1]))

        z['Open'] = np.asarray([100 if x == 'NL' else 0 if x == 'pk' else x for x in z['Open']])
        z['Close'] = np.asarray([100 if x == 'NL' else 0 if x == 'pk' else x for x in z['Close']])

        z['Open'] = z['Open'].astype('str')
        z['Close'] = z['Close'].astype('str')

        z.loc[["," in x for x in z['Open']], 'Open'] = 'adfadad'
        z.loc[[len(x) > 4 for x in z['Open']], 'Open'] = np.nan

        z.loc[["," in x for x in z['Close']], 'Close'] = 'sdfadf'
        z.loc[[len(x) > 4 for x in z['Close']], 'Close'] = np.nan

        z['Open'] = z['Open'].astype('float')
        z['Close'] = z['Close'].astype('float')

        output = pd.DataFrame({'DATE': [], 'HOME_TEAM': [], 'WINNER': [], 'LOSER': [], 'PTS_WINNER': [],
                               'PTS_LOSER': [], 'OPEN_SPREAD_WINNER': [], 'OPEN_SPREAD_LOSER': [],
                               'CLOSE_SPREAD_WINNER': [], 'CLOSE_SPREAD_LOSER': [], 'MONEY_LINE_WINNER': [],
                               'MONEY_LINE_LOSER': [], 'MARGIN_OF_VICTORY': []})

        for x in range(0, len(z['Team']), 2):
            date = z['Date'][x]

            if z['VH'][x] == 'V':
                home_team = z['Team'][x + 1]
            else:
                home_team = 'Neutral'

            if z['Final'][x] > z['Final'][x + 1]:
                winner = z['Team'][x]
                loser = z['Team'][x + 1]
                pts_winner = z['Final'][x]
                pts_loser = z['Final'][x + 1]
            else:
                winner = z['Team'][x + 1]
                loser = z['Team'][x]
                pts_winner = z['Final'][x + 1]
                pts_loser = z['Final'][x]

            spreads = z.iloc[x:(x + 2), :][['Open', 'Close']]
            if spreads['Open'][x] > spreads['Open'][x + 1]:
                z.loc[x, 'Open'] = z.loc[x + 1, 'Open']
                z.loc[x + 1, 'Open'] = -1 * z.loc[x + 1, 'Open']
            else:
                z.loc[x + 1, 'Open'] = z.loc[x, 'Open']
                z.loc[x, 'Open'] = -1 * z.loc[x, 'Open']
            if spreads['Close'][x] > spreads['Close'][x + 1]:
                z.loc[x, 'Close'] = z.loc[x + 1, 'Close']
                z.loc[x + 1, 'Close'] = -1 * z.loc[x + 1, 'Close']
            else:
                z.loc[x + 1, 'Close'] = spreads.loc[x, 'Close']
                z.loc[x, 'Close'] = -1 * spreads.loc[x, 'Close']

            if z['Final'][x] > z['Final'][x + 1]:
                open_spread_winner = z['Open'][x]
                close_spread_winner = z['Close'][x]

                open_spread_loser = z['Open'][x + 1]
                close_spread_loser = z['Close'][x + 1]

                ml_winner = z['ML'][x]
                ml_loser = z['ML'][x + 1]

            else:
                open_spread_winner = z['Open'][x + 1]
                close_spread_winner = z['Close'][x + 1]

                open_spread_loser = z['Open'][x]
                close_spread_loser = z['Close'][x]

                ml_winner = z['ML'][x + 1]
                ml_loser = z['ML'][x]

            margin_of_victory = pts_winner - pts_loser

            new_row = {'DATE': date, 'HOME_TEAM': home_team, 'WINNER': winner, 'LOSER': loser, 'PTS_WINNER': pts_winner,
                       'PTS_LOSER': pts_loser, 'OPEN_SPREAD_WINNER': open_spread_winner,
                       'OPEN_SPREAD_LOSER': open_spread_loser,
                       'CLOSE_SPREAD_WINNER': close_spread_winner, 'CLOSE_SPREAD_LOSER': close_spread_loser,
                       'MONEY_LINE_WINNER': ml_winner, 'MONEY_LINE_LOSER': ml_loser,
                       'MARGIN_OF_VICTORY': margin_of_victory}

            output = output.append(new_row, ignore_index=True)

        print(file)

        fin_output = pd.concat([fin_output, output])

    fin_output = fin_output.reset_index(drop=True)

    fin_output['COVERED_OPEN'] = np.asarray([
        np.nan if np.isnan(fin_output['OPEN_SPREAD_WINNER'][x]) == True
        else 0 if fin_output['OPEN_SPREAD_WINNER'][x] > 0
        else 0 if fin_output['MARGIN_OF_VICTORY'][x] < (-1 * fin_output['OPEN_SPREAD_WINNER'][x])
        else 1 for x in range(len(fin_output['DATE']))])

    fin_output['COVERED_CLOSE'] = np.asarray([
        np.nan if np.isnan(fin_output['CLOSE_SPREAD_WINNER'][x]) == True
        else 0 if fin_output['CLOSE_SPREAD_WINNER'][x] > 0
        else 0 if fin_output['MARGIN_OF_VICTORY'][x] < (-1 * fin_output['CLOSE_SPREAD_WINNER'][x])
        else 1 for x in range(len(fin_output['DATE']))])

    for day in range(len(fin_output['DATE'])):
        cur_date = datetime.datetime.strptime(fin_output['DATE'][day], '%Y-%m-%d')

        if cur_date.weekday() == 0:
            cur_date = cur_date
        elif cur_date.weekday() == 1:
            cur_date = cur_date - datetime.timedelta(days=1)
        elif cur_date.weekday() == 2:
            cur_date = cur_date - datetime.timedelta(days=2)
        elif cur_date.weekday() == 3:
            cur_date = cur_date - datetime.timedelta(days=3)
        elif cur_date.weekday() == 4:
            cur_date = cur_date - datetime.timedelta(days=4)
        elif cur_date.weekday() == 5:
            cur_date = cur_date - datetime.timedelta(days=5)
        elif cur_date.weekday() == 6:
            cur_date = cur_date - datetime.timedelta(days=6)

        cur_date = cur_date.strftime('%Y-%m-%d')

        fin_output.loc[day, 'DATE'] = cur_date

    proper_names = {"App State": "Appalachian State",
                    "Appalachian St": "Appalachian State",
                    "Alabama Crimson": "Alabama",
                    "Arizona U": "Arizona",
                    "Arizona St": "Arizona State",
                    "Arkansas St": "Arkansas State",
                    "Arkansas State Red": "Arkansas State",
                    "BYU": "Brigham Young",
                    "Boston Col": "Boston College",
                    "Bowling Grn": "Bowling Green State",
                    "Bowling Green": "Bowling Green State",
                    "Buffalo U": "Buffalo",
                    "California Golden": "California",
                    "Central FL": "Central Florida",
                    "Central Mich": "Central Michigan",
                    "Cincinnati U": "Cincinnati",
                    "Coastal Car": "Coastal Carolina",
                    "Colorado St": "Colorado State",
                    "Duke Blue": "Duke",
                    "E Carolina": "East Carolina",
                    "E Michigan": "Eastern Michigan",
                    "Fla Atlantic": "Florida Atlantic",
                    "Florida Intl": "Florida International",
                    "Florida St": "Florida State",
                    "Fresno St": "Fresno State",
                    "GA Southern": "Georgia Southern",
                    "GA Tech": "Georgia Tech",
                    "Georgia Tech Yellow": "Georgia Tech",
                    "Hawai'i Rainbow": "Hawaii",
                    "Houston U": "Houston",
                    "Illinois Fighting": "Illinois",
                    "Kansas St": "Kansas State",
                    "Kent State Golden": "Kent State",
                    "LA Lafayette": "Louisiana",
                    "Lafayette": "Louisiana",
                    "ULLafayette": "Louisiana",
                    "Louisiana Ragin'": "Louisiana",
                    "LA Monroe": "Louisiana-Monroe",
                    "UL-Monroe": "Louisiana-Monroe",
                    "ULMonroe": "Louisiana-Monroe",
                    "UL Monroe": "Louisiana-Monroe",
                    "LA Tech": "Louisiana Tech",
                    "LSU": "Louisiana State",
                    "U Mass": "Massachusetts",
                    "UMass": "Massachusetts",
                    "Miami Florida": "Miami_FL",
                    "Miami Ohio": "Miami_OH",
                    "Miami (OH)": "Miami_OH",
                    "Michigan St": "Michigan State",
                    "Middle Tenn": "Middle Tennessee State",
                    "Middle Tennessee Blue": "Middle Tennessee State",
                    "Mid Tennessee State": "Middle Tennessee State",
                    "Middle Tenn St": "Middle Tennessee State",
                    "Minnesota U": "Minnesota",
                    "Miss State": "Mississippi State",
                    "Nevada Wolf": "Nevada",
                    "N Carolina": "North Carolina",
                    "N Mex State": "New Mexico State",
                    "NC State": "North Carolina State",
                    "NCState": "North Carolina State",
                    "N Illinois": "Northern Illinois",
                    "NO Illinois": "Northern Illinois",
                    "North Carolina Tar": "North Carolina",
                    "Notre Dame Fighting": "Notre Dame",
                    "North Texas Mean": "North Texas",
                    "UNLV": "Nevada-Las Vegas",
                    "Ole Miss": "Mississippi",
                    "Oklahoma St": "Oklahoma State",
                    "Oregon St": "Oregon State",
                    "Penn State Nittany": "Penn State",
                    "Pittsburgh U": "Pittsburgh",
                    "Rutgers Scarlet": "Rutgers",
                    "San Diego St": "San Diego State",
                    "San Jose St": "San Jose State",
                    "San José State": "San Jose State",
                    "S Alabama": "South Alabama",
                    "S Carolina": "South Carolina",
                    "S Florida": "South Florida",
                    "S Methodist": "Southern Methodist",
                    "SMU": "Southern Methodist",
                    "S Mississippi": "Southern Mississippi",
                    "Southern Miss": "Southern Mississippi",
                    "UAB": "Alabama-Birmingham",
                    "USC": "Southern California",
                    "Tulsa Golden": "Tulsa",
                    "TX Christian": "Texas Christian",
                    "Texas Tech Red": "Texas Tech",
                    "TCU": "Texas Christian",
                    "TCU Horned": "Texas Christian",
                    "Tennessee U": "Tennessee",
                    "TX El Paso": "Texas-El Paso",
                    "UCF": "Central Florida",
                    "UTEP": "Texas-El Paso",
                    "TX-San Ant": "Texas-San Antonio",
                    "UTSA": "Texas-San Antonio",
                    "Tex San Antonio": "Texas-San Antonio",
                    "VA Tech": "Virginia Tech",
                    "Washington U": "Washington",
                    "W Kentucky": "Western Kentucky",
                    "W Michigan": "Western Michigan",
                    "W Virginia": "West Virginia",
                    "Wash State": "Washington State"}

    for x in range(len(fin_output['HOME_TEAM'])):
        try:
            fin_output.loc[x, 'HOME_TEAM'] = proper_names[fin_output['HOME_TEAM'][x]]
        except:
            fin_output.loc[x, 'HOME_TEAM'] = fin_output.loc[x, 'HOME_TEAM']

        try:
            fin_output.loc[x, 'WINNER'] = proper_names[fin_output['WINNER'][x]]
        except:
            fin_output.loc[x, 'WINNER'] = fin_output.loc[x, 'WINNER']

        try:
            fin_output.loc[x, 'LOSER'] = proper_names[fin_output['LOSER'][x]]
        except:
            fin_output.loc[x, 'LOSER'] = fin_output.loc[x, 'LOSER']

    return(fin_output)

#ncaa_history = get_historical_ncaa_data(['2007-08-27', '2008-08-25', '2009-08-31', '2010-08-30', '2011-08-29', '2012-08-27', '2013-08-26', '2014-08-25', '2015-08-31',
#                              '2016-08-22', '2017-08-21', '2018-08-20', '2019-08-19'], attributes =
#                                                        {'yards-per-pass-attempt': 'desc',
#                                                       'yards-per-rush-attempt': 'desc',
#                                                       'offensive-points-per-game': 'desc',
#                                                       'opponent-yards-per-pass-attempt': 'asc',
#                                                       'opponent-yards-per-rush-attempt': 'asc',
#                                                       'opponent-offensive-points-per-game': 'asc',
#                                                       'turnover-margin-per-game': 'desc',
#                                                       'predictive-by-other': 'desc',
#                                                       'schedule-strength-by-other': 'desc'}, start_week = 1)

#ncaa_history = ncaa_history.reset_index()
#for x in range(len(ncaa_history['team'])):
#    try:
#        ncaa_history.loc[x, 'team'] = proper_names[ncaa_history['team'][x]]
#    except:
#        ncaa_history.loc[x, 'team'] = ncaa_history.loc[x, 'team']

#ncaa_history = ncaa_history.set_index('team')
