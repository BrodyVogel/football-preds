import numpy as np
import pandas as pd
import datetime

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

def evaluate(data, teamA, teamB, store = False):
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

    if store == True:
        if final_score > 0:
            return([final_score, teamA])
        elif final_score < 0:
            return([-1 * final_score, teamB])
        else:
            return([final_score, 'Neither'])

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

stat_history = get_historical_nfl_data(start_dates = ['2015-10-07', '2016-10-05', '2017-10-04', '2018-10-03', '2019-10-02'],
                                       start_week = 5,
                                       attributes={'yards-per-pass-attempt': 'desc',
                                                   'yards-per-rush-attempt': 'desc',
                                                   'offensive-points-per-game': 'desc',
                                                   'opponent-yards-per-pass-attempt': 'asc',
                                                   'opponent-yards-per-rush-attempt': 'asc',
                                                   'opponent-offensive-points-per-game': 'asc',
                                                   'turnover-margin-per-game': 'desc',
                                                   'predictive-by-other': 'desc'}
                                       )

#history = get_historical_nfl_results([2015, 2016, 2017, 2018, 2019])

#to_eval = history.loc[history['Week'] > 4]

#to_eval['pred_winner'] = 'Neither'
#to_eval['confidence'] = np.nan

#to_eval = to_eval.replace("St. Louis", "LA Rams")
#to_eval = to_eval.replace("Oakland", "Las Vegas")
#to_eval = to_eval.replace("San Diego", "LA Chargers")

#to_eval = to_eval.reset_index(drop = True)

#for row in range(len(to_eval['Home_Team'])):
#    week_to_locate = to_eval['Week'][row]
#    year_to_locate = to_eval['Year'][row]
#    to_eval.loc[row, 'confidence'] = evaluate(stat_history.loc[(stat_history['Year'] == year_to_locate) & (stat_history['Week'] == week_to_locate)],
#                                        to_eval['Winner'][row], to_eval['Loser'][row], store = True)[0]
#    to_eval.loc[row, 'pred_winner'] = evaluate(stat_history.loc[(stat_history['Year'] == year_to_locate) & (stat_history['Week'] == week_to_locate)],
#                                        to_eval['Winner'][row], to_eval['Loser'][row], store = True)[1]

#to_eval['Correct'] = to_eval['Winner'] == to_eval['pred_winner']

#we_were_right = to_eval.loc[to_eval['Correct'] == 1]
#we_were_right.groupby('confidence')['Margin_of_Victory'].median()

#we_were_wrong = to_eval.loc[to_eval['Correct'] == 0]
#we_were_wrong.groupby('confidence')['Margin_of_Victory'].summarize()

#we_did_know = to_eval.loc[to_eval['confidence'] > 2]
#we_did_know.groupby('Year')['Correct'].apply(lambda x: x.sum() / len(x))