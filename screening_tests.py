import numpy as np
import pandas as pd
import datetime

def win_breakdown(stats = None, results = None, factor = 'bs'):

    #factor = 'schedule-strength-by-other_rank'
    #factor = 'turnover-margin-per-game_rank'
    #factor = 'opponent-offensive-points-per-game_rank'
    factor = 'opponent-yards-per-rush-attempt_rank'
    #factor = 'opponent-yards-per-pass-attempt_rank'
    #factor = 'offensive-points-per-game_rank'
    #factor = 'yards-per-rush-attempt_rank'
    #factor = 'yards-per-pass-attempt_rank'
    #factor = 'predictive-by-other_rank'



    z = ncaa_history.copy()

    z = z.reset_index()

    y = fin_output.copy()

    y = pd.merge(y, z[['team', 'Date', factor]], left_on = ['DATE', 'WINNER'], right_on = ['Date', 'team'], how = 'left')

    y = pd.merge(y, z[['team', 'Date', factor]], left_on = ['DATE', 'LOSER'], right_on = ['Date', 'team'], how = 'left')

    y = y[['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', factor + '_x', factor + '_y']]

    y.columns = ['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', factor + '_WINNER', factor + '_LOSER']

    y = y.dropna().reset_index(drop = True)

    y['ADV_WON'] = [1 if y[factor + '_WINNER'][x] < y[factor + '_LOSER'][x] else 0 for x in range(len(y['WINNER']))]

    y['ADV'] = y[factor + '_LOSER'] - y[factor + '_WINNER']

    y['ADV'] = y['ADV'].abs()

    y['ADV_BUCKET'] = y['ADV'].transform(
                     lambda x: pd.qcut(x, 10, duplicates='drop', labels = False))

    y['MARGIN_OF_VICTORY_ADV'] = [y['MARGIN_OF_VICTORY'][x] if y['ADV_WON'][x] == 1
                                  else -1 * y['MARGIN_OF_VICTORY'][x]
                                  for x in range(len(y['WINNER']))]

    print("Percentage of Games Won by Team with Advantage:", y['ADV_WON'].mean())
    print("Break Points for Baskets:", y.groupby('ADV_BUCKET')['ADV'].describe()[['min', 'max']])
    print("Percentage of Games Won by Team with Cascading Advantage Size:", y.groupby('ADV_BUCKET')['ADV_WON'].mean())
    print("Margin of Victory with Cascading Advantage Size: \n", y.groupby('ADV_BUCKET')['MARGIN_OF_VICTORY_ADV'].describe())


def win_breakdown_two_factors(stats, results, factors):
    # factor = 'schedule-strength-by-other_rank'
    # factor = 'turnover-margin-per-game_rank'
    # factor = 'opponent-offensive-points-per-game_rank'
    # factor = 'opponent-yards-per-rush-attempt_rank'
    # factor = 'opponent-yards-per-pass-attempt_rank'
    # factor = 'offensive-points-per-game_rank'
    # factor = 'yards-per-rush-attempt_rank'
    # factor = 'yards-per-pass-attempt_rank'
    # factor = 'predictive-by-other_rank'

    #factors = ['opponent-offensive-points-per-game_rank', 'offensive-points-per-game_rank']
    #factors = ['offensive-points-per-game_rank', 'opponent-offensive-points-per-game_rank']
    #factors = ['yards-per-rush-attempt_rank', 'opponent-yards-per-rush-attempt_rank']
    #factors = ['opponent-yards-per-rush-attempt_rank', 'yards-per-rush-attempt_rank']
    factors = ['opponent-yards-per-pass-attempt_rank', 'yards-per-pass-attempt_rank']
    #factors = ['yards-per-pass-attempt_rank', 'opponent-yards-per-pass-attempt_rank']

    factor_good = factors[0]
    factor_bad = factors[1]

    z = ncaa_history.copy()

    z = z.reset_index()

    y = fin_output.copy()

    y = pd.merge(y, z[['team', 'Date', factor_good]], left_on=['DATE', 'WINNER'], right_on=['Date', 'team'], how='left')

    y = pd.merge(y, z[['team', 'Date', factor_bad]], left_on=['DATE', 'LOSER'], right_on=['Date', 'team'], how='left')

    y = y[['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', factor_good, factor_bad]]

    y.columns = ['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', factor_good,
                 factor_bad]

    y = y.dropna().reset_index(drop=True)

    y['ADV_WON'] = [1 if y[factor_good][x] < y[factor_bad][x] else 0 for x in range(len(y['WINNER']))]

    y['ADV'] = y[factor_bad] - y[factor_good]

    y['ADV'] = y['ADV'].abs()

    y['ADV_BUCKET'] = y['ADV'].transform(
        lambda x: pd.qcut(x, 10, duplicates='drop', labels=False))

    y['MARGIN_OF_VICTORY_ADV'] = [y['MARGIN_OF_VICTORY'][x] if y['ADV_WON'][x] == 1
                                  else -1 * y['MARGIN_OF_VICTORY'][x]
                                  for x in range(len(y['WINNER']))]

    print("Percentage of Games Won by Team with Advantage:", y['ADV_WON'].mean())
    print("Break Points for Baskets:", y.groupby('ADV_BUCKET')['ADV'].describe()[['min', 'max']])
    print("Percentage of Games Won by Team with Cascading Advantage Size:", y.groupby('ADV_BUCKET')['ADV_WON'].mean())
    print("Margin of Victory with Cascading Advantage Size: \n",
          y.groupby('ADV_BUCKET')['MARGIN_OF_VICTORY_ADV'].describe())

