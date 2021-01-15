from get_data import *
from importlib import reload

analysis = get_data_nfl(date = '2020-01-13', attributes = {'yards-per-pass-attempt': 'desc',
                                                       'yards-per-rush-attempt': 'desc',
                                                       'offensive-points-per-game': 'desc',
                                                       'opponent-yards-per-pass-attempt': 'asc',
                                                       'opponent-yards-per-rush-attempt': 'asc',
                                                       'opponent-offensive-points-per-game': 'asc',
                                                       'turnover-margin-per-game': 'desc',
                                                       'predictive-by-other': 'desc',
                                                       'schedule-strength-by-other': 'desc'})

analysis_ncaa = get_data_ncaaf(date = '2021-01-10', attributes = {'yards-per-pass-attempt': 'desc',
                                                       'yards-per-rush-attempt': 'desc',
                                                       'offensive-points-per-game': 'desc',
                                                       'opponent-yards-per-pass-attempt': 'asc',
                                                       'opponent-yards-per-rush-attempt': 'asc',
                                                       'opponent-offensive-points-per-game': 'asc',
                                                       'turnover-margin-per-game': 'desc',
                                                       'predictive-by-other': 'desc',
                                                       'schedule-strength-by-other': 'desc'})

factor_policy = {
    "turnover-margin-per-game_rank":
        {"one_point": [55.5, 60],
         "two_points": [84.5, 71],
         "three_points": None,
         "two_fac": None},

    "predictive-by-other_rank":
        {"one_point": [15.5, 21.5],
         "two_points": [28.5, 35],
         "three_points": [44.5, 56],
         "two_fac": None},

    "total_rush_offense":
        {"one_point": [43.5, 54],
         "two_points": [66.5, 83.5],
         "three_points": None,
         "two_fac": ['yards-per-rush-attempt_rank', 'opponent-yards-per-rush-attempt_rank']},

    "total_rush_defense":
        {"one_point": [43.5, 54],
         "two_points": [66.5, 82],
         "three_points": None,
         "two_fac": ['opponent-yards-per-rush-attempt_rank', 'yards-per-rush-attempt_rank']},

    "total_pass_defense":
        {"one_point": [43, 52.5],
         "two_points": [83, 127],
         "three_points": None,
         "two_fac": ['opponent-yards-per-pass-attempt_rank', 'yards-per-pass-attempt_rank']},

    "total_pass_offense":
        {"one_point": [43.5, 53],
         "two_points": [83, 127],
         "three_points": None,
         "two_fac": ['yards-per-pass-attempt_rank', 'opponent-yards-per-pass-attempt_rank']}
}

sos_adjusted_analysis_ncaa = adjust_sos(analysis_ncaa, 'schedule-strength-by-other_rank', magnitude = 8)

sos_adjusted_nfl = adjust_sos(analysis, 'schedule-strength-by-other_rank', magnitude = 4)

evaluate(analysis_ncaa, 'Ohio State', 'Alabama', size=12)
evaluate_v2(analysis_ncaa, 'Ohio State', 'Alabama', factor_policy = factor_policy, verbose = True, spread_target = [nopq])
evaluate(sos_adjusted_analysis_ncaa, 'Ohio State', 'Alabama', size=12)
evaluate_v2(sos_adjusted_analysis_ncaa, 'Ohio State', 'Alabama', factor_policy = factor_policy, verbose = True, spread_target = None)

evaluate(analysis, 'Baltimore', 'Buffalo', size = 8)
evaluate(sos_adjusted_nfl, 'Baltimore', 'Buffalo', size = 8)

bowl = get_ncaa_schedule(17)

for game in range(len(bowl['Home Team'])):

    try:
        evaluate(sos_adjusted_analysis_ncaa, bowl['Home Team'][game], bowl['Away Team'][game], size=12)
        print("\n")
        evaluate_v2(sos_adjusted_analysis_ncaa, bowl['Home Team'][game], bowl['Away Team'][game], factor_policy = factor_policy,
                    verbose = True, spread_target = [nopq])
    except:
        home_team = bowl.loc[game, 'Away Team'].split("vs.")[0].strip()
        away_team = bowl.loc[game, 'Away Team'].split("vs.")[1].strip()

        evaluate(sos_adjusted_analysis_ncaa, home_team, away_team, size=12)
        print("\n")
        evaluate_v2(sos_adjusted_analysis_ncaa, home_team, away_team, factor_policy = factor_policy,
                    verbose = True, spread_target = [nopq])
    print('\n\n')

