# Mock quiz data for testing - change it if you want to add a new feature 
mock_quiz_data = {
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
                            "correct": False,
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
                            "correct": False,
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
                            "correct": True,
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
                            "correct": False,
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
                    "media": {
                        "type": "video",
                        "src": "./static/videos/test.mp4",
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
                            "correct": False,
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
                            "correct": True,
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
                    "media": {
                        "type": "audio",
                        "src": "./static/audios/test.mp3",
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
                        "en": "It is a gas giant.",
                        "fr": "C'est une géante gazeuse."
                    }
                }
            ]
        }
    }
}

