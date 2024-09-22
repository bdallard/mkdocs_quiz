from bs4 import BeautifulSoup  # Import BeautifulSoup to parse the generated HTML
from .base_test_case import BaseTestCase  # Import the BaseTestCase from your shared setup
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File


class TestHTMLGeneration(BaseTestCase):

    def test_generate_quiz_html(self):
        # Load the plugin configuration with default values
        self.load_plugin_config(True, True, True)
        # Mock the quiz data
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'question': {'en': 'What is the capital of France?'},
                            'type': 'multiple-choice',
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False, 'indice': {'en': 'This is the capital of Germany.'}},
                                {'text': {'en': 'Madrid'}, 'correct': False, 'indice': {'en': 'This is the capital of Spain.'}},
                                {'text': {'en': 'Paris'}, 'correct': True, 'indice': {'en': 'Paris is the city of light'}},
                                {'text': {'en': 'Rome'}, 'correct': False, 'indice': {'en': 'This is the capital of Italy.'}}
                            ]
                        }
                    ]
                }
            }
        }
        # Generate quiz HTML
        quiz = self.plugin.quiz_data['quizzes']['quiz1']
        quiz_html = self.plugin.generate_quiz_html(quiz)
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate that the question text is present
        self.assertTrue(soup.find_all(string=lambda text: 'What is the capital of France?' in text))

        # Validate the presence of the options
        options = [li.get_text(strip=True) for li in soup.find_all('li')]
        self.assertIn('Berlin', options)
        self.assertIn('Madrid', options)
        self.assertIn('Paris', options)
        self.assertIn('Rome', options)

        # Validate the presence of indices
        indices = [li['data-indice'] for li in soup.find_all('li')]
        self.assertIn('This is the capital of Germany.', indices)
        self.assertIn('This is the capital of Spain.', indices)
        self.assertIn('Paris is the city of light', indices)
        self.assertIn('This is the capital of Italy.', indices)

    def test_on_page_markdown(self):
        self.load_plugin_config(True, True, True)
        markdown = """
        # Sample Page

        <!-- QUIZ_ID: quiz1 -->
        """
        file = File('sample_page.md', 'docs', 'site', False)
        page = Page('Sample Page', file, self.config)

        # Mock quiz data for the page
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'question': {
                                'en': 'What is the capital of France?'
                            },
                            'type': 'multiple-choice',
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False, 'indice': {'en': 'This is the capital of Germany.'}},
                                {'text': {'en': 'Madrid'}, 'correct': False, 'indice': {'en': 'This is the capital of Spain.'}},
                                {'text': {'en': 'Paris'}, 'correct': True, 'indice': {'en': 'Paris is the city of light'}},
                                {'text': {'en': 'Rome'}, 'correct': False, 'indice': {'en': 'This is the capital of Italy.'}}
                            ]
                        }
                    ]
                }
            }
        }

        updated_markdown = self.plugin.on_page_markdown(markdown, page, self.config, None)

        # Replace placeholders with quiz HTML
        for placeholder, quiz_html in page.meta.get('quiz_placeholder', []):
            updated_markdown = updated_markdown.replace(placeholder, quiz_html)

        soup = BeautifulSoup(updated_markdown, 'html.parser')

        # Validate that the question text is present
        self.assertTrue(soup.find_all(string=lambda text: 'What is the capital of France?' in text))

        # Validate the presence of the options
        options = [li.get_text(strip=True) for li in soup.find_all('li')]
        self.assertIn('Berlin', options)
        self.assertIn('Madrid', options)
        self.assertIn('Paris', options)
        self.assertIn('Rome', options)

    def test_hint_functionality(self):
        self.load_plugin_config(True, True, True)
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
                            'question': {'en': 'What is the capital of France?'},
                            'options': [
                                {'text': {'en': 'Berlin'}, 'correct': False, 'indice': {'en': 'This is the capital of Germany.'}},
                                {'text': {'en': 'Madrid'}, 'correct': False, 'indice': {'en': 'This is the capital of Spain.'}},
                                {'text': {'en': 'Paris'}, 'correct': True, 'indice': {'en': 'Paris is the city of light'}},
                                {'text': {'en': 'Rome'}, 'correct': False, 'indice': {'en': 'This is the capital of Italy.'}}
                            ]
                        }
                    ]
                }
            }
        }
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate the presence of indices
        indices = [li['data-indice'] for li in soup.find_all('li')]
        self.assertIn('This is the capital of Germany.', indices)
        self.assertIn('This is the capital of Spain.', indices)
        self.assertIn('Paris is the city of light', indices)
        self.assertIn('This is the capital of Italy.', indices)

    def test_show_correct_answer(self):
        self.load_plugin_config(True, True, True)
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                        {
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
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Validate the presence of correct and incorrect classes
        self.assertTrue(soup.find(class_='correct'))
        self.assertTrue(soup.find(class_='incorrect'))

    def test_show_indice_on_answer_true(self):
        self.load_plugin_config(show_indice_on_answer=True, show_score=True, show_progress_bar=True, language='en')
        self.plugin.quiz_data = {
            'quizzes': {
                'quiz1': {
                    'questions': [
                                {
                            "type": "multiple-choice",
                            "question": {
                                "en": "What is the capital of France?",
                                "fr": "Quelle est la capitale de la France?"
                            },
                            "media": {
                                "type": "image",
                                "src": "./static/images/test.png",
                                "alt": {
                                    "en": "Paris",
                                    "fr": "Paris"
                                }
                            },
                            "options": [
                                {
                                    "text": {
                                        "en": "Berlin",
                                        "fr": "Berlin"
                                    },
                                    "correct": "false",
                                    "indice": {
                                        "en": "This is the capital of Germany.",
                                        "fr": "Ceci est la capitale de l'Allemagne."
                                    }
                                },
                                {
                                    "text": {
                                        "en": "Madrid",
                                        "fr": "Madrid"
                                    },
                                    "correct": "false",
                                    "indice": {
                                        "en": "This is the capital of Spain.",
                                        "fr": "Ceci est la capitale de l'Espagne."
                                    }
                                },
                                {
                                    "text": {
                                        "en": "Paris",
                                        "fr": "Paris"
                                    },
                                    "correct": "true",
                                    "indice": {
                                        "en": "Paris is the city of light",
                                        "fr": ""
                                    }
                                },
                                {
                                    "text": {
                                        "en": "Rome",
                                        "fr": "Rome"
                                    },
                                    "correct": "false",
                                    "indice": {
                                        "en": "This is the capital of Italy.",
                                        "fr": "Ceci est la capitale de l'Italie."
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
        # Generate quiz HTML
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Check for the presence of the hint button
        hint_button = soup.find('button', class_='hint-button')
        self.assertIsNotNone(hint_button)

        # Validate the media presence (image for this question)
        img_tag = soup.find('img')
        self.assertIsNotNone(img_tag)
        self.assertEqual(img_tag['src'], './static/images/test.png')
        self.assertEqual(img_tag['alt'], 'Paris')

    def test_show_indice_on_answer_false(self):
        # Load plugin configuration with show_indice_on_answer set to False
        self.load_plugin_config(show_indice_on_answer=False, show_score=True, show_progress_bar=True)

        # Mocking the quiz data based on your quizzes.json structure
        self.plugin.quiz_data = {
            "quizzes": {
                "quiz1": {
                    "questions": [
                        {
                            "type": "multiple-choice",
                            "question": {"en": "What is the capital of France?"},
                            "media": {
                                "type": "image",
                                "src": "./static/images/test.png",
                                "alt": {"en": "Paris"}
                            },
                            "options": [
                                {
                                    "text": {"en": "Berlin"},
                                    "correct": False,
                                    "indice": {"en": "This is the capital of Germany."}
                                },
                                {
                                    "text": {"en": "Madrid"},
                                    "correct": False,
                                    "indice": {"en": "This is the capital of Spain."}
                                },
                                {
                                    "text": {"en": "Paris"},
                                    "correct": True,
                                    "indice": {"en": "Paris is the city of light"}
                                },
                                {
                                    "text": {"en": "Rome"},
                                    "correct": False,
                                    "indice": {"en": "This is the capital of Italy."}
                                }
                            ]
                        }
                    ]
                }
            }
        }

        # Generate the quiz HTML
        quiz_html = self.plugin.generate_quiz_html(self.plugin.quiz_data['quizzes']['quiz1'])
        soup = BeautifulSoup(quiz_html, 'html.parser')

        # Check that the hint button does not exist since show_indice_on_answer is False
        hint_button = soup.find('button', class_='hint-button')
        self.assertIsNone(hint_button)

        # Validate the media presence (image for this question)
        img_tag = soup.find('img')
        self.assertIsNotNone(img_tag)
        self.assertEqual(img_tag['src'], './static/images/test.png')
        self.assertEqual(img_tag['alt'], 'Paris')

