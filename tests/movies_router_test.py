import unittest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from data.models import Movie, User
from routers.movies import create_movie
from services.movies_service import fetch_and_update_metascore


class TestCreateMovieAsync(unittest.IsolatedAsyncioTestCase):
    """Test suite for async movie creation functionality"""

    async def test_create_movie_returns_immediately(self):
        """Test that create_movie returns immediately without waiting for API"""
        movie_input = Movie(
            id=None,
            title="The Matrix",
            director="The Wachowskis",
            release_year=1999,
            rating=None
        )
        user_input = User(
            id=2,
            username='Gosho',
            password='1234',
            role='admin'
        )

        # Mock the service functions
        with patch('services.movies_service.movie_exists') as mock_exists, \
             patch('services.movies_service.create') as mock_create, \
             patch('routers.movies.asyncio.create_task') as mock_create_task:

            # Setup mocks
            mock_exists.return_value = False
            dummy_movie = Movie(id=1, title="The Matrix", director="The Wachowskis", release_year=1999, rating=0)
            mock_create.return_value = dummy_movie

            # Call the endpoint
            result = await create_movie(movie_input,'2;Gosho')

            # Verify that the function returns immediately
            self.assertEqual(result.id, 1)
            self.assertEqual(result.title, "The Matrix")
            self.assertEqual(result.rating, 0)  # Should be 0 initially

            # Verify that create was called with the movie
            mock_create.assert_called_once_with(movie_input)

            # Verify that background task was created (not awaited)
            mock_create_task.assert_called_once()

    async def test_create_movie_background_updates_metascore(self):
        """Test that the background task updates metascore after API call"""
        movie_input = Movie(
            id=None,
            title="Inception",
            director="Christopher Nolan",
            release_year=2010,
            rating=None
        )

        dummy_movie = Movie(id=2, title="Inception", director="Christopher Nolan", release_year=2010, rating=0)

        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"Metascore": "74"}

        # Mock the AsyncClient
        mock_async_client = AsyncMock()
        mock_async_client.get.return_value = mock_response
        mock_async_client.__aenter__.return_value = mock_async_client
        mock_async_client.__aexit__.return_value = None

        with patch('services.movies_service.httpx.AsyncClient', return_value=mock_async_client), \
             patch('services.movies_service.create_async') as mock_create_async:

            # Call the background task function to test it
            await fetch_and_update_metascore(movie_input, dummy_movie)

            # Verify that the API was called
            mock_async_client.get.assert_called_once()

            # Verify that create_async was called with the metascore
            mock_create_async.assert_called_once()
            call_args = mock_create_async.call_args
            self.assertEqual(call_args[0][0], "74")  # metascore should be "74"

    async def test_create_movie_duplicate_movie_returns_bad_request(self):
        """Test that creating a duplicate movie returns BadRequest"""
        movie_input = Movie(
            id=None,
            title="Existing Movie",
            director="Some Director",
            release_year=2000,
            rating=None
        )
        user_input = User(
            id=2,
            username='Gosho',
            password='1234',
            role='admin'
        )

        with patch('services.movies_service.movie_exists') as mock_exists:
            mock_exists.return_value = True

            result = await create_movie(movie_input,'2;Gosho')

            # Should return BadRequest response
            self.assertIn('already exists', result.content)

    async def test_create_movie_api_failure_doesnt_block_response(self):
        """Test that API failure in background task doesn't affect initial response"""
        movie_input = Movie(
            id=None,
            title="Test Movie",
            director="Test Director",
            release_year=2020,
            rating=None
        )
        user_input = User(
            id=2,
            username='Gosho',
            password='1234',
            role='admin'
        )

        dummy_movie = Movie(id=3, title="Test Movie", director="Test Director", release_year=2020, rating=0)

        with patch('services.movies_service.movie_exists', return_value=False), \
             patch('services.movies_service.create', return_value=dummy_movie), \
             patch('routers.movies.asyncio.create_task'):

            # Call should still succeed regardless of background task
            result = await create_movie(movie_input,'2;Gosho')

            self.assertEqual(result.id, 3)
            self.assertEqual(result.rating, 0)


if __name__ == '__main__':
    unittest.main()
