# Mkdocs Quiz

`mkdocs_quiz` is a MkDocs plugin that allows you to integrate interactive quizzes into your documentation site using custom JSON files. This plugin supports multiple quiz types, including multiple-choice, true-false, fill-in-the-blank questions. It provides options to customize quiz behavior and appearance, enhancing user engagement with your documentation.

[![CI](https://github.com/bdallard/mkdocs_quiz/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bdallard/mkdocs_quiz/actions/workflows/ci.yml)

## Features

- **Multiple Quiz Types**: Support for various question formats.
- **Media Support**: Include images, videos, and audio in your quizzes.
- **Multi-language Support**: Define questions and options in multiple languages.
- **Customizable Options**: Control quiz behavior through configuration settings.
- **Progress Tracking**: Display scores and progress bars.
- **Hints and Indices**: Provide hints based on user responses.

## Installation

First, ensure you have MkDocs installed. If you don't, check it out [here](https://github.com/mkdocs/mkdocs).

Install the `mkdocs_quiz` plugin using pip:

```bash
pip install mkdocs_quiz
```

---

## Quick Start Guide

### Create your MkDocs project

If you don't already have a MkDocs project, create one:

```bash
mkdocs new my-project
cd my-project
```

Your project directory should look like this:

```
my-project/
├── docs/
│   ├── javascripts/
│   │   └── extra.js
│   ├── stylesheets/
│   │   └── extra.css
│   └── static/
│       └── audios/
│       └── images/
│       └── videos/
├── mkdocs.yml
└── quizzes.json
```

### Update `mkdocs.yml`

Configure your `mkdocs.yml` to include the plugin and reference necessary CSS and JavaScript files:

```yaml
site_name: My Docs

plugins:
  - search
  - mkdocs_quiz:
      quiz_file: quizzes.json
      language: en
      show_refresh_button: true
      show_indice_on_answer: true
      show_score: true
      show_progress_bar: true
      logging: true

extra_css:
  - stylesheets/extra.css
  - https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css

extra_javascript:
  - javascripts/extra.js
```

### Create your json quiz file

Create a `quizzes.json` file in the root of your project directory. This file will contain your quiz data and configuration options. Here's an example structure:

```json
{
  "quizzes": {
    "quiz1": {
      "questions": [
        {
          "type": "multiple-choice",
          "question": {
            "en": "What is the capital of France?",
            "fr": "Quelle est la capitale de la France?"
          },
          "media": {
            "type": "image",
            "src": "./static/images/paris.png",
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
              "correct": false,
              "indice": {
                "en": "Berlin is the capital of Germany.",
                "fr": "Berlin est la capitale de l'Allemagne."
              }
            },
            {
              "text": {
                "en": "Madrid",
                "fr": "Madrid"
              },
              "correct": false,
              "indice": {
                "en": "Madrid is the capital of Spain.",
                "fr": "Madrid est la capitale de l'Espagne."
              }
            },
            {
              "text": {
                "en": "Paris",
                "fr": "Paris"
              },
              "correct": true,
              "indice": {
                "en": "Correct! Paris is known as the City of Light.",
                "fr": "Correct! Paris est connue comme la Ville Lumière."
              }
            },
            {
              "text": {
                "en": "Rome",
                "fr": "Rome"
              },
              "correct": false,
              "indice": {
                "en": "Rome is the capital of Italy.",
                "fr": "Rome est la capitale de l'Italie."
              }
            }
          ]
        },
        {
          "type": "true-false",
          "question": {
            "en": "The Earth is flat.",
            "fr": "La Terre est plate."
          },
          "media": {
            "type": "video",
            "src": "./static/videos/earth.mp4",
            "alt": {
              "en": "Earth",
              "fr": "Terre"
            }
          },
          "options": [
            {
              "text": {
                "en": "True",
                "fr": "Vrai"
              },
              "correct": false,
              "indice": {
                "en": "Incorrect. The Earth is round.",
                "fr": "Incorrect. La Terre est ronde."
              }
            },
            {
              "text": {
                "en": "False",
                "fr": "Faux"
              },
              "correct": true,
              "indice": {
                "en": "Correct! The Earth is spherical.",
                "fr": "Correct! La Terre est sphérique."
              }
            }
          ]
        },
        {
          "type": "fill-in-the-blank",
          "question": {
            "en": "____ is the largest planet in our solar system.",
            "fr": "____ est la plus grande planète de notre système solaire."
          },
          "media": {
            "type": "audio",
            "src": "./static/audios/jupiter.mp3",
            "alt": {
              "en": "Largest planet",
              "fr": "Plus grande planète"
            }
          },
          "answer": {
            "en": "Jupiter",
            "fr": "Jupiter"
          },
          "indice": {
            "en": "Hint: It's a gas giant.",
            "fr": "Indice: C'est une géante gazeuse."
          }
        },
        {
          "type": "multi-choice",
          "question": {
            "en": "Select the primary colors:",
            "fr": "Sélectionnez les couleurs primaires :"
          },
          "options": [
            {
              "text": {
                "en": "Red",
                "fr": "Rouge"
              },
              "correct": true,
              "indice": {
                "en": "Red is a primary color.",
                "fr": "Le rouge est une couleur primaire."
              }
            },
            {
              "text": {
                "en": "Blue",
                "fr": "Bleu"
              },
              "correct": true,
              "indice": {
                "en": "Blue is a primary color.",
                "fr": "Le bleu est une couleur primaire."
              }
            },
            {
              "text": {
                "en": "Green",
                "fr": "Vert"
              },
              "correct": false,
              "indice": {
                "en": "Green is a secondary color.",
                "fr": "Le vert est une couleur secondaire."
              }
            },
            {
              "text": {
                "en": "Yellow",
                "fr": "Jaune"
              },
              "correct": true,
              "indice": {
                "en": "Yellow is a primary color.",
                "fr": "Le jaune est une couleur primaire."
              }
            }
          ]
        }
      ]
    }
    // Add more quizzes as needed
  }
}
```

> Ensure that fields like `indice` are included if `show_indice_on_answer` is set to `true` in your configuration, same for the other options 🤓

### Integrate your quizzes in your markdown files

Include quizzes in your documentation by referencing them in your Markdown files using the `<!-- QUIZ_ID: quiz_name -->` syntax.

Example `docs/index.md`:

```markdown
# Geography Quiz

Test your knowledge about world capitals.

<!-- QUIZ_ID: quiz1 -->

# Space Quiz

Challenge yourself with questions about space.

<!-- QUIZ_ID: quiz2 -->
```

### Run the Documentation Site

Start the MkDocs development server to test your site with quizzes:

```bash
mkdocs serve
```

Open your browser and navigate to `http://localhost:8000` to see your quizzes in action.

--- 

## Testing

This test suite ensures the correctness and robustness of the `mkdoc-qcm` plugin, covering multiple aspects such as HTML generation, quiz logic, UI components, and configuration options.

### Tools used

- **unittest**: For writing unit tests.
- **BeautifulSoup**: For parsing and asserting HTML content.
- **mock**: For simulating quiz data.

### Test structure

The test suite is organized into four main files:

1. **`test_html_generation.py`**: Tests for generating quiz HTML
2. **`test_logic.py`**: Tests for quiz logic and functionality
3. **`test_ui_components.py`**: Tests for optional UI elements
4. **`test_mock.py`**: End-to-end testing with mock data integration

### Running test with `tox`

To run the tests, use the `tox` command:

```bash
tox
```