evaluate(analysis_ncaa, 'Fresno St', 'New Mexico', size=12)
print("\n")
evaluate_v2(analysis_ncaa, 'Fresno St', 'New Mexico', factor_policy = factor_policy,
                    verbose = True, spread_target = [nopq])


# Week 4
## 11-3

# Week 5
## 8-6

# Week 6
## 10-4


# Week 9
##
# San Francisco > GB (3)
# Tennessee > Chicago (4)
# Seattle > Buffalo (4)
# Houston > Jacksonville (2)
# Baltimore > Indianapolis (2)
# Atlanta > Denver (1)
# Kansas City > Carolina (2)
# NY Giants > Washington (1)
# Detroit == Minnesota
# LA Chargers > Las Vegas (3)
# Arizona > Miami (2)
# Pittsburgh > Dallas (5)
# Tampa Bay > New Orleans (2)
# New England > NY Jets (2)

week_17 = get_nfl_schedule(17)

for row in range(len(week_17)):
    try:
        print(week_17.iloc[row, :]['Away_Team'], '@', week_17.iloc[row, :]['Home_Team'])
        evaluate(sos_adjusted_nfl, week_17.iloc[row, :]['Away_Team'], week_17.iloc[row, :]['Home_Team'], size = 8)
        print('\n\n')
    except:
        continue

stat_history = get_historical_nfl_data(start_dates = ['2012-10-10', '2013-10-09', '2014-10-08', '2015-10-07', '2016-10-05', '2017-10-04', '2018-10-03', '2019-10-02'],
                                       start_week = 5,
                                       attributes={'yards-per-pass-attempt': 'desc',
                                                   'yards-per-rush-attempt': 'desc',
                                                   'offensive-points-per-game': 'desc',
                                                   'opponent-yards-per-pass-attempt': 'asc',
                                                   'opponent-yards-per-rush-attempt': 'asc',
                                                   'opponent-offensive-points-per-game': 'asc',
                                                   'turnover-margin-per-game': 'desc',
                                                   'predictive-by-other': 'desc',
                                                   'schedule-strength-by-other': 'desc'}
                                       )

history = get_historical_nfl_results([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019])

sos_history = adjust_sos(stat_history, 'schedule-strength-by-other_rank', magnitude=3, group_columns=['Year', 'Week'])

to_eval = history.loc[history['Week'] > 4]

to_eval['pred_winner'] = 'Neither'
to_eval['confidence'] = np.nan
to_eval['pred_winner_advantages'] = np.nan
to_eval['pred_loser_advantages'] = np.nan

to_eval = to_eval.replace("St. Louis", "LA Rams")
to_eval = to_eval.replace("Oakland", "Las Vegas")
to_eval = to_eval.replace("San Diego", "LA Chargers")

to_eval = to_eval.reset_index(drop = True)

to_eval_2 = to_eval.copy()

for row in range(len(to_eval_2['Home_Team'])):
    week_to_locate = to_eval_2['Week'][row]
    year_to_locate = to_eval_2['Year'][row]
    try:
        to_eval_2.loc[row, 'confidence'] = evaluate(stat_history.loc[(stat_history['Year'] == year_to_locate) & (stat_history['Week'] == week_to_locate)],
                                        to_eval_2['Winner'][row], to_eval_2['Loser'][row], size = 8, store = True)[2]
        to_eval_2.loc[row, 'pred_winner'] = evaluate(stat_history.loc[(stat_history['Year'] == year_to_locate) & (stat_history['Week'] == week_to_locate)],
                                        to_eval_2['Winner'][row], to_eval_2['Loser'][row], size = 8, store = True)[3]

        to_eval_2.loc[row, 'pred_winner_advantages'] = evaluate(stat_history.loc[(stat_history['Year'] == year_to_locate) & (stat_history['Week'] == week_to_locate)],
                 to_eval_2['Winner'][row], to_eval_2['Loser'][row], size=8, store=True)[0]
        to_eval_2.loc[row, 'pred_loser_advantages'] = \
        evaluate(stat_history.loc[(stat_history['Year'] == year_to_locate) & (stat_history['Week'] == week_to_locate)],
                 to_eval_2['Winner'][row], to_eval_2['Loser'][row], size=8, store=True)[1]

    except:
        to_eval_2.loc[row, 'confidence'] = np.nan
        to_eval_2.loc[row, 'pred_winner'] = np.nan
        to_eval_2.loc[row, 'pred_winner_advantages'] = np.nan
        to_eval_2.loc[row, 'pred_loser_advantages'] = np.nan

