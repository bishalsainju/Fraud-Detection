import pandas as pd
import math

# Read in csv
# Notes: Has been converted to UTF-8 encoding
# from original download. Column titles have had
# spaces replaced with underscores.
seshat = pd.read_csv('seshat.csv')

# Remove information on contributors
# responsible for data validation. Sorry, contributors!
seshat = seshat[seshat.Variable != 'RA']
seshat = seshat[seshat.Variable != 'Editor']
seshat = seshat[seshat.Variable != 'Expert']

# Function mapped to Value_From to convert from
# string data to integer data
def valConvert(value):
    value = value.lower()
    nan = float('NaN')
    if value == 'present' or value == 'inferred present' or value == 'inferred inferred present':
        return 1
    elif value == 'absent' or value == 'inferred absent':
        return 0
    elif value in ['unknown','suspected unknown', 'inferred', 'uncoded']:
        return nan
    else:
        return value

# Convert "present" and "absent" variables to boolean integers
seshat['Value_From'] = seshat['Value_From'].apply(valConvert)

# Drop unnecessary columns
seshat = seshat.drop(columns=['Section','Subsection','Fact_Type','Comment'])

# Grab the first polity and NGA in the dataset
curPolity = seshat.iloc[0]['Polity']
curNGA = seshat.iloc[0]['NGA']

# Set up some things
polities = pd.DataFrame()
curSeries = pd.Series()
curSeries['Polity'] = curPolity
curSeries['NGA'] = curNGA

# Just... Rearrange everything
for index, row in seshat.iterrows():
    # Check if new row is a new polity
    if row['Polity'] != curPolity:
        print('Munging polity ' + curPolity + '...')
        # Add the current series to the polities dataframe
        polities = polities.append(curSeries.copy(), ignore_index=True)
        # Reset the current series
        curSeries = pd.Series()
        # Update the new polity
        curPolity = row['Polity']
        curSeries['Polity'] = curPolity
        curSeries['NGA'] = row['NGA']

    # Grab the variable that is actually being expressed
    variable = row['Variable']
    if row['Value_Note'] == 'simple' and row['Date_Note'] != row['Date_Note']:
        # For simple variables without date shenanigans, just store it in the series
        curSeries[variable] = row['Value_From']

print('Munging Seshat herself...')

# Delete duplicate columns
polities = polities.drop(columns=[
    'Written records_1',
    'Philosophy_1',
    'Time_1',
    'Population of the largest settlement_1'
    ])

# Standard max function takes NaN as larger than everything
def notDumbMax(l, r):
    if math.isnan(l):
        return r
    elif math.isnan(r):
        return l
    else:
        return max(l,r)

# Convenience function for combining two series via maximum
def combineWithMax(df, s1, s2):
    return df[s1].combine(df[s2], notDumbMax)

# Merge columns that are really the same but have minor spelling differences.
# Columns with capitalized first letters are favored for consistency. 

polities['Drinking water supply systems'] = combineWithMax(
        polities, 
        'Drinking water supply systems', 
        'drinking water supply systems'
        )

polities['Food storage sites'] = combineWithMax(
        polities, 
        'Food storage sites', 
        'food storage sites'
        )

polities['Markets'] = combineWithMax(
        polities, 
        'Markets', 
        'markets'
        )

polities['Nonwritten records'] = combineWithMax(
        polities, 
        'Nonwritten records', 
        'Non written records'
        )

polities['Irrigation systems'] = combineWithMax(
        polities, 
        'Irrigation systems', 
        'irrigation systems'
        )


polities['Professional lawyers'] = combineWithMax(
        polities, 
        'Professional lawyers', 
        'Professional Lawyers'
        )

polities['Non-phonetic writing'] = combineWithMax(
        polities, 
        'Non-phonetic writing', 
        'Non-phonetic  writing'
        )

polities['Symbolic buildings'] = combineWithMax(
        polities, 
        'Symbolic buildings', 
        'Symbolic building'
        )

# Remove the extra columns that we merged into their more-handsome siblings
polities = polities.drop(columns=[
        'Professional Lawyers',
        'irrigation systems',
        'Non written records',
        'markets',
        'food storage sites',
        'Non-phonetic  writing',
        'drinking water supply systems',
        'Symbolic building'
    ])


# Do some re-naming to achieve greater consistency with other columns
# and clarity in the absence of sub-sections
polities = polities.rename(columns={
    'Nonwritten records' : 'Non-written records',
    'cost'               : 'Polity-owned building cost',
    'extent'             : 'Polity-owned building extent',
    'height'             : 'Polity-owned building height',
    'Source of support'  : 'Bureaucracy source of support',
    'Examination system' : 'Bureaucracy examination system',
    'Merit promotion'    : 'Bureaucracy merit promotion',
    'Length'             : 'Measurement of length',
    'Area'               : 'Measurement of Area',
    'Volume'             : 'Measurement of Volume',
    'Weight'             : 'Measurement of Weight',
    'Time'               : 'Measurement of Time',
    'Geometrical'        : 'Measurement of Geometry'
    })

# Re-sort the columns by name
polities = polities.reindex(sorted(polities.columns), axis=1)

# Index by Polity
polities = polities.set_index('Polity')

# Export
polities.to_csv('seshat_munged.csv', sep=',')
