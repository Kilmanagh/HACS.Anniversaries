/**
 * Anniversary Timeline Card
 * Shows upcoming anniversaries in chronological order with all attributes
 */

class AnniversaryTimelineCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this.config = {
      title: config.title || 'Upcoming Anniversaries',
      max_items: config.max_items || 5,
      show_attributes: config.show_attributes || ['zodiac_sign', 'birthstone', 'generation'],
      entity_filter: config.entity_filter || 'sensor.anniversary_*',
      show_icons: config.show_icons !== false,
      color_coding: config.color_coding !== false,
      ...config
    };
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getAnniversaryEntities() {
    if (!this._hass) return [];
    
    const entities = Object.keys(this._hass.states)
      .filter(entityId => {
        if (this.config.entities) {
          return this.config.entities.includes(entityId);
        }
        return entityId.match(/^sensor\.anniversary_.*/) && 
               !entityId.includes('upcoming_anniversaries');
      })
      .map(entityId => this._hass.states[entityId])
      .filter(entity => entity && entity.state !== 'unavailable')
      .sort((a, b) => parseInt(a.state) - parseInt(b.state))
      .slice(0, this.config.max_items);
    
    return entities;
  }

  getIcon(entity) {
    const days = parseInt(entity.state);
    const name = entity.attributes.friendly_name || entity.entity_id;
    
    // Custom icons based on name/type
    if (name.toLowerCase().includes('birthday') || name.toLowerCase().includes('birth')) return '🎂';
    if (name.toLowerCase().includes('wedding') || name.toLowerCase().includes('anniversary')) return '💍';
    if (name.toLowerCase().includes('graduation')) return '🎓';
    if (name.toLowerCase().includes('work') || name.toLowerCase().includes('job')) return '💼';
    
    // Days-based icons
    if (days === 0) return '🌟';
    if (days <= 7) return '🔥';
    if (days <= 30) return '⏰';
    
    // Milestone icons
    if (entity.attributes.is_milestone) return '💎';
    
    return '📅';
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

  getColorForDays(days) {
    if (!this.config.color_coding) return '#1976d2';
    if (days === 0) return '#f44336';      // Red - today
    if (days <= 7) return '#ff9800';       // Orange - this week  
    if (days <= 30) return '#ffc107';      // Yellow - this month
    return '#4caf50';                      // Green - future
  }

  render() {
    const entities = this.getAnniversaryEntities();
    
    this.shadowRoot.innerHTML = `
      <style>
        .card {
          background: var(--card-background-color);
          border-radius: var(--ha-card-border-radius);
          box-shadow: var(--ha-card-box-shadow);
          padding: 16px;
          margin: 4px;
        }
        .card-header {
          font-size: 1.2em;
          font-weight: bold;
          margin-bottom: 16px;
          color: var(--primary-text-color);
        }
        .timeline-item {
          display: flex;
          align-items: center;
          padding: 12px 0;
          border-bottom: 1px solid var(--divider-color);
        }
        .timeline-item:last-child {
          border-bottom: none;
        }
        .timeline-icon {
          font-size: 24px;
          margin-right: 12px;
          min-width: 32px;
        }
        .timeline-content {
          flex: 1;
        }
        .timeline-name {
          font-weight: bold;
          color: var(--primary-text-color);
          margin-bottom: 4px;
        }
        .timeline-date {
          font-size: 0.9em;
          color: var(--secondary-text-color);
          margin-bottom: 4px;
        }
        .timeline-attributes {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
        .attribute-badge {
          background: var(--secondary-background-color);
          padding: 2px 6px;
          border-radius: 12px;
          font-size: 0.8em;
          color: var(--primary-text-color);
        }
        .days-counter {
          text-align: center;
          min-width: 60px;
          font-weight: bold;
          font-size: 1.1em;
          padding: 8px;
          border-radius: 8px;
          color: white;
        }
        .milestone-indicator {
          animation: sparkle 2s infinite;
        }
        @keyframes sparkle {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
        .no-anniversaries {
          text-align: center;
          color: var(--secondary-text-color);
          padding: 20px;
        }
      </style>
      
      <div class="card">
        <div class="card-header">${this.config.title}</div>
        ${entities.length === 0 ? 
          '<div class="no-anniversaries">No upcoming anniversaries</div>' :
          entities.map(entity => this.renderTimelineItem(entity)).join('')
        }
      </div>
    `;
  }

  renderTimelineItem(entity) {
    const days = parseInt(entity.state);
    const attrs = entity.attributes;
    const icon = this.config.show_icons ? this.getIcon(entity) : '📅';
    const color = this.getColorForDays(days);
    const isMilestone = attrs.is_milestone;
    
    return `
      <div class="timeline-item">
        <div class="timeline-icon ${isMilestone ? 'milestone-indicator' : ''}">${icon}</div>
        <div class="timeline-content">
          <div class="timeline-name">${attrs.friendly_name || entity.entity_id}</div>
          <div class="timeline-date">
            ${attrs.next_date} 
            ${attrs.years_at_anniversary ? `(${attrs.years_at_anniversary} years)` : ''}
          </div>
          <div class="timeline-attributes">
            ${this.renderAttributes(attrs)}
          </div>
        </div>
        <div class="days-counter" style="background-color: ${color}">
          ${days} day${days !== 1 ? 's' : ''}
        </div>
      </div>
    `;
  }

  renderAttributes(attrs) {
    return this.config.show_attributes.map(attr => {
      const value = attrs[attr];
      if (!value) return '';
      
      let emoji = '';
      let display = value;
      
      switch(attr) {
        case 'zodiac_sign':
          emoji = this.getZodiacEmoji(value);
          display = `${emoji} ${value}`;
          break;
        case 'birthstone':
          emoji = this.getBirthstoneEmoji(value);
          display = `${emoji} ${value}`;
          break;
        case 'birth_flower':
          display = `🌸 ${value}`;
          break;
        case 'generation':
          display = `👥 ${value}`;
          break;
        case 'named_anniversary':
          display = `💫 ${value}`;
          break;
        default:
          display = value;
      }
      
      return `<span class="attribute-badge">${display}</span>`;
    }).join('');
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('anniversary-timeline-card', AnniversaryTimelineCard);

// Register the card
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'anniversary-timeline-card',
  name: 'Anniversary Timeline Card',
  description: 'Shows upcoming anniversaries in chronological order',
  preview: true
});

console.info(
  '%c  ANNIVERSARY-TIMELINE-CARD  %c  Version 1.0.0  ',
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray'
);
