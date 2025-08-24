/**
 * Anniversary Details Card
 * Focus on a single anniversary with rich details and all attributes
 */

class AnniversaryDetailsCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = {
      entity: config.entity,
      show_attributes: config.show_attributes !== false,
      show_background: config.show_background !== false,
      show_animation: config.show_animation !== false,
      compact_mode: config.compact_mode || false,
      ...config
    };
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getZodiacEmoji(sign) {
    const zodiacEmojis = {
      'Aquarius': '♒', 'Pisces': '♓', 'Aries': '♈', 'Taurus': '♉',
      'Gemini': '♊', 'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
      'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐', 'Capricorn': '♑'
    };
    return zodiacEmojis[sign] || '⭐';
  }

  getBirthstoneEmoji(stone) {
    const stoneEmojis = {
      'Garnet': '🔴', 'Amethyst': '🟣', 'Aquamarine': '🔵', 'Diamond': '💎',
      'Emerald': '🟢', 'Pearl': '⚪', 'Ruby': '♦️', 'Peridot': '🟡',
      'Sapphire': '🔷', 'Opal': '🌈', 'Topaz': '🟠', 'Turquoise': '🩵'
    };
    return stoneEmojis[stone] || '💍';
  }

  getBackgroundGradient(days) {
    if (!this.config.show_background) return 'var(--card-background-color)';
    
    if (days === 0) return 'linear-gradient(135deg, #ff6b6b, #ee5a24)';
    if (days <= 7) return 'linear-gradient(135deg, #ffa726, #ff9800)';
    if (days <= 30) return 'linear-gradient(135deg, #42a5f5, #1976d2)';
    return 'linear-gradient(135deg, #66bb6a, #4caf50)';
  }

  render() {
    if (!this._hass) return;
    
    const entity = this._hass.states[this.config.entity];
    if (!entity) {
      this.shadowRoot.innerHTML = `
        <div style="padding: 20px; text-align: center; color: var(--error-color);">
          Entity "${this.config.entity}" not found
        </div>
      `;
      return;
    }

    const days = parseInt(entity.state);
    const attrs = entity.attributes;
    const background = this.getBackgroundGradient(days);
    const isToday = days === 0;
    const isMilestone = attrs.is_milestone;

    this.shadowRoot.innerHTML = `
      <style>
        .card {
          background: ${background};
          border-radius: var(--ha-card-border-radius);
          box-shadow: var(--ha-card-box-shadow);
          padding: 24px;
          margin: 4px;
          color: ${this.config.show_background ? 'white' : 'var(--primary-text-color)'};
          position: relative;
          overflow: hidden;
        }
        .card-header {
          text-align: center;
          margin-bottom: 20px;
        }
        .entity-name {
          font-size: 1.5em;
          font-weight: bold;
          margin-bottom: 8px;
        }
        .countdown-display {
          text-align: center;
          margin: 20px 0;
        }
        .days-number {
          font-size: 4em;
          font-weight: bold;
          line-height: 1;
          ${isToday ? 'animation: pulse 1s infinite;' : ''}
          ${isMilestone ? 'animation: sparkle 2s infinite;' : ''}
        }
        .days-label {
          font-size: 1.2em;
          opacity: 0.9;
        }
        .anniversary-date {
          text-align: center;
          font-size: 1.1em;
          margin: 16px 0;
          opacity: 0.9;
        }
        .attributes-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 12px;
          margin-top: 20px;
        }
        .attribute-item {
          background: rgba(255, 255, 255, 0.1);
          padding: 12px;
          border-radius: 8px;
          text-align: center;
          backdrop-filter: blur(5px);
        }
        .attribute-icon {
          font-size: 1.5em;
          margin-bottom: 4px;
        }
        .attribute-label {
          font-size: 0.8em;
          opacity: 0.8;
          text-transform: uppercase;
          letter-spacing: 1px;
        }
        .attribute-value {
          font-weight: bold;
          margin-top: 4px;
        }
        .celebration-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          pointer-events: none;
          background: radial-gradient(circle at 50% 50%, rgba(255, 215, 0, 0.3) 0%, transparent 70%);
          ${isToday && this.config.show_animation ? 'animation: celebrate 3s infinite;' : ''}
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        @keyframes sparkle {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.02); }
        }
        @keyframes celebrate {
          0%, 100% { opacity: 0; }
          50% { opacity: 1; }
        }
        .compact {
          padding: 16px;
        }
        .compact .days-number {
          font-size: 2.5em;
        }
        .compact .entity-name {
          font-size: 1.2em;
        }
      </style>
      
      <div class="card ${this.config.compact_mode ? 'compact' : ''}">
        ${isToday ? '<div class="celebration-overlay"></div>' : ''}
        
        <div class="card-header">
          <div class="entity-name">${attrs.friendly_name || entity.entity_id}</div>
        </div>
        
        <div class="countdown-display">
          <div class="days-number">${days}</div>
          <div class="days-label">${days === 1 ? 'Day' : 'Days'} ${isToday ? 'TODAY! 🎉' : ''}</div>
        </div>
        
        <div class="anniversary-date">
          📅 ${attrs.next_date}
          ${attrs.years_at_anniversary ? `<br>🎂 ${attrs.years_at_anniversary} years` : ''}
        </div>
        
        ${this.config.show_attributes ? this.renderAttributes(attrs) : ''}
      </div>
    `;
  }

  renderAttributes(attrs) {
    const attributeItems = [];
    
    if (attrs.zodiac_sign) {
      attributeItems.push({
        icon: this.getZodiacEmoji(attrs.zodiac_sign),
        label: 'Zodiac',
        value: attrs.zodiac_sign
      });
    }
    
    if (attrs.birthstone) {
      attributeItems.push({
        icon: this.getBirthstoneEmoji(attrs.birthstone),
        label: 'Birthstone',
        value: attrs.birthstone
      });
    }
    
    if (attrs.birth_flower) {
      attributeItems.push({
        icon: '🌸',
        label: 'Birth Flower',
        value: attrs.birth_flower
      });
    }
    
    if (attrs.generation) {
      attributeItems.push({
        icon: '👥',
        label: 'Generation',
        value: attrs.generation
      });
    }
    
    if (attrs.named_anniversary) {
      attributeItems.push({
        icon: '💫',
        label: 'Anniversary',
        value: attrs.named_anniversary
      });
    }
    
    if (attrs.current_years !== undefined) {
      attributeItems.push({
        icon: '📊',
        label: 'Current Age',
        value: `${attrs.current_years} years`
      });
    }
    
    if (attrs.weeks_remaining !== undefined) {
      attributeItems.push({
        icon: '📆',
        label: 'Weeks Left',
        value: attrs.weeks_remaining
      });
    }

    if (attributeItems.length === 0) return '';

    return `
      <div class="attributes-grid">
        ${attributeItems.map(item => `
          <div class="attribute-item">
            <div class="attribute-icon">${item.icon}</div>
            <div class="attribute-label">${item.label}</div>
            <div class="attribute-value">${item.value}</div>
          </div>
        `).join('')}
      </div>
    `;
  }

  getCardSize() {
    return this.config.compact_mode ? 2 : 4;
  }
}

customElements.define('anniversary-details-card', AnniversaryDetailsCard);

// Register the card
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'custom:anniversary-details-card',
  name: 'Anniversary Details Card',
  description: 'Detailed view of a single anniversary with rich attributes',
  preview: true
});

console.info(
  '%c  ANNIVERSARY-DETAILS-CARD  %c  Version 1.0.0  ',
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray'
);
