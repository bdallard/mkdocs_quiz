import unittest
from unittest.mock import patch, mock_open
from mkdocs.config import Config, config_options
from mkdocs_quiz.plugin import QuizPlugin

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = QuizPlugin()
        self.mock_schema = (
            ('site_name', config_options.Type(str, default='My Docs')),
            ('site_url', config_options.Type(str, default='')),
            ('extra_css', config_options.Type(list, default=[
                'stylesheets/extra.css',
                'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
            ])),
            ('extra_javascript', config_options.Type(list, default=[
                'javascripts/extra.js'
            ])),
        )
        self.config = Config(self.mock_schema)

    def load_plugin_config(self, quiz_file='quizzes.json', language='en', show_refresh_button=True,
                           show_indice_on_answer=True, show_score=True, show_progress_bar=True, logging=False):
        """
        Loads plugin configuration options based on the options in your mkdocs.yml
        Now includes the logging option.
        """
        self.plugin.config = {
            'quiz_file': quiz_file,
            'language': language,
            'show_refresh_button': show_refresh_button,
            'show_indice_on_answer': show_indice_on_answer,
            'show_score': show_score,
            'show_progress_bar': show_progress_bar,
            'logging': logging,  # New logging option
        }
        self.config.load_dict(self.plugin.config)
        self.plugin.on_config(self.config)

    def test_plugin_config_loading(self):
        # Load the config with the defaults from mkdocs.yml
        self.load_plugin_config()

        # Assert the plugin config is loaded correctly
        self.assertEqual(self.plugin.config['quiz_file'], 'quizzes.json')
        self.assertEqual(self.plugin.config['language'], 'en')
        self.assertTrue(self.plugin.config['show_refresh_button'])
        self.assertTrue(self.plugin.config['show_indice_on_answer'])
        self.assertTrue(self.plugin.config['show_score'])
        self.assertTrue(self.plugin.config['show_progress_bar'])
        self.assertFalse(self.plugin.config['logging'])  # Ensure logging is false by default

    def test_plugin_config_custom_values(self):
        # Load the config with custom values
        self.load_plugin_config(
            quiz_file='custom_quiz.json',
            language='fr',
            show_refresh_button=False,
            show_indice_on_answer=False,
            show_score=False,
            show_progress_bar=False,
            logging=True  # Custom logging value
        )

        # Assert the plugin config is updated with custom values
        self.assertEqual(self.plugin.config['quiz_file'], 'custom_quiz.json')
        self.assertEqual(self.plugin.config['language'], 'fr')
        self.assertFalse(self.plugin.config['show_refresh_button'])
        self.assertFalse(self.plugin.config['show_indice_on_answer'])
        self.assertFalse(self.plugin.config['show_score'])
        self.assertFalse(self.plugin.config['show_progress_bar'])
        self.assertTrue(self.plugin.config['logging'])  # Ensure logging is set to true
