const tabButtons = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');
const scoreDisplay = document.getElementById('score');

let score = 0;

const updateScore = (value) => {
  score += value;
  scoreDisplay.textContent = score;
};

const showTab = (tabId) => {
  tabButtons.forEach((button) => {
    const isActive = button.dataset.tab === tabId;
    button.classList.toggle('active', isActive);
    button.setAttribute('aria-selected', String(isActive));
  });

  tabPanels.forEach((panel) => {
    panel.classList.toggle('active', panel.id === tabId);
  });
};

tabButtons.forEach((button) => {
  button.addEventListener('click', () => showTab(button.dataset.tab));
});

const ensureFeedback = (trigger) => {
  let feedback = trigger.parentElement.querySelector('.feedback');

  if (!feedback) {
    feedback = document.createElement('div');
    feedback.className = 'feedback';
    trigger.parentElement.appendChild(feedback);
  }

  return feedback;
};

const showFeedback = (element, message, type) => {
  if (!element) return;
  element.textContent = message;
  element.className = 'feedback ' + type;
};

const processAnswer = (button, isCorrect, points = 5, successMessage, errorMessage) => {
  if (button.dataset.locked === 'true') return;

  const feedback = ensureFeedback(button);
  button.dataset.locked = 'true';

  document.querySelectorAll('.answer-btn').forEach((btn) => {
    if (btn.closest('.card') !== button.closest('.card')) {
      return;
    }

    btn.classList.remove('correct', 'incorrect');
    if (btn === button) {
      btn.classList.add(isCorrect ? 'correct' : 'incorrect');
    }
  });

  if (isCorrect) {
    updateScore(points);
  }

  showFeedback(
    feedback,
    isCorrect ? successMessage : errorMessage,
    isCorrect ? 'success' : 'error'
  );
};

document.querySelectorAll('.answer-btn').forEach((button) => {
  button.addEventListener('click', () => {
    const isCorrect = button.dataset.correct === 'true';
    const points = Number(button.dataset.score || 5);

    processAnswer(
      button,
      isCorrect,
      points,
      `MUITO BEM! VOCÊ ACERTOU +${points} PONTOS!`,
      'TENTE NOVAMENTE!'
    );
  });
});

document.querySelectorAll('.check-copy').forEach((button) => {
  button.addEventListener('click', () => {
    const input = button.previousElementSibling;
    const answer = input.dataset.answer || '';
    const value = input.value.trim().toLowerCase();
    const isCorrect = value === answer.toLowerCase();
    const points = Number(button.dataset.score || 5);

    if (button.dataset.locked === 'true') return;
    button.dataset.locked = 'true';

    if (isCorrect) {
      updateScore(points);
    }

    const feedback = ensureFeedback(button);
    showFeedback(
      feedback,
      isCorrect ? `PERFEITO! VOCÊ GANHOU +${points} PONTOS!` : 'QUASE LÁ! TENTE NOVAMENTE.',
      isCorrect ? 'success' : 'error'
    );
  });
});

const posterTitleInput = document.getElementById('posterTitle');
const studentNameInput = document.getElementById('studentName');
const posterTextInput = document.getElementById('posterText');
const previewTitle = document.getElementById('previewTitle');
const previewStudent = document.getElementById('previewStudent');
const previewMessage = document.getElementById('previewMessage');
const previewFigures = document.getElementById('previewFigures');
const figureButtons = document.querySelectorAll('.figure-option');

const updatePosterPreview = () => {
  const selectedFigures = [...figureButtons]
    .filter((button) => button.classList.contains('selected'))
    .map((button) => button.dataset.figure || '');

  previewTitle.textContent = posterTitleInput.value.trim() || 'FOLCLORE BRASILEIRO';
  previewStudent.textContent = studentNameInput.value.trim() || 'ALUNO';
  previewMessage.textContent = posterTextInput.value.trim() || 'EU AMO O FOLCLORE BRASILEIRO!';

  previewFigures.innerHTML = selectedFigures.length
    ? selectedFigures.map((figure) => `<span>${figure}</span>`).join('')
    : '<span>🧑‍🦯 SACI-PERERÊ</span>';
};

figureButtons.forEach((button) => {
  button.addEventListener('click', () => {
    button.classList.toggle('selected');
    updatePosterPreview();
  });
});

posterTitleInput?.addEventListener('input', updatePosterPreview);
studentNameInput?.addEventListener('input', updatePosterPreview);
posterTextInput?.addEventListener('input', updatePosterPreview);

const readyButton = document.querySelector('.ready-btn');
readyButton?.addEventListener('click', () => {
  if (readyButton.dataset.locked === 'true') return;
  readyButton.dataset.locked = 'true';
  updateScore(10);

  const feedback = ensureFeedback(readyButton);
  showFeedback(
    feedback,
    'EXCELENTE! VOCÊ CRIOU UMA IDEIA DE CARTAZ E GANHOU +10 PONTOS!',
    'success'
  );
});

document.querySelector('.export-pdf-btn')?.addEventListener('click', () => {
  const preview = document.getElementById('posterPreview');

  if (!preview) return;

  showTab('cartaz');
  preview.scrollIntoView({ behavior: 'smooth', block: 'center' });

  const printWrapper = document.createElement('div');
  printWrapper.className = 'poster-print-wrapper';
  const clone = preview.cloneNode(true);
  clone.classList.add('print-clone');
  printWrapper.appendChild(clone);
  document.body.appendChild(printWrapper);

  setTimeout(() => {
    window.print();
    setTimeout(() => {
      printWrapper.remove();
    }, 300);
  }, 200);
});

updatePosterPreview();