r = to_eval_2.loc[to_eval_2.confidence > 0].groupby(['Year', 'confidence'])['Correct'].mean()

to_eval_2['Margin_of_Victory_pred_winner'] = np.nan
for x in range(len(to_eval_2['Winner'])):
    if to_eval_2['pred_winner'][x] == to_eval_2['Winner'][x] or to_eval_2['pred_winner'][x] == 'Neither':
        to_eval_2.loc[x, 'Margin_of_Victory_pred_winner'] = to_eval_2['Margin_of_Victory'][x]
    elif type(to_eval_2['pred_winner'][x]) == float and np.isnan(to_eval_2['pred_winner'][x]) == True:
        to_eval_2.loc[x, 'Margin_of_Victory_pred_winner'] = to_eval_2['Margin_of_Victory'][x]
    else:
        to_eval_2.loc[x, 'Margin_of_Victory_pred_winner'] = -1 * to_eval_2['Margin_of_Victory'][x]

n = to_eval_2.groupby(['confidence'])['Margin_of_Victory_pred_winner'].describe(percentiles = [0.05, 0.1, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.90, 0.95])
o = to_eval_2.groupby(['confidence', 'pred_winner_advantages'])['Margin_of_Victory_pred_winner'].describe(percentiles = [0.05, 0.1, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.90, 0.95])



to_eval_2['Correct'] = to_eval_2['Winner'] == to_eval_2['pred_winner']

we_were_right = to_eval_2.loc[to_eval_2['Correct'] == 1]
we_were_right.groupby('confidence')['Margin_of_Victory'].describe()

we_were_wrong = to_eval_2.loc[to_eval_2['Correct'] == 0]
we_were_wrong.groupby('confidence')['Margin_of_Victory'].describe()

#we_did_know = to_eval.loc[to_eval['confidence'] > 2]
#we_did_know.groupby('Year')['Correct'].apply(lambda x: x.sum() / len(x))

out_data = pd.DataFrame({'Year': [], 'Week': [], 'Home_Team': [], 'Away_Team': [], 'Winner': [],
                         'Pts_Winner': [], 'Pts_Loser': [], 'Margin_of_Victory': []})

for t in range(2010, 2020):
    z = pd.read_html('https://www.sports-reference.com/cfb/years/' + str(t) + '-schedule.html', flavor = 'html5lib')[0]

    z = z.replace(to_replace = '\(.?.?\).?', value = "", regex = True)

    z = z.loc[z.Wk != 'Wk'].reset_index(drop = True)

    try:
        z = z.drop(columns = ['Time', 'Rk', 'Date', 'Day', 'Notes'])

    except:
        z = z.drop(columns = ['Rk', 'Date', 'Day', 'Notes'])


    z.columns = ['Week', 'Winner', 'Pts_Winner', 'where', 'Loser', 'Pts_Loser']

    z['Home_Team'] = np.asarray([z['Winner'][x] if z['where'][x] != "@" else z['Loser'][x]
                            for x in range(len(z['Winner']))])

    z['Away_Team'] = np.asarray([z['Loser'][x] if z['where'][x] != "@" else z['Winner'][x]
                            for x in range(len(z['Winner']))])

    z['Pts_Winner'] = z['Pts_Winner'].astype('float')
    z['Pts_Loser'] = z['Pts_Loser'].astype('float')

    z = z[['Week', 'Home_Team', 'Away_Team', 'Winner', 'Pts_Winner', 'Pts_Loser']]

    z['Margin_of_Victory'] = z['Pts_Winner'] - z['Pts_Loser']

    z['Year'] = t

    print(t)

    out_data = pd.concat([out_data, z])

        
