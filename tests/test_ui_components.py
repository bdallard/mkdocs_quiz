from bs4 import BeautifulSoup
from .base_test_case import BaseTestCase  # Assuming BaseTestCase is in a shared setup file

class TestUIComponents(BaseTestCase):

    def test_show_progress_bar_enabled(self):
        # Load plugin configuration with progress bar enabled
        self.load_plugin_config(show_indice_on_answer=True, show_score=True, show_progress_bar=True, language='en')

        # Mocking quiz data (You can reuse mock_quiz_data here)
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'type': 'multiple-choice',
                            'question': {'en': 'What is the capital of France?'},
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False},
                                {'text': {'en': 'Paris'}, 'correct': True}
                            ]
                        }
                    ]
                }
            }
        }

        # Generate quiz HTML
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate the progress bar is present
        progress_bar = soup.find('div', class_='progress-bar')
        self.assertIsNotNone(progress_bar)

    def test_show_progress_bar_disabled(self):
        # Load plugin configuration with progress bar disabled
        self.load_plugin_config(show_indice_on_answer=True, show_score=True, show_progress_bar=False, language='en')

        # Mocking quiz data
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'type': 'multiple-choice',
                            'question': {'en': 'What is the capital of France?'},
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False},
                                {'text': {'en': 'Paris'}, 'correct': True}
                            ]
                        }
                    ]
                }
            }
        }

        # Generate quiz HTML
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate the progress bar is not present
        progress_bar = soup.find('div', class_='progress-bar')
        self.assertIsNone(progress_bar)

    def test_show_refresh_button_enabled(self):
        # Load plugin configuration with refresh button enabled
        self.load_plugin_config(show_indice_on_answer=True, show_score=True, show_progress_bar=True, show_refresh_button=True, language='en')

        # Mocking quiz data
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'type': 'multiple-choice',
                            'question': {'en': 'What is the capital of France?'},
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False},
                                {'text': {'en': 'Paris'}, 'correct': True}
                            ]
                        }
                    ]
                }
            }
        }

        # Generate quiz HTML
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate the refresh button is present
        refresh_button = soup.find('button', class_='refresh-quiz')
        self.assertIsNotNone(refresh_button)


    def test_show_refresh_button_disabled(self):
        # Load plugin configuration with refresh button disabled
        self.load_plugin_config(show_indice_on_answer=True, show_score=True, show_progress_bar=True, show_refresh_button=False, language='en')

        # Mocking quiz data
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'type': 'multiple-choice',
                            'question': {'en': 'What is the capital of France?'},
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False},
                                {'text': {'en': 'Paris'}, 'correct': True}
                            ]
                        }
                    ]
                }
            }
        }

        # Generate quiz HTML
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate the refresh button is not present
        refresh_button = soup.find('button', class_='refresh-button')
        self.assertIsNone(refresh_button)
