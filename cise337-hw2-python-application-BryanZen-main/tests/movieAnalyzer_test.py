import pytest
import sys, os

sys.path.insert(1, os.getcwd())
from src.movieAnalyzer import pd, get_movies_interval, get_rating_popularity_stats, get_actor_movies_release_year_range, \
    get_actor_median_rating, get_directors_median_reviews


class TestMovieAnalyzer:

    def setup_method(self):
        top200_movies_file = os.path.join('src', 'data', 'Top_200_Movies.csv')
        self.file = pd.read_csv(top200_movies_file)

    def test_get_movies_interval_invalid_y(self):
        with pytest.raises(ValueError):
            get_movies_interval(1990, 1980)

    def test_get_movies_interval_invalid_t1(self):
        with pytest.raises(TypeError):
            get_movies_interval('1990', 1980)

    def test_get_movies_interval_invalid_t2(self):
        with pytest.raises(TypeError):
            get_movies_interval(1990, '1980')

    def test_get_movies_interval_valid(self):
        val = pd.Series(
            ["Schindler's List", "Reservoir Dogs", "Unforgiven", "Jurassic Park", "In the Name of the Father",
             "Groundhog Day"], index=['5', '88', '131', '141', '177', '205'], dtype=object, name='Title')
        assert get_movies_interval(1992, 1993).equals(val)

    def test_get_rating_popularity_stats_invalid1(self):
        with pytest.raises(ValueError):
            get_rating_popularity_stats('Ratin', 'mean')

    def test_get_rating_popularity_stats_invalid2(self):
        with pytest.raises(ValueError):
            get_rating_popularity_stats('Rating', 'mea')

    def test_get_rating_popularity_stats_valid(self):
        assert get_rating_popularity_stats('Popularity Index', 'mean') == '1091.92'
        assert get_rating_popularity_stats('Popularity Index', 'median') == '673.0'
        assert get_rating_popularity_stats('Popularity Index', 'count') == '207'
        assert get_rating_popularity_stats('Popularity Index', 'min') == '3'
        assert get_rating_popularity_stats('Popularity Index', 'max') == '4940'
        assert get_rating_popularity_stats('Rating', 'mean') == '8.34'
        assert get_rating_popularity_stats('Rating', 'median') == '8.3'
        assert get_rating_popularity_stats('Rating', 'count') == '207'
        assert get_rating_popularity_stats('Rating', 'min') == '8.1'
        assert get_rating_popularity_stats('Rating', 'max') == '9.3'

    def test_get_actor_movies_release_year_range_invalid1(self):
        with pytest.raises(TypeError):
            get_actor_movies_release_year_range('Leonardo DiCaprio', '2010', 2002)

    def test_get_actor_movies_release_year_range_invalid2(self):
        with pytest.raises(TypeError):
            get_actor_movies_release_year_range('Leonardo DiCaprio', 2010, '2002')

    def test_get_actor_movies_release_year_range_invalid3(self):
        with pytest.raises(ValueError):
            get_actor_movies_release_year_range('Leonardo DiCaprio', 2002, 2010)

    def test_get_actor_movies_release_year_range_valid(self):
        val = pd.Series([2010, 2012, 2013, 2010],
                        index=['Inception', 'Django Unchained', 'The Wolf of Wall Street', 'Shutter Island'])
        assert get_actor_movies_release_year_range('Leonardo DiCaprio', 2022, 2010).equals(val)

    def test_get_actor_median_rating_invalid_1(self):
        with pytest.raises(ValueError):
            get_actor_median_rating('')

    def test_get_actor_median_rating_invalid_2(self):
        with pytest.raises(TypeError):
            get_actor_median_rating(1)

    def test_get_actor_median_rating_valid(self):
        assert get_actor_median_rating('Bryan Zen') is None
        assert get_actor_median_rating('Leonardo DiCaprio') == '8.3'

    def test_get_directors_median_reviews(self):
        val = pd.Series([0.190, 0.124, 0.397, 1.050, 1.050],
                        index=['Aamir Khan', 'Akira Kurosawa', 'Alfred Hitchcock', 'Andrew Stanton', 'Anthony Russo'])
        assert get_directors_median_reviews()['Aamir Khan'] == val['Aamir Khan']
        assert get_directors_median_reviews()['Akira Kurosawa'] == val['Akira Kurosawa']
        assert get_directors_median_reviews()['Alfred Hitchcock'] == val['Alfred Hitchcock']
        assert get_directors_median_reviews()['Andrew Stanton'] == val['Andrew Stanton']
        assert get_directors_median_reviews()['Anthony Russo'] == val['Anthony Russo']