reset_fin_output = fin_output.copy()

reset_fin_output['pred_winner'] = 'Neither'
reset_fin_output['confidence'] = np.nan
#reset_fin_output['home_team_advantages'] = np.nan
#reset_fin_output['away_team_advantages'] = np.nan

reset_fin_output['three_advantages'] = np.nan
reset_fin_output['two_advantages'] = np.nan
reset_fin_output['one_advantages'] = np.nan
reset_fin_output['half_advantages'] = np.nan

to_test = reset_fin_output.copy().reset_index(drop = True)

reset_ncaa_history = ncaa_history.copy()

for row in range(len(to_test['WINNER'])):
    date_to_locate = to_test['DATE'][row]
    try:
        to_test.loc[row, 'one_advantages'], to_test.loc[row, 'three_advantages'], to_test.loc[row, 'confidence'],\
        to_test.loc[row, 'pred_winner'] = evaluate_v2(reset_ncaa_history.loc[(reset_ncaa_history['Date'] == date_to_locate)],
                 to_test['WINNER'][row], to_test['LOSER'][row], factor_policy=factor_policy, magnitude=25, store=True, grouping = 'overall')

    except:
        to_test.loc[row, 'three_advantages'] = np.nan
        to_test.loc[row, 'two_advantages'] = np.nan
        to_test.loc[row, 'one_advantages'] = np.nan
        to_test.loc[row, 'half_advantages'] = np.nan
        to_test.loc[row, 'pred_winner'] = np.nan
        to_test.loc[row, 'confidence'] = np.nan

to_test_evaluate = to_test.loc[np.isnan(to_test.confidence) == False].reset_index(drop = True)
to_test_evaluate = to_test_evaluate.loc[to_test_evaluate.pred_winner != 'Neither'].reset_index(drop = True)

to_test_evaluate['MARGIN_OF_VICTORY_pred_winner'] = np.nan
for x in range(len(to_test_evaluate['WINNER'])):
    if to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x] or to_test_evaluate['pred_winner'][x] == 'Neither':
        to_test_evaluate.loc[x, 'MARGIN_OF_VICTORY_pred_winner'] = to_test_evaluate['MARGIN_OF_VICTORY'][x]
    elif type(to_test_evaluate['pred_winner'][x]) == float and np.isnan(to_test_evaluate['pred_winner'][x]) == True:
        to_test_evaluate.loc[x, 'MARGIN_OF_VICTORY_pred_winner'] = to_test_evaluate['MARGIN_OF_VICTORY'][x]
    else:
        to_test_evaluate.loc[x, 'MARGIN_OF_VICTORY_pred_winner'] = -1 * to_test_evaluate['MARGIN_OF_VICTORY'][x]

to_test_evaluate.groupby(['confidence'])['MARGIN_OF_VICTORY_pred_winner'].describe()

to_test_evaluate['WON'] = to_test_evaluate.MARGIN_OF_VICTORY_pred_winner > 0

to_test_evaluate.groupby('confidence').WON.mean()

to_test_evaluate['grouped_confidence'] = to_test_evaluate['confidence'].transform(
                     lambda x: pd.qcut(x, 20, labels = False, duplicates='drop'))

n = to_test_evaluate.groupby(['grouped_confidence'])['MARGIN_OF_VICTORY_pred_winner'].describe(percentiles = [0.05, 0.1, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.90, 0.95])
p = n[['25%', '40%', '50%', '75%', '90%']]
q = to_test_evaluate.groupby(['grouped_confidence'])['confidence'].describe()[['min', 'max']]
o = to_test_evaluate.groupby(['confidence', 'pred_winner_advantages'])['Margin_of_Victory_pred_winner'].describe(percentiles = [0.05, 0.1, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.90, 0.95])

q = q.reset_index()
p = p.reset_index()

nopq = pd.merge(q, p)


