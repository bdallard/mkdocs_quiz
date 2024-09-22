from unittest.mock import patch, mock_open
from .base_test_case import BaseTestCase
from bs4 import BeautifulSoup 

class TestQuizLogic(BaseTestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"quizzes": {"quiz1": {...}}}')
    def test_load_quiz_file(self, mock_file):
        self.load_plugin_config()
        
        # Manually load the quiz data (as done in your original test file)
        self.plugin.quiz_data = {
            "quizzes": {
                "quiz1": {
                    "questions": [
                        {
                            "type": "multiple-choice",
                            "question": {"en": "What is the capital of France?"},
                            "options": [
                                {"text": {"en": "Berlin"}, "correct": False},
                                {"text": {"en": "Paris"}, "correct": True},
                                {"text": {"en": "Rome"}, "correct": False}
                            ]
                        }
                    ]
                }
            }
        }
        
        # Ensure that quiz1 is present in the loaded data
        self.assertIn('quiz1', self.plugin.quiz_data['quizzes'])

    def test_score_computation(self):
        self.load_plugin_config()
        quiz = {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is 2 + 2?",
                        "fr": "Qu'est-ce que 2 + 2?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": False,
                            "indice": {
                                "en": "This is incorrect.",
                                "fr": "Ceci est incorrect."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": True,
                            "indice": {
                                "en": "This is correct.",
                                "fr": "Ceci est correct."
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "The capital of France is ___.",
                        "fr": "La capitale de la France est ___."
                    },
                    "answer": {
                        "en": "Paris",
                        "fr": "Paris"
                    },
                    "indice": {
                        "en": "It is known as the city of light.",
                        "fr": "Elle est connue comme la ville lumière."
                    }
                }
            ]
        }

        # Generate the HTML for the quiz
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Ensure the score div is present and initially hidden
        score_div = soup.find('div', class_='score')
        self.assertIsNotNone(score_div)
        self.assertIn('hidden', score_div['class'])

    def test_multi_choice_question(self):
        self.load_plugin_config()
        quiz = {
            "questions": [
                {
                    "type": "multi-choice",
                    "question": {"en": "Select all prime numbers."},
                    "options": [
                        {"text": {"en": "2"}, "correct": True},
                        {"text": {"en": "3"}, "correct": True},
                        {"text": {"en": "4"}, "correct": False},
                        {"text": {"en": "5"}, "correct": True}
                    ]
                }
            ]
        }

        # Generate the HTML for the multi-choice question
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Check for the presence of checkboxes for multi-choice
        checkboxes = soup.find_all('input', {'type': 'checkbox'})
        self.assertEqual(len(checkboxes), 4)

    def test_score_hidden_when_disabled(self):
        self.load_plugin_config(show_indice_on_answer=False, show_score=False, show_progress_bar=True)
        quiz = {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is 2 + 2?",
                        "fr": "Qu'est-ce que 2 + 2?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "3",
                                "fr": "3"
                            },
                            "correct": False,
                            "indice": {
                                "en": "This is incorrect.",
                                "fr": "Ceci est incorrect."
                            }
                        },
                        {
                            "text": {
                                "en": "4",
                                "fr": "4"
                            },
                            "correct": True,
                            "indice": {
                                "en": "This is correct.",
                                "fr": "Ceci est correct."
                            }
                        }
                    ]
                }
            ]
        }
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Ensure the score div is not present
        score_div = soup.find('div', class_='score')
        self.assertIsNone(score_div)

    def test_generate_quiz_html_with_media(self):
        self.load_plugin_config(show_indice_on_answer=False, show_score=False, show_progress_bar=True)
        
        # Mock quiz data with media (image and video)
        quiz = {
            'questions': [
                {
                    'question': {
                        'en': 'What is shown in the image below?'
                    },
                    'type': 'multiple-choice',
                    'media': {
                        'type': 'image',
                        'src': 'https://media.tenor.com/VFFJ8Ei3C2IAAAAM/rickroll-rick.gif',
                        'alt': {
                            'en': 'An example image'
                        }
                    },
                    'options': [
                        {'text': {'en': 'A cat'}, 'correct': False, 'indice': {'en': 'It is not a cat.'}},
                        {'text': {'en': 'A dog'}, 'correct': True, 'indice': {'en': 'Correct, it is a dog.'}},
                    ]
                },
                {
                    'question': {
                        'en': 'What sound is played in the audio below?'
                    },
                    'type': 'multiple-choice',
                    'media': {
                        'type': 'audio',
                        'src': './static/audios/test.mp3',
                        'alt': {
                            'en': 'An example audio'
                        }
                    },
                    'options': [
                        {'text': {'en': 'A bell'}, 'correct': True, 'indice': {'en': 'Correct, it is a bell.'}},
                        {'text': {'en': 'A whistle'}, 'correct': False, 'indice': {'en': 'It is not a whistle.'}},
                    ]
                },
            ]
        }

        quiz_html = self.plugin.generate_quiz_html(quiz)

        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Check for the presence of image and its attributes
        img_tag = soup.find('img')
        self.assertIsNotNone(img_tag)
        self.assertEqual(img_tag['src'], 'https://media.tenor.com/VFFJ8Ei3C2IAAAAM/rickroll-rick.gif')
        self.assertEqual(img_tag['alt'], 'An example image')

        # Check for the presence of audio and its attributes
        audio_tag = soup.find('audio')
        self.assertIsNotNone(audio_tag)
        self.assertEqual(audio_tag.find('source')['src'], './static/audios/test.mp3')
        
        # Check for the quiz question text
        self.assertTrue(soup.find_all(string=lambda text: 'What is shown in the image below?' in text))
        self.assertTrue(soup.find_all(string=lambda text: 'What sound is played in the audio below?' in text))

        # Check the options for both questions
        options = [li.get_text(strip=True) for li in soup.find_all('li')]
        self.assertIn('A cat', options)
        self.assertIn('A dog', options)
        self.assertIn('A bell', options)
        self.assertIn('A whistle', options)

    @patch('builtins.print')
    def test_logging_enabled(self, mock_print):
        # Load plugin config with logging enabled
        self.load_plugin_config(logging=True)

        # Trigger an event that would cause a log message
        self.plugin.console_log("Test log message with logging enabled")

        # Gather all the calls to print and extract the first argument
        print_calls = [call[0][0] for call in mock_print.call_args_list]

        # Check if the expected log message is among the print calls
        self.assertIn("DEBUG MESSAGE: Test log message with logging enabled", print_calls)


    @patch('builtins.print')
    def test_logging_disabled(self, mock_print):
        # Load plugin config with logging disabled (default)
        self.load_plugin_config(logging=False)

        # Trigger an event that would cause a log message
        self.plugin.console_log("Test log message with logging disabled")

        # Ensure the print function was not called, as logging is disabled
        mock_print.assert_not_called()
