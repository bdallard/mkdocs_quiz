import unittest
from bs4 import BeautifulSoup
from .base_test_case import BaseTestCase  # Assuming BaseTestCase is in a shared setup file
from .mock_quiz_data import mock_quiz_data

class TestEndToEnd(BaseTestCase):
    
    def setUp(self):
        super().setUp()  # Ensure the plugin is initialized in the base class
        # Load the plugin configuration
        self.load_plugin_config(show_indice_on_answer=True, show_score=True, show_progress_bar=True, show_refresh_button=True, language='en', logging=True)

        # Set the quiz data
        self.plugin.quiz_data = mock_quiz_data

    def test_end_to_end(self):
        # Generate HTML for the first quiz
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Assertions to verify that everything is working correctly
        # Check for the presence of the refresh button
        refresh_button = soup.find('button', class_='refresh-quiz')
        self.assertIsNotNone(refresh_button)

        # Check for the presence of progress bar
        progress_bar = soup.find('div', class_='progress-bar')
        self.assertIsNotNone(progress_bar)

        # Check for the presence of quiz hints (indices)
        indice_texts = [li['data-indice'] for li in soup.find_all('li', {'data-indice': True})]
        self.assertIn("This is the capital of Germany.", indice_texts)
        

if __name__ == '__main__':
    unittest.main()
