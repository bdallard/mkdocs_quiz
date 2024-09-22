document.addEventListener("DOMContentLoaded", function () {
    const quizzes = document.querySelectorAll('.quiz');

    quizzes.forEach(quiz => {
        const questions = quiz.querySelectorAll('.question');

        questions.forEach(question => {
            const quizType = question.getAttribute('data-quiz-type');
            const feedbackDiv = question.querySelector('.feedback');

            if (quizType === 'multiple-choice' || quizType === 'true-false') {
                const options = question.querySelectorAll('li');
                const indiceDiv = question.querySelector('.indice');

                options.forEach(option => {
                    option.addEventListener('click', () => {
                        option.parentElement.querySelectorAll('li').forEach(li => li.classList.remove('selected', 'font-bold', 'border-blue-500', 'bg-blue-100'));
                        option.classList.add('selected', 'font-bold', 'border-blue-500', 'bg-blue-100');

                        // Show feedback and indice for incorrect answers
                        if (option.classList.contains('incorrect')) {
                            indiceDiv.textContent = option.getAttribute('data-indice');
                            indiceDiv.classList.remove('hidden');
                            option.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                            feedbackDiv.textContent = "Incorrect!";
                            feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        } else {
                            indiceDiv.classList.add('hidden');
                            option.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                            feedbackDiv.textContent = "Correct!";
                            feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        }
                        feedbackDiv.classList.remove('hidden');
                    });
                });
            } else if (quizType === 'fill-in-the-blank') {
                const submitButton = question.querySelector('.submit-answer');
                const answerInput = question.querySelector(`#answer-${question.id.split('-')[1]}`);
                const indiceDiv = question.querySelector('.indice');
                const correctAnswer = question.getAttribute('data-answer');

                submitButton.addEventListener('click', () => {
                    if (answerInput.value.trim().toLowerCase() === correctAnswer.trim().toLowerCase()) {
                        answerInput.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                        indiceDiv.classList.add('hidden');
                        feedbackDiv.textContent = "Correct!";
                        feedbackDiv.classList.add('bg-green-100', 'border-green-500', 'text-green-700');
                    } else {
                        answerInput.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                        indiceDiv.classList.remove('hidden');
                        feedbackDiv.textContent = "Incorrect!";
                        feedbackDiv.classList.add('bg-red-100', 'border-red-500', 'text-red-700');
                    }
                    feedbackDiv.classList.remove('hidden');
                });
            }
        });
    });
});

