// Anniversary Cards Bundle
// This file loads all anniversary custom cards automatically

// Load all card files
const cardFiles = [
  'anniversary-timeline-card.js',
  'anniversary-details-card.js',
  'anniversary-calendar-card.js', 
  'anniversary-stats-card.js'
];

const baseUrl = '/local/custom_components/anniversaries/www/';

// Function to load a script dynamically
function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.type = 'module';
    script.src = src;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

// Load all card scripts
async function loadAnniversaryCards() {
  console.info(
    '%c  ANNIVERSARY-CARDS-BUNDLE  %c  Loading cards...  ',
    'color: orange; font-weight: bold; background: black',
    'color: white; font-weight: bold; background: dimgray'
  );

  try {
    for (const file of cardFiles) {
      await loadScript(baseUrl + file);
      console.debug(`Loaded anniversary card: ${file}`);
    }
    
    console.info(
      '%c  ANNIVERSARY-CARDS-BUNDLE  %c  All cards loaded successfully!  ',
      'color: orange; font-weight: bold; background: black',
      'color: white; font-weight: bold; background: green'
    );
  } catch (error) {
    console.error('Failed to load anniversary cards:', error);
  }
}

// Load cards when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadAnniversaryCards);
} else {
  loadAnniversaryCards();
}
