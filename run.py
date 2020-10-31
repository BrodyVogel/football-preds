from get_data import *

analysis = get_data_nfl(date = '2020-09-30', attributes = {'yards-per-pass-attempt': 'desc',
                                                       'yards-per-rush-attempt': 'desc',
                                                       'offensive-points-per-game': 'desc',
                                                       'opponent-yards-per-pass-attempt': 'asc',
                                                       'opponent-yards-per-rush-attempt': 'asc',
                                                       'opponent-offensive-points-per-game': 'asc',
                                                       'turnover-margin-per-game': 'desc',
                                                       'predictive-by-other': 'desc'})
# Week 4
## 11-3

# Week 5
## 8-6

# Week 6
## 10-4

week_5 = get_schedule(4)

for row in range(len(week_5)):
    print(week_5.iloc[row, :]['Away_Team'], '@', week_5.iloc[row, :]['Home_Team'])
    evaluate(analysis, week_5.iloc[row, :]['Away_Team'], week_5.iloc[row, :]['Home_Team'])
    print('\n\n')