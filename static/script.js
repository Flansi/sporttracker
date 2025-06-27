    // Umschalten der Optionslisten
    document.querySelectorAll('.toggle').forEach((btn) => {
      btn.addEventListener('click', () => {
        const list = btn.previousElementSibling;
        const hiddenNow = list.classList.toggle('hidden');
        btn.textContent = hiddenNow ? 'Optionen zeigen' : 'Optionen verbergen';
      });
    });
