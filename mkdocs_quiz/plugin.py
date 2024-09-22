import re
import uuid
import json
from mkdocs.plugins import BasePlugin
import os
import warnings
from mkdocs.config import config_options
from mkdocs.structure.files import File

warnings.filterwarnings("ignore")

class QuizPlugin(BasePlugin):
    """
    Simple MkDocs plugin that generates interactive quizzes in MkDocs pages.
    It supports several question types such as : multiple-choice, true/false, fill-in-the-blank, and multi-choice questions.
    The plugin is configured via the MkDocs configuration file see the `mkdocs.yml` file
    """

    config_scheme = (
        ('quiz_file', config_options.Type(str, default='quizzes.json')),
        ('language', config_options.Type(str, default='en')),
        ('show_refresh_button', config_options.Type(bool, default=True)),
        ('show_indice_on_answer', config_options.Type(bool, default=True)),
        ('show_score', config_options.Type(bool, default=True)),
        ('show_progress_bar', config_options.Type(bool, default=True)),
        ('logging', config_options.Type(bool, default=False)),  
    )

    def console_log(self, message):
        """
        Prints a log message if logging is enabled in the plugin configuration.

        Args:
            message (str): The message to print.
        """
        if self.config.get('logging', True):
            print(f"DEBUG MESSAGE: {message}")

    def on_config(self, config):
        """
        Handles the MkDocs configuration loading event.

        This method is called when the MkDocs configuration is loaded, see more on the MkDocs official documentation.

        Args:
            config (Config): The MkDocs configuration object.

        Returns:
            Config: The updated MkDocs configuration.
        """
        self.console_log("Running on_config...")
        quiz_file_path = self.config.get('quiz_file')
        self.language = self.config.get('language', 'en')
        self.show_refresh_button = self.config.get('show_refresh_button', True)
        self.show_indice_on_answer = self.config.get('show_indice_on_answer', True)
        self.show_score = self.config.get('show_score', True)
        self.show_progress_bar = self.config.get('show_progress_bar', True)
        self.console_log(f"Configuration - Language: {self.language}, Show refresh button: {self.show_refresh_button}")

        # Load quiz data
        if quiz_file_path and os.path.isfile(quiz_file_path):
            try:
                with open(quiz_file_path, 'r') as file:
                    self.quiz_data = json.load(file)
                self.console_log(f"Loaded quiz data from {quiz_file_path}: {self.quiz_data}")
            except json.JSONDecodeError as e:
                self.console_log(f"JSON is invalid: {e}")
                self.quiz_data = {'quizzes': {}}
        else:
            self.quiz_data = {'quizzes': {}}
        return config
    
    
    def on_files(self, files, config):
        """
        Handles the event when MkDocs files are loaded, see more on the MkDocs official documentation.

        Args:
            files (Files): The collection of MkDocs files.
            config (Config): The MkDocs configuration object.

        Returns:
            Files: The updated collection of MkDocs files.
        """
        plugin_dir = os.path.dirname(__file__)
        js_file = File(os.path.join(plugin_dir, 'static', 'quiz.js'), config['docs_dir'], config['site_dir'], False)
        css_file = File(os.path.join(plugin_dir, 'static', 'quiz.css'), config['docs_dir'], config['site_dir'], False)
        self.console_log(f"Adding JS file: {js_file}")
        self.console_log(f"Adding CSS file: {css_file}")
        files.append(js_file)
        files.append(css_file)
        return files

    def on_page_markdown(self, markdown, page, config, files):
        """
        Handles the Markdown content of a page before rendering, see more on the MkDocs official documentation.
        Quiz placeholders should be defined in the format `<!-- QUIZ_ID: <quiz_id> -->` in your doc.

        Args:
            markdown (str): The page's Markdown content.
            page (Page): The page object.
            config (Config): The MkDocs configuration object.
            files (Files): The collection of MkDocs files.

        Returns:
            str: The updated Markdown content with quiz placeholders replaced.
        """
        quiz_placeholder_pattern = re.compile(r'<!-- QUIZ_ID: (\w+) -->')
        matches = quiz_placeholder_pattern.findall(markdown)
        self.console_log(f"Running on_page_markdown... Found quiz placeholders: {matches}")

        for quiz_id in matches:
            if quiz_id in self.quiz_data['quizzes']:
                self.console_log(f"Generating HTML for quiz ID: {quiz_id}")
                quiz_html = self.generate_quiz_html(self.quiz_data['quizzes'][quiz_id])
                placeholder = f"<!-- QUIZ_PLACEHOLDER_{quiz_id} -->"
                markdown = markdown.replace(f'<!-- QUIZ_ID: {quiz_id} -->', placeholder)
                page.meta['quiz_placeholder'] = page.meta.get('quiz_placeholder', []) + [(placeholder, quiz_html)]
        
        return markdown
    
    def on_post_page(self, output_content, page, config):
        """
        Handles the post-render event for a page.

        Args:
            output_content (str): The rendered HTML content of the page.
            page (Page): The page object.
            config (Config): The MkDocs configuration object.

        Returns:
            str: The updated HTML content with quizzes and script/style injections.
        """
        if 'quiz_placeholder' in page.meta:
            for placeholder, quiz_html in page.meta['quiz_placeholder']:
                self.console_log(f"Replacing placeholder: {placeholder} with quiz HTML")
                output_content = output_content.replace(placeholder, quiz_html)
        # Inject the JavaScript and CSS into the page
        script_tag = '<script src="static/quiz.js"></script>'
        link_tag = '<link rel="stylesheet" href="static/quiz.css">'
        output_content = output_content.replace('</body>', f'{script_tag}</body>')
        output_content = output_content.replace('</head>', f'{link_tag}</head>')
        return output_content

    def generate_media_html(self, media):
        """
        Generates the HTML for media elements (images, videos, or audio) in quiz questions.

        Args:
            media (dict): A dictionary containing media information. Should contain the keys 'type' and 'src' (and optionally 'alt').

        Returns:
            str: The generated HTML for the media.
        """
        self.console_log(f"Generating media HTML for media type: {media['type']}")
        if media['type'] == 'image':
            return f"<img src='{media['src']}' alt='{media['alt'][self.language]}' class='media-content mb-4'>"
        elif media['type'] == 'video':
            return f"<video controls class='media-content mb-4'><source src='{media['src']}' type='video/mp4'>Your browser does not support the video tag.</video>"
        elif media['type'] == 'audio':
            return f"<audio controls class='media-content mb-4'><source src='{media['src']}' type='audio/mpeg'>Your browser does not support the audio element.</audio>"
        return ''

    def generate_quiz_html(self, quiz):
        """
        This method builds the entire HTML structure for the quiz, including questions, options, media, and
        additional features like refresh buttons and progress bars.

        Args:
            quiz (dict): The quiz data. Should contain a list of questions and other quiz-related metadata.

        Returns:
            str: The generated HTML for the quiz.
        """
        quiz_id = uuid.uuid4().hex
        questions = quiz.get('questions', [])
        self.console_log(f"Generating quiz HTML for quiz ID: {quiz_id}, total questions: {len(questions)}")
        show_refresh_button = 'true' if self.show_refresh_button else 'false'
        show_indice_on_answer = 'true' if self.show_indice_on_answer else 'false'
        show_score = 'true' if self.show_score else 'false'
        show_progress_bar = 'true' if self.show_progress_bar else 'false'
        quiz_html = f"<div class='quiz' id='quiz-{quiz_id}' data-show-refresh-button='{show_refresh_button}' data-show-indice-on-answer='{show_indice_on_answer}' data-show-score='{show_score}' data-show-progress-bar='{show_progress_bar}' data-score='0'>"

        # Add progress bar if enabled
        if self.show_progress_bar:
            quiz_html += """
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: 0%;"></div>
            </div>
            """

        for question in questions:
            question_id = uuid.uuid4().hex
            question_text = question['question'].get(self.language, question['question']['en'])
            media = question.get('media', None)
            quiz_type = question.get('type', 'multiple-choice')
            self.console_log(f"Processing question ID: {question_id}, Type: {quiz_type}, Text: {question_text}")
            quiz_html += f"<div class='question p-4 border border-gray-200 rounded-lg shadow-md mb-6' id='question-{question_id}' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-quiz-type='{quiz_type}'>"

            if media:
                quiz_html += self.generate_media_html(media)

            quiz_html += f"<p class='font-bold text-lg mb-4'>{question_text}"
            if self.show_indice_on_answer:
                quiz_html += f""" <button class='hint-button' data-indice='{question.get("indice", {}).get(self.language, question.get("indice", {}).get("en", ""))}'><i class='fa fa-lightbulb-o'></i></button>"""
            quiz_html += f"</p>"

            if quiz_type in ['multiple-choice', 'true-false']:
                options = question.get('options', [])
                quiz_html += f"<ul class='list-none p-0'>"
                self.console_log(f"Multiple choice/true-false options: {options}")
                for i, option in enumerate(options):
                    text = option['text'].get(self.language, option['text']['en'])
                    indice = option.get('indice', {}).get(self.language, option.get('indice', {}).get('en', ''))
                    correct = 'correct' if option['correct'] else 'incorrect'
                    quiz_html += f"""
                        <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-option-id='{i}' data-indice='{indice}'>
                            {text}
                        </li>
                    """
                quiz_html += "</ul>"
                if self.show_indice_on_answer:
                    quiz_html += f"<div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'></div>"
                quiz_html += f"<div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>"
            
            elif quiz_type == 'fill-in-the-blank':
                self.console_log("Processing fill-in-the-blank question...")
                answer = question['answer'].get(self.language, question['answer']['en']).strip().lower()
                self.console_log(f"Fill-in-the-blank question with answer: {answer}")
                indice = question.get('indice', {}).get(self.language, question.get('indice', {}).get('en', ''))
                self.console_log(f"Indice for fill-in-the-blank: {indice}")
                
                quiz_html += f"""
                    <input type='text' class='answer-input p-2 mb-2 border border-gray-200 rounded-lg' id='answer-{question_id}' data-answer='{answer}'>
                    <button class='submit-answer bg-blue-500 text-white p-2 rounded-lg' data-question-id='{question_id}'>Submit</button>
                
                """
                if self.show_indice_on_answer and indice:
                    self.console_log(f"Showing indice for fill-in-the-blank question ID: {question_id}")
                    quiz_html += f"""
                    <div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'>{indice}</div>
                    """
                quiz_html += f"<div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>"
                self.console_log(f"Generated HTML for fill-in-the-blank question ID: {question_id}")
                    
            elif quiz_type == 'multi-choice':
                options = question.get('options', [])
                quiz_html += f"<ul class='list-none p-0'>"
                for i, option in enumerate(options):
                    text = option['text'].get(self.language, option['text']['en'])
                    indice = option.get('indice', {}).get(self.language, option.get('indice', {}).get('en', ''))
                    correct = 'correct' if option['correct'] else 'incorrect'
                    quiz_html += f"""
                        <li class='{correct} p-2 mb-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-100' data-quiz-id='{quiz_id}' data-question-id='{question_id}' data-option-id='{i}' data-indice='{indice}'>
                            <input type="checkbox" class="multi-choice-checkbox" data-option-id="{i}"> <span>{text}</span>
                        </li>
                    """
                quiz_html += "</ul>"
                if self.show_indice_on_answer:
                    quiz_html += f"<div class='indice mt-4 p-3 border border-yellow-300 bg-yellow-100 text-yellow-700 rounded-lg hidden' id='indice-{question_id}'></div>"
                quiz_html += f"<div class='feedback mt-4 p-3 rounded-lg hidden' id='feedback-{question_id}'></div>"
                quiz_html += f"<button class='submit-multi-choice bg-blue-500 text-white p-2 rounded-lg' data-quiz-id='{quiz_id}' data-question-id='{question_id}'>Submit</button>"

            quiz_html += "</div>"

        if self.show_refresh_button:
            quiz_html += "<button class='refresh-quiz bg-blue-500 text-white p-2 rounded-lg mt-4'>Refresh</button>"
        
        if self.show_score:
            quiz_html += "<div class='score mt-4 text-lg font-bold hidden'>Score: 0</div>"
        
        quiz_html += "</div>"
        self.console_log(f"Generated HTML for quiz ID: {quiz_id}")
        return quiz_html
