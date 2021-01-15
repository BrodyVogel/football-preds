from abstract_base_classes import *
import numpy as np
import pandas as pd
import datetime

class BetNCAAF(Bet):

    def __init__(self):
        self.description = '"BetNCAAF" instantiation of the "Bet" Abstract Base Class'

    def get_data(self, date, attributes):
        output = pd.DataFrame({'team': []})
        output = output.set_index('team')

        for attribute in list(attributes.keys()):
            if 'by-other' in attribute:
                url = 'https://www.teamrankings.com/college-football/ranking/' + attribute + '?date=' + date
            else:
                url = 'https://www.teamrankings.com/college-football/stat/' + attribute + '?date=' + date

            z = pd.read_html(url, flavor='html5lib')[0]

            z = z.iloc[:, 0:3]

            z.columns = [attribute + '_rank', 'team', attribute]

            z = z.replace('Miami (OH)', 'Miami_OH')
            z = z.replace('Miami (FL)', 'Miami_FL')

            if 'by-other' in attribute:
                z['team'] = ['Miami_OH' if 'Miami (OH)' in x
                             else 'Miami_FL' if 'Miami (FL' in x
                else x.split(' (')[0] for x in z['team']]

            z = z.set_index('team')

            output = pd.merge(z, output, how='left', on=['team'])

        output = output.replace('--', np.nan)

        for column in output.columns:
            output[column] = pd.to_numeric(output[column])

        for column in output.columns:
            if 'rank' in column:
                key = column.split('_rank')[0]
                if attributes[key] == 'desc':
                    output[column] = output[key].rank(ascending=False)
                else:
                    output[column] = output[key].rank(ascending=True)

        return output

    def get_historical_stats(self, start_dates, start_week, attributes):
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
                    to_concat = self.get_data(date, attributes)
                except:
                    new_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    new_date = new_date + datetime.timedelta(days=1)
                    new_date = new_date.strftime('%Y-%m-%d')
                    print(new_date)
                    to_concat = self.get_data(new_date, attributes)

                to_concat['Week'] = start_week_go
                to_concat['Year'] = date[0:4]
                to_concat['Date'] = date

                df_list.append(to_concat)

                start_week_go += 1

        output = pd.concat(df_list)

        output['Week'] = output['Week'].astype('int32')
        output['Year'] = output['Year'].astype('int32')

        return (output)