def factor_overlap(factors):
    stats = ncaa_history.copy()
    results = fin_output.copy()

    stats = stats.reset_index()

    if (type(factors[1]) is str) == False:
        factor_good_a = factors[0][0]
        factor_bad_a = factors[0][1]

        factor_good_b = factors[1][0]
        factor_bad_b = factors[1][1]

        results = pd.merge(results, stats[['team', 'Date', factor_good_a]], left_on=['DATE', 'WINNER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factor_bad_a]], left_on=['DATE', 'LOSER'],
                           right_on=['Date', 'team'], how='left')

        results['two-factor-adv-a'] = results[factor_bad_a] - results[factor_good_a]

        results = results.drop(columns = [factor_bad_a, factor_good_a])

        results = pd.merge(results, stats[['team', 'Date', factor_good_b]], left_on=['DATE', 'WINNER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factor_bad_b]], left_on=['DATE', 'LOSER'],
                           right_on=['Date', 'team'], how='left')

        results['two-factor-adv-b'] = results[factor_bad_b] - results[factor_good_b]

        results = results.drop(columns=[factor_bad_b, factor_good_b])

        results = results[['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', 'two-factor-adv-a',
                           'two-factor-adv-b']]

        results = results.dropna().reset_index(drop=True)

        results['ADV_A_WON'] = [1 if results['two-factor-adv-a'][x] > 0 else 0 for x in range(len(results['WINNER']))]

        results['ADV_A'] = results['two-factor-adv-a']

        results['ADV_A'] = results['ADV_A'].abs()

        results['ADV_A_BUCKET'] = results['ADV_A'].transform(
            lambda x: pd.qcut(x, 5, duplicates='drop', labels=False))

        results['MARGIN_OF_VICTORY_ADV_A'] = [results['MARGIN_OF_VICTORY'][x] if results['ADV_A_WON'][x] == 1
                                              else -1 * results['MARGIN_OF_VICTORY'][x]
                                              for x in range(len(results['WINNER']))]

        results['ADV_B_WON'] = [1 if results['two-factor-adv-b'][x] > 0 else 0 for x in range(len(results['WINNER']))]

        results['ADV_B'] = results['two-factor-adv-b']

        results['ADV_B'] = results['ADV_B'].abs()

        results['ADV_B_BUCKET'] = results['ADV_B'].transform(
            lambda x: pd.qcut(x, 5, duplicates='drop', labels=False))

        results['MARGIN_OF_VICTORY_ADV_B'] = [results['MARGIN_OF_VICTORY'][x] if results['ADV_B_WON'][x] == 1
                                              else -1 * results['MARGIN_OF_VICTORY'][x]
                                              for x in range(len(results['WINNER']))]


    elif (type(factors[0]) is str) == False:

        print('YES')
        factor_good = factors[0][0]
        factor_bad = factors[0][1]

        results = pd.merge(results, stats[['team', 'Date', factor_good]], left_on=['DATE', 'WINNER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factor_bad]], left_on=['DATE', 'LOSER'],
                           right_on=['Date', 'team'], how='left')

        results['two-factor-adv'] = results[factor_bad] - results[factor_good]

        results = results.drop(columns = [factor_good, factor_bad])

        results = pd.merge(results, stats[['team', 'Date', factors[1]]], left_on=['DATE', 'WINNER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factors[1]]], left_on=['DATE', 'LOSER'],
                           right_on=['Date', 'team'], how='left')

        results = results[['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', 'two-factor-adv',
                           factors[1] + '_x', factors[1] + '_y']]

        results.columns = ['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY', 'two-factor-adv',
                           factors[1] + '_WINNER', factors[1] + '_LOSER']

        results = results.dropna().reset_index(drop=True)

        results['ADV_A_WON'] = [1 if results['two-factor-adv'][x] > 0 else 0 for x in range(len(results['WINNER']))]

        results['ADV_A'] = results['two-factor-adv']

        results['ADV_A'] = results['ADV_A'].abs()

        results['ADV_A_BUCKET'] = results['ADV_A'].transform(
            lambda x: pd.qcut(x, 5, duplicates='drop', labels=False))

        results['MARGIN_OF_VICTORY_ADV_A'] = [results['MARGIN_OF_VICTORY'][x] if results['ADV_A_WON'][x] == 1
                                              else -1 * results['MARGIN_OF_VICTORY'][x]
                                              for x in range(len(results['WINNER']))]

        results['ADV_B_WON'] = [1 if results[factors[1] + '_WINNER'][x] < results[factors[1] + '_LOSER'][x] else 0
                                for x in range(len(results['WINNER']))]

        results['ADV_B'] = results[factors[1] + '_LOSER'] - results[factors[1] + '_WINNER']

        results['ADV_B'] = results['ADV_B'].abs()

        results['ADV_B_BUCKET'] = results['ADV_B'].transform(
            lambda x: pd.qcut(x, 5, duplicates='drop', labels=False))

        results['MARGIN_OF_VICTORY_ADV_B'] = [results['MARGIN_OF_VICTORY'][x] if results['ADV_B_WON'][x] == 1
                                              else -1 * results['MARGIN_OF_VICTORY'][x]
                                              for x in range(len(results['WINNER']))]


    else:

        results = pd.merge(results, stats[['team', 'Date', factors[0]]], left_on=['DATE', 'WINNER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factors[0]]], left_on=['DATE', 'LOSER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factors[1]]], left_on=['DATE', 'WINNER'],
                           right_on=['Date', 'team'], how='left')

        results = pd.merge(results, stats[['team', 'Date', factors[1]]], left_on=['DATE', 'LOSER'],
                           right_on=['Date', 'team'], how='left')

        results = results[['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY',
                           factors[0] + '_x', factors[0] + '_y', factors[1] + '_x', factors[1] + '_y']]

        results.columns = ['DATE', 'WINNER', 'LOSER', 'PTS_WINNER', 'PTS_LOSER', 'MARGIN_OF_VICTORY',
                           factors[0] + '_WINNER', factors[0] + '_LOSER', factors[1] + '_WINNER', factors[1] + '_LOSER']

        results = results.dropna().reset_index(drop=True)

        results['ADV_A_WON'] = [1 if results[factors[0] + '_WINNER'][x] < results[factors[0] + '_LOSER'][x] else 0
                                for x in range(len(results['WINNER']))]

        results['ADV_A'] = results[factors[0] + '_LOSER'] - results[factors[0] + '_WINNER']

        results['ADV_A'] = results['ADV_A'].abs()

        results['ADV_A_BUCKET'] = results['ADV_A'].transform(
            lambda x: pd.qcut(x, 5, duplicates='drop', labels=False))

        results['MARGIN_OF_VICTORY_ADV_A'] = [results['MARGIN_OF_VICTORY'][x] if results['ADV_A_WON'][x] == 1
                                              else -1 * results['MARGIN_OF_VICTORY'][x]
                                              for x in range(len(results['WINNER']))]

        results['ADV_B_WON'] = [1 if results[factors[1] + '_WINNER'][x] < results[factors[1] + '_LOSER'][x] else 0
                                for x in range(len(results['WINNER']))]

        results['ADV_B'] = results[factors[1] + '_LOSER'] - results[factors[1] + '_WINNER']

        results['ADV_B'] = results['ADV_B'].abs()

        results['ADV_B_BUCKET'] = results['ADV_B'].transform(
            lambda x: pd.qcut(x, 5, duplicates='drop', labels=False))

        results['MARGIN_OF_VICTORY_ADV_B'] = [results['MARGIN_OF_VICTORY'][x] if results['ADV_B_WON'][x] == 1
                                              else -1 * results['MARGIN_OF_VICTORY'][x]
                                              for x in range(len(results['WINNER']))]

    results['ADV_OVERLAP'] = results['ADV_A_WON'] == results['ADV_B_WON']

    print("Percentage of Games Won by Team with Advantage A:", results['ADV_A_WON'].mean())
    print("Percentage of Games Won by Team with Advantage B:", results['ADV_B_WON'].mean())
    print(results[['MARGIN_OF_VICTORY_ADV_A', 'MARGIN_OF_VICTORY_ADV_B']].corr())
    print(results['ADV_OVERLAP'].sum() / len(results['ADV_OVERLAP']))
    print(results[['ADV_A', 'ADV_B']].corr())

    adv_a = results.groupby(['ADV_A_BUCKET', 'ADV_B_BUCKET'])['ADV_A_WON'].mean()
    adv_a_mov = results.groupby(['ADV_A_BUCKET', 'ADV_B_BUCKET'])['MARGIN_OF_VICTORY_ADV_A'].describe()
    adv_b = results.groupby(['ADV_B_BUCKET', 'ADV_A_BUCKET'])['ADV_B_WON'].mean()
    adv_b_mov = results.groupby(['ADV_B_BUCKET', 'ADV_A_BUCKET'])['MARGIN_OF_VICTORY_ADV_B'].describe()

    return([adv_a, adv_a_mov, adv_b, adv_b_mov])

adv_a, adv_a_mov, adv_b, adv_b_mov = factor_overlap([['yards-per-pass-attempt_rank', 'opponent-yards-per-pass-attempt_rank'],
                                                     'yards-per-pass-attempt_rank']) # --> 0.22, 0.45, 0.70
adv_a, adv_a_mov, adv_b, adv_b_mov = factor_overlap([['yards-per-rush-attempt_rank', 'opponent-yards-per-rush-attempt_rank'],
                                                     'yards-per-rush-attempt_rank']) # --> 0.2, 0.41, 0.69
adv_a, adv_a_mov, adv_b, adv_b_mov = factor_overlap([['yards-per-rush-attempt_rank', 'opponent-yards-per-rush-attempt_rank'],
                                                     ['offensive-points-per-game_rank', 'opponent-offensive-points-per-game_rank']]) # --> 0.3, 0.38, 0.68
adv_a, adv_a_mov, adv_b, adv_b_mov = factor_overlap([['yards-per-pass-attempt_rank', 'opponent-yards-per-pass-attempt_rank'],
                                                     ['offensive-points-per-game_rank', 'opponent-offensive-points-per-game_rank']]) # --> 0.35, 0.43, 0.70
adv_a, adv_a_mov, adv_b, adv_b_mov = factor_overlap([['yards-per-pass-attempt_rank', 'opponent-yards-per-pass-attempt_rank'],
                                                     ['yards-per-rush-attempt_rank', 'opponent-yards-per-rush-attempt_rank']]) # --> 0.13, 0.28, 0.62
adv_a, adv_a_mov, adv_b, adv_b_mov = factor_overlap(['yards-per-pass-attempt_rank', 'offensive-points-per-game_rank']) # --> 0.37, 0.43, 0.70