to_test_evaluate['OPEN_SPREAD_pred_winner'] = [
    to_test_evaluate['OPEN_SPREAD_WINNER'][x] if to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x]
    else to_test_evaluate['OPEN_SPREAD_LOSER'][x] if to_test_evaluate['pred_winner'][x] == to_test_evaluate['LOSER'][x]
    else np.nan for x in range(len(to_test_evaluate['DATE']))]

to_test_evaluate['CLOSE_SPREAD_pred_winner'] = [
    to_test_evaluate['CLOSE_SPREAD_WINNER'][x] if to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x]
    else to_test_evaluate['CLOSE_SPREAD_LOSER'][x] if to_test_evaluate['pred_winner'][x] == to_test_evaluate['LOSER'][x]
    else np.nan for x in range(len(to_test_evaluate['DATE']))]

to_test_evaluate['COVERED_OPEN_pred_winner'] = np.asarray([
    np.nan if np.isnan(to_test_evaluate['OPEN_SPREAD_pred_winner'][x]) == True
    else 1 if (to_test_evaluate['OPEN_SPREAD_pred_winner'][x] > 0) & (to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x])
    else 1 if (to_test_evaluate['MARGIN_OF_VICTORY'][x] > (-1 * to_test_evaluate['OPEN_SPREAD_pred_winner'][x])) & (to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x])
    else 1 if (to_test_evaluate['MARGIN_OF_VICTORY'][x] < (-1 * to_test_evaluate['OPEN_SPREAD_pred_winner'][x])) & (to_test_evaluate['pred_winner'][x] == to_test_evaluate['LOSER'][x])
    else 0 for x in range(len(to_test_evaluate['DATE']))])

to_test_evaluate['COVERED_CLOSE_pred_winner'] = np.asarray([
    np.nan if np.isnan(to_test_evaluate['CLOSE_SPREAD_pred_winner'][x]) == True
    else 1 if (to_test_evaluate['CLOSE_SPREAD_pred_winner'][x] > 0) & (to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x])
    else 1 if (to_test_evaluate['MARGIN_OF_VICTORY'][x] > (-1 * to_test_evaluate['CLOSE_SPREAD_pred_winner'][x])) & (to_test_evaluate['pred_winner'][x] == to_test_evaluate['WINNER'][x])
    else 1 if (to_test_evaluate['MARGIN_OF_VICTORY'][x] < (-1 * to_test_evaluate['CLOSE_SPREAD_pred_winner'][x])) & (to_test_evaluate['pred_winner'][x] == to_test_evaluate['LOSER'][x])
    else 0 for x in range(len(to_test_evaluate['DATE']))])

def spread_level(x):
    if x < -35:
        return 'a < -35'
    elif -35 <= x < -30:
        return 'b -35/-30.5'
    elif -30 <= x < -25:
        return 'c -30/-25.5'
    elif -25 <= x < -20:
        return 'd -25/-20.5'
    elif -20 <= x < -15:
        return 'e -20/-15.5'
    elif -15 <= x < -10:
        return 'f -15/-10.5'
    elif -10 <= x < -6.5:
        return 'g -10/-7'
    elif -6.5 <= x < -4:
        return 'h -6.5/-4.5'
    elif -4 <= x < -2.5:
        return 'i -4/-3'
    elif -2.5 <= x < 0:
        return 'j -3/-0.5'
    elif 0 <= x < 3:
        return 'k 0/2.5'
    elif 3 <= x < 4.5:
        return 'k 3/4'
    elif 4.5 <= x < 7:
        return 'l 4.5/6.5'
    elif 7 <= x < 10.5:
        return 'm 7/10'
    elif 10.5 <= x < 15.5:
        return 'n 10.5/15'
    elif 15.5 <= x < 20.5:
        return 'o 15.5/20'
    elif 20.5 <= x < 25.5:
        return 'p 20.5/25'
    elif 25.5 <= x < 30.5:
        return 'q 25.5/30'
    elif 30.5 <= x < 35:
        return 'r 30.5/35'
    elif x >= 35:
        return 's > 35'
    else:
        return 'N/A'

