# Mkdocs Quizz 

## Installation 

```
pip install mkdocs_quiz
```

### Add extra js/css

Go to your `docs/` folder and create : 

- `javascripts/extra.js` file here : 
- `stylesheets/extra.css` file here : 

Then add to `mkdocs.yml` file this lines :  

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

### Create a `quizzes.json` file 

Ensure your `quizzes` JSON file is structured like this :

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
                    "options": [
                        {
                            "text": {
                                "en": "Berlin",
                                "fr": "Berlin"
                            },
                            "correct": false,
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
                            "correct": false,
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
                            "correct": true,
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
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Italy.",
                                "fr": "Ceci est la capitale de l'Italie."
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
                    "options": [
                        {
                            "text": {
                                "en": "True",
                                "fr": "Vrai"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The Earth is round.",
                                "fr": "La Terre est ronde."
                            }
                        },
                        {
                            "text": {
                                "en": "False",
                                "fr": "Faux"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
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
                    "answer": {
                        "en": "Jupiter",
                        "fr": "Jupiter"
                    },
                    "indice": {
                        "en": "It is a gas giant.",
                        "fr": "C'est une géante gazeuse."
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
                                "fr": "Rouge est une couleur primaire."
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
                                "fr": "Bleu est une couleur primaire."
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
                                "fr": "Vert est une couleur secondaire."
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
                                "fr": "Jaune est une couleur primaire."
                            }
                        }
                    ]
                }
            ]
        },
        "quiz2": {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "Which element has the chemical symbol 'O'?",
                        "fr": "Quel élément a le symbole chimique 'O'?"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "Oxygen",
                                "fr": "Oxygène"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "Gold",
                                "fr": "Or"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for gold is 'Au'.",
                                "fr": "Le symbole de l'or est 'Au'."
                            }
                        },
                        {
                            "text": {
                                "en": "Osmium",
                                "fr": "Osmium"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for osmium is 'Os'.",
                                "fr": "Le symbole de l'osmium est 'Os'."
                            }
                        },
                        {
                            "text": {
                                "en": "Hydrogen",
                                "fr": "Hydrogène"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for hydrogen is 'H'.",
                                "fr": "Le symbole de l'hydrogène est 'H'."
                            }
                        }
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "Water boils at 100°C.",
                        "fr": "L'eau bout à 100°C."
                    },
                    "options": [
                        {
                            "text": {
                                "en": "True",
                                "fr": "Vrai"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "False",
                                "fr": "Faux"
                            },
                            "correct": false,
                            "indice": {
                                "en": "At sea level, water boils at 100°C.",
                                "fr": "Au niveau de la mer, l'eau bout à 100°C."
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "The chemical formula for water is ___.",
                        "fr": "La formule chimique de l'eau est ___."
                    },
                    "answer": {
                        "en": "H2O",
                        "fr": "H2O"
                    },
                    "indice": {
                        "en": "It consists of two hydrogen atoms and one oxygen atom.",
                        "fr": "Elle se compose de deux atomes d'hydrogène et d'un atome d'oxygène."
                    }
                }
            ]
        }
    }
}
```

### Run the mkdocs server like usual

```
mkdocs serve
``` 

