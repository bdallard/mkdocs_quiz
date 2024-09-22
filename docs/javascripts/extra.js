document.addEventListener("DOMContentLoaded", function () {
    const quizzes = document.querySelectorAll('.quiz');

    quizzes.forEach(quiz => {
        const questions = quiz.querySelectorAll('.question');
        let score = 0;
        let answeredQuestions = 0;
        const totalQuestions = questions.length;
        const showProgressBar = quiz.getAttribute('data-show-progress-bar') === 'true';
        const progressBarContainer = quiz.querySelector('.progress-bar-container');

        // initialize progress bar
        if (showProgressBar) {
            if (progressBarContainer) {
                progressBarContainer.style.display = 'block';
            }
        } else {
            if (progressBarContainer) {
                progressBarContainer.style.display = 'none';
            }
        }

        // update the score
        function updateScore(increment) {
            score += increment;
            quiz.querySelector('.score').textContent = `Score: ${score} / ${totalQuestions}`;
            //console.log(`Updated score: ${score}`);
        }

        // check if quiz is completed
        function checkCompletion() {
            if (answeredQuestions === totalQuestions) {
                quiz.querySelector('.score').classList.remove('hidden');
                //console.log(`Quiz complete! Total score: ${score}`);
            }
        }

        // update the progress bar
        function updateProgressBar() {
            if (showProgressBar) {
                const progress = (answeredQuestions / totalQuestions) * 100;
                quiz.querySelector('.progress-bar').style.width = `${progress}%`;
                //console.log(`Progress bar updated: ${progress}%`);
            }
        }
        // question loop 
        questions.forEach(question => {
            const quizType = question.getAttribute('data-quiz-type');
            const feedbackDiv = question.querySelector('.feedback');
            const indiceDiv = question.querySelector('.indice');
            //console.log(`Processing question of type: ${quizType}`);

            if (quizType === 'multiple-choice' || quizType === 'true-false') {
                const options = question.querySelectorAll('li');

                options.forEach(option => {
                    option.addEventListener('click', () => {
                        const selectedOptions = option.parentElement.querySelectorAll('.selected');

                        if (selectedOptions.length === 0) {
                            answeredQuestions++;
                            const isCorrect = option.classList.contains('correct');
                            //console.log(`Option selected: ${isCorrect ? "Correct" : "Incorrect"}`);
                            updateScore(isCorrect ? 1 : 0);
                            checkCompletion();
                            updateProgressBar();
                        }

                        option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                        option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                        // show feedback and hint for answers
                        const dataIndice = option.getAttribute('data-indice');
                        indiceDiv.textContent = dataIndice;
                        indiceDiv.classList.remove('hidden');

                        if (option.classList.contains('incorrect')) {
                            option.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        } else {
                            option.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        }
                        feedbackDiv.textContent = dataIndice;
                        feedbackDiv.classList.remove('hidden');

                        // Scroll to the next question if it exists
                        const nextQuestion = question.nextElementSibling;
                        if (nextQuestion && nextQuestion.classList.contains('question')) {
                            nextQuestion.scrollIntoView({ behavior: 'smooth' });
                        }
                    });
                });

                // Hint button functionality
                const hintButton = question.querySelector('.hint-button');
                if (hintButton) {
                    hintButton.addEventListener('click', () => {
                        const hintIndice = hintButton.getAttribute('data-indice');
                        //console.log(`Hint clicked: ${hintIndice}`);
                        indiceDiv.textContent = hintIndice;
                        indiceDiv.classList.toggle('hidden');
                    });
                }
                //BEUG HERE 
            } else if (quizType === 'fill-in-the-blank') {

                const submitButton = question.querySelector('.submit-answer');
                const answerInput = question.querySelector(`#answer-${question.getAttribute('data-question-id')}`);  // Get answer input by data-question-id
                //console.log(`Answer input field: `, answerInput); // Check if answerInput is found

                // Get the correct answer from the data-answer attribute of the input field
                const correctAnswer = answerInput.getAttribute('data-answer');
                //console.log(`Correct answer for fill-in-the-blank: ${correctAnswer}`);

                // Get the correct indiceDiv and feedbackDiv by question_id
                const questionId = question.getAttribute('data-question-id');
                const indiceDiv = question.querySelector(`#indice-${questionId}`);
                const feedbackDiv = question.querySelector(`#feedback-${questionId}`);
                //console.log(`Indices fill-in-the-blank: ${indiceDiv.textContent}`);

                submitButton.addEventListener('click', () => {
                    const submittedAnswer = answerInput.value.trim().toLowerCase();
                    console.log(`Submitted answer: ${submittedAnswer}`);

                    if (!answerInput.classList.contains('answered')) {
                        answeredQuestions++;
                        answerInput.classList.add('answered');
                        const isCorrect = submittedAnswer === correctAnswer.trim().toLowerCase();
                        //console.log(`Is the submitted answer correct? ${isCorrect}`);
                        updateScore(isCorrect ? 1 : 0);
                        updateProgressBar();
                        checkCompletion();
                    }

                    if (submittedAnswer === correctAnswer.trim().toLowerCase()) {
                        answerInput.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        indiceDiv.classList.add('hidden');
                        feedbackDiv.textContent = "Correct!";
                        feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    } else {
                        answerInput.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        const dataIndice = submitButton.getAttribute('data-indice');

                        // Display the indice and incorrect feedback
                        if (indiceDiv) {
                            indiceDiv.textContent = dataIndice;
                            indiceDiv.classList.remove('hidden');
                        }

                        feedbackDiv.textContent = "Incorrect!";
                        feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    }
                    feedbackDiv.classList.remove('hidden');

                    // Scroll to the next question if it exists
                    const nextQuestion = question.nextElementSibling;
                    if (nextQuestion && nextQuestion.classList.contains('question')) {
                        nextQuestion.scrollIntoView({ behavior: 'smooth' });
                    }
                });

                const hintButton = question.querySelector('.hint-button');
                if (hintButton) {
                    hintButton.addEventListener('click', () => {
                        const hintIndice = hintButton.getAttribute('data-indice');
                        //console.log(`Hint clicked: ${hintIndice}`);
                        indiceDiv.textContent = hintIndice;
                        indiceDiv.classList.toggle('hidden');
                    });
                }
            } else if (quizType === 'multi-choice') {
                const submitButton = question.querySelector('.submit-multi-choice');
                submitButton.addEventListener('click', () => {
                    if (!question.classList.contains('answered')) {
                        answeredQuestions++;
                        question.classList.add('answered');

                        const selectedOptions = question.querySelectorAll('.multi-choice-checkbox:checked');
                        let correctAnswers = 0;
                        let totalCorrectOptions = question.querySelectorAll('li.correct').length;

                        selectedOptions.forEach(option => {
                            const li = option.parentElement;
                            const dataIndice = li.getAttribute('data-indice');
                            if (li.classList.contains('correct')) {
                                li.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                                correctAnswers++;
                            } else {
                                li.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                            }
                            feedbackDiv.textContent = dataIndice;
                            feedbackDiv.classList.remove('hidden');
                        });

                        updateScore(correctAnswers === totalCorrectOptions ? 1 : 0);
                        checkCompletion();
                        updateProgressBar();

                        // Scroll to the next question if it exists
                        const nextQuestion = question.nextElementSibling;
                        if (nextQuestion && nextQuestion.classList.contains('question')) {
                            nextQuestion.scrollIntoView({ behavior: 'smooth' });
                        }
                    }
                });

                // Hint button functionality
                const hintButton = question.querySelector('.hint-button');
                if (hintButton) {
                    hintButton.addEventListener('click', () => {
                        const hintIndice = hintButton.getAttribute('data-indice');
                        indiceDiv.textContent = hintIndice;
                        indiceDiv.classList.toggle('hidden');
                    });
                }
            }
        });

        // Refresh button functionality
        const refreshButton = quiz.querySelector('.refresh-quiz');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => {
                score = 0;
                answeredQuestions = 0;
                quiz.querySelector('.score').textContent = `Score: ${score} / ${totalQuestions}`;
                quiz.querySelector('.score').classList.add('hidden');
                if (showProgressBar && progressBarContainer) {
                    quiz.querySelector('.progress-bar').style.width = '0%';
                }
                questions.forEach(question => {
                    const quizType = question.getAttribute('data-quiz-type');
                    const feedbackDiv = question.querySelector('.feedback');
                    const indiceDiv = question.querySelector('.indice');  // Ensure we get the hint div here

                    if (quizType === 'multiple-choice' || quizType === 'true-false') {
                        const options = question.querySelectorAll('li');

                        options.forEach(option => {
                            option.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100', 'bg-red-100', 'border-red-500', 'text-red-700', 'bg-green-100', 'border-green-500', 'text-green-700');
                        });

                        indiceDiv.classList.add('hidden');
                        feedbackDiv.classList.add('hidden');
                        //BEUG HERE ?? I DO NOT KNOW BECAUSE I CAN SEE ANY ACTIONS
                    } else if (quizType === 'fill-in-the-blank') {
                        const answerInput = question.querySelector(`#answer-${question.id.split('-')[1]}`);

                        answerInput.value = '';
                        answerInput.classList.remove('bg-green-100', 'border-green-500', 'text-green-700', 'bg-red-100', 'border-red-500', 'text-red-700', 'answered');
                        indiceDiv.classList.add('hidden');
                        feedbackDiv.classList.add('hidden');
                    } else if (quizType === 'multi-choice') {
                        const options = question.querySelectorAll('li');
                        options.forEach(option => {
                            option.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100', 'bg-red-100', 'border-red-500', 'text-red-700', 'bg-green-100', 'border-green-500', 'text-green-700');
                            const checkbox = option.querySelector('.multi-choice-checkbox');
                            checkbox.checked = false;
                        });

                        question.classList.remove('answered');
                        indiceDiv.classList.add('hidden');
                        feedbackDiv.classList.add('hidden');
                    }
                });
            });
        }

        // Add score display element
        const scoreDisplay = document.createElement('div');
        scoreDisplay.classList.add('score', 'hidden', 'mt-4', 'p-2', 'border', 'border-gray-300', 'bg-gray-100', 'rounded-lg', 'text-center');
        scoreDisplay.textContent = `Score: ${score} / ${totalQuestions}`;
        quiz.appendChild(scoreDisplay);
    });
});