to_test_evaluate['OPEN_SPREAD_pred_winner_BASKET'] = to_test_evaluate['OPEN_SPREAD_pred_winner'].apply(spread_level)
to_test_evaluate['CLOSE_SPREAD_pred_winner_BASKET'] = to_test_evaluate['CLOSE_SPREAD_pred_winner'].apply(spread_level)

to_test_evaluate['OPEN_SPREAD_BASKET'] = to_test_evaluate['OPEN_SPREAD'].apply(spread_level)
to_test_evaluate['CLOSE_SPREAD_BASKET'] = to_test_evaluate['CLOSE_SPREAD'].apply(spread_level)

to_test_evaluate['month'] = np.asarray([float(to_test_evaluate['DATE'][x][5:7]) for x in range(len(to_test_evaluate['DATE']))])
to_test_evaluate = to_test_evaluate.loc[to_test_evaluate.month > 9]

to_test_evaluate['CLOSE_RAW_SPREAD'] = to_test_evaluate['CLOSE_SPREAD_LOSER'].abs()

to_test_evaluate['CLOSE_RAW_SPREAD_BASKET'] = to_test_evaluate['CLOSE_RAW_SPREAD'].apply(spread_level)

to_test_evaluate['CLOSE_SPREAD_DECILE_BY_CONFIDENCE'] = to_test_evaluate.groupby(['confidence'])['CLOSE_RAW_SPREAD'].transform(
                     lambda x: pd.qcut(x, 10, labels = False, duplicates='drop'))

to_test_evaluate['CLOSE_SPREAD_pred_winner_DECILE_BY_CONFIDENCE'] = to_test_evaluate.groupby(['confidence'])['CLOSE_SPREAD_pred_winner'].transform(
                     lambda x: pd.qcut(x, 5, labels = False, duplicates='drop'))

to_test_evaluate['CLOSE_SPREAD_pred_winner_DECILE'] = pd.qcut(to_test_evaluate['CLOSE_SPREAD_pred_winner'], 10, labels = False, duplicates='drop')

lm = to_test_evaluate.groupby(['confidence', 'CLOSE_SPREAD_pred_winner_BASKET'])['COVERED_CLOSE_pred_winner'].mean()
m = to_test_evaluate.groupby(['confidence', 'CLOSE_SPREAD_pred_winner_DECILE'])['COVERED_CLOSE_pred_winner'].mean()

ab = to_test_evaluate.groupby(['confidence', 'CLOSE_SPREAD_pred_winner_BASKET'])['COVERED_CLOSE_pred_winner'].mean()
ac = to_test_evaluate.groupby(['confidence', 'CLOSE_SPREAD_pred_winner_BASKET'])['COVERED_CLOSE_pred_winner'].count()



abc = pd.DataFrame({'avg': ab, 'count': ac})

abc = abc.reset_index()

d = to_test_evaluate.groupby('')

out_data_3['Margin_of_Victory_pred_winner'] = np.nan
for x in range(len(out_data_3['Winner'])):
    if out_data_3['pred_winner'][x] == out_data_3['Winner'][x] or out_data_3['pred_winner'][x] == 'Neither':
        out_data_3.loc[x, 'Margin_of_Victory_pred_winner'] = out_data_3['Margin_of_Victory'][x]
    elif type(out_data_3['pred_winner'][x]) == float and np.isnan(out_data_3['pred_winner'][x]) == True:
        out_data_3.loc[x, 'Margin_of_Victory_pred_winner'] = out_data_3['Margin_of_Victory'][x]
    else:
        out_data_3.loc[x, 'Margin_of_Victory_pred_winner'] = -1 * out_data_3['Margin_of_Victory'][x]

out_data_3['Correct'] = out_data_3['Winner'] == out_data_3['pred_winner']

out_data_3.loc[out_data_3.confidence > 0].groupby('Week')['Correct'].mean()

right = out_data_3.loc[out_data_3.Correct == 1]
wrong = out_data_3.loc[(out_data_3.Correct == 0) & (out_data_3.confidence > 0)]
l = out_data_3.groupby(['confidence', 'pred_winner_advantages'])['Margin_of_Victory_pred_winner'].describe(percentiles = [0.05, 0.1, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.90, 0.95])
wrong.groupby('confidence')['Margin_of_Victory'].describe()

