# Run this script from the repository's root.

import os
import pandas as pd

top200_movies_file = os.path.join('src', 'data', 'Top_200_Movies.csv')


def get_movies_data():
    return pd.read_csv(top200_movies_file)


def get_movies_interval(y1, y2):
    if not isinstance(y1, int):
        raise TypeError
    if not isinstance(y2, int):
        raise TypeError
    if y2 < y1:
        raise ValueError
    r = get_movies_data()
    out = pd.Series([], dtype=object, name='Title')
    for index, row in r.iterrows():
        if y1 <= int(row['Year of Release']) <= y2:
            out[str(index)] = row['Title']
    return out


def get_rating_popularity_stats(index, type):
    if index != 'Rating' and index != 'Popularity Index':
        raise ValueError('Invalid index or type')
    if type != 'count' and type != 'mean' and type != 'median' and type != 'min' and type != 'max':
        raise ValueError('Invalid index or type')
    r = get_movies_data()
    out = pd.Series([], dtype=object)
    for i, row in r.iterrows():
        if index == 'Rating':
            if row['Rating'] is not None:
                out[i] = float(row['Rating'])
        if index == 'Popularity Index':
            if row['Popularity Index'] is not None:
                out[i] = int(row['Popularity Index'].replace(',', ''))
    if type == 'count':
        return str(out.size)
    if type == 'mean':
        return str(round(out.mean(), 2))
    if type == 'median':
        return str(out.median())
    if type == 'min':
        return str(out.min())
    if type == 'max':
        return str(out.max())


def get_actor_movies_release_year_range(actor, upper, lower=0):
    if not isinstance(upper, int):
        raise TypeError
    if not isinstance(lower, int):
        raise TypeError
    if upper < lower:
        raise ValueError
    r = get_movies_data()
    out = pd.Series([], dtype=object)
    for index, row in r.iterrows():
        if lower <= int(row['Year of Release']) <= upper:
            if row['Movie Cast'].find(actor) != -1:
                out[row['Title']] = int(row['Year of Release'])
    return out


def get_actor_median_rating(actor):
    if actor == '':
        raise ValueError
    if not isinstance(actor, str):
        raise TypeError
    r = get_movies_data()
    out = pd.Series([], dtype=object)
    count = 0
    for index, row in r.iterrows():
        if row['Movie Cast'].find(actor) != -1:
            count += 1
            if row['Rating'] is not None:
                out[index] = float(row['Rating'])
    if count == 0:
        return None
    else:
        return str(out.median())


def get_directors_median_reviews():
    r = get_movies_data()
    r['Number of Reviews'] = r['Number of Reviews'].apply(toM)
    out = r.groupby('Director')['Number of Reviews'].median()
    print(out)
    return out


def toM(x):
    if isinstance(x, float):
        return round(x, 3)
    if isinstance(x, int):
        return round((float(x)), 3)
    if x.find('K') != -1:
        return round(((float(x.replace('K', '')) * 1000) / 1000000), 3)
    if x.find('M') != -1:
        return round((float(x.replace('M', ''))), 3)