# No-Brainer (75%) / Good Bet (60%) / Better Than Chance (50%)
# 0: 75% chance game is between 22.5
#    60% chance game is between 15
#    50% chance game is between 11
#    30% chance game is within 7
#    25% chance game is within 5

# 1: +7.5 / +2.5 / -2.5
#    -14.5 / -7.5 / -3.5

# 2: +6.5 / -1.5 / -4.5
#    -17.5 / -8.5 / -5.5

# 3: +4.5 / -2.5 / -6.5
#    -20.5 / -10.5 / -7.5

# 4: +1.5 / -4.5 / -7.5
#    -21.5 / -13.5 / -8.5

# 5: +1.5 / -6.5 / -10.5
#    -24.5 / -17.5 / -11.5

# 6: -4.5 / -11.5 / -16.5
#    -29.5 / -21.5 / -17.5

# 7: -4.5 / -13.5 / -17.5
#    -31.5 / -23 / -18.5

# 8: -9.5 / -17.5 / -22.5
#    -37.5 / -28.5 / -23.5

# No-Brainer NFL (75%) / Good Bet (60%) / Better Than Chance (50%)
# 0: 75% chance game is within 14
#    60% chance game is within 10
#    50% chance game is within 7
#    30% chance game is within 4
#    25% chance game is within 3

# 1: +6.5 / +1.5 / -2.5
#    -8.5 / -4.5 / -3.5

# 2: +5.5 / +1.5 / -2.5
#    -13.5 / -7.5 / -3.5

# 3: +3.5 / -2.5 / -5.5
#    -16.5 / -8.5 / -6.5

# 4: +3.5 / -2.5 / -6.5
#    -16.5 / -10.5 / -7.5

# 5: -2.5 / -4.5 / -8
#    -18.5 / -13.5 / -9

# 6: -2.5 / -6 / -12.5
#    -21.5 / -15.5 / -13.5

# 7: -5.5 / -9 / -13
#    -25 / -17.5 / -14

# 8: -6.5 / -9 / -13
#    -25 / -17.5 / -14


z = pd.read_html('https://www.espn.com/college-football/lines', flavor = 'html5lib')

spreads = pd.DataFrame({'AWAY_TEAM': [], 'HOME_TEAM': [], 'SPREAD_AWAY': [],  'SPREAD_HOME': [], 'ML_AWAY': [], 'ML_HOME': []})

for t in range(len(z)):
    frame = z[t]
    frame.columns = ['TEAMS', 'REC', 'LINE', 'ML', 'FPI']
    away_team = frame['TEAMS'][0]
    away_team = " ".join(away_team.split(" ")[:-1])
    home_team = frame['TEAMS'][1]
    home_team = " ".join(home_team.split(" ")[:-1])
    line = frame['LINE'].min()
    if frame['LINE'][0] > frame['LINE'][1]:
        spread_away = -1 * line
        spread_home = line
    else:
        spread_away = line
        spread_home = -1 * line
    ml_away = frame['ML'][0]
    ml_home = frame['ML'][1]

    new_row = {'AWAY_TEAM': away_team, 'HOME_TEAM': home_team, 'SPREAD_AWAY': spread_away,
               'SPREAD_HOME': spread_home, 'ML_AWAY': ml_away, 'ML_HOME': ml_home}

    spreads = spreads.append(new_row, ignore_index=True)

for x in range(len(spreads['HOME_TEAM'])):
    try:
        spreads.loc[x, 'HOME_TEAM'] = proper_names[spreads['HOME_TEAM'][x]]
    except:
        spreads.loc[x, 'HOME_TEAM'] = spreads.loc[x, 'HOME_TEAM']

    try:
        spreads.loc[x, 'AWAY_TEAM'] = proper_names[spreads['AWAY_TEAM'][x]]
    except:
        spreads.loc[x, 'AWAY_TEAM'] = spreads.loc[x, 'AWAY_TEAM']

spreads = spreads.replace('--', np.nan)
spreads = spreads.replace('', np.nan)