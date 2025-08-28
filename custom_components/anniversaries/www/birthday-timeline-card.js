/**
 * Birthday Timeline Card v1.0.0
 * Shows upcoming birthdays only in chronological order
 */

class BirthdayTimelineCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._renderTimeout = null;
  }

  setConfig(config) {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    
    console.log('🎂 [Birthday Card] setConfig called with:', config);
    console.log('🎂 [Birthday Card] Raw config.date_format:', config.date_format);
    
    this.config = {
      title: config.title || '🎂 Upcoming Birthdays',
      max_items: config.max_items || 5,
      date_format: config.date_format || 'long', // Default to long format
      show_day_of_week: config.show_day_of_week !== false,
      show_icons: config.show_icons !== false,
      color_coding: config.color_coding !== false,
      debug: config.debug || false
    };
    
    console.log('🎂 [Birthday Card] Final config:', this.config);
    
    if (this._hass) {
      this.scheduleRender();
    }
  }

  scheduleRender() {
    if (this._renderTimeout) {
      clearTimeout(this._renderTimeout);
    }
    this._renderTimeout = setTimeout(() => {
      this.render();
      this._renderTimeout = null;
    }, 0);
  }

  set hass(hass) {
    this._hass = hass;
    if (this.config) {
      this.scheduleRender();
    }
  }

  getBirthdayEntities() {
    if (!this._hass || !this.config) return [];
    
    console.log('🎂 [Birthday Card] Getting birthday entities');
    
    const entities = Object.keys(this._hass.states)
      .filter(entityId => {
        const entity = this._hass.states[entityId];
        if (!entity) return false;
        
        // Must be a sensor
        if (!entityId.startsWith('sensor.')) return false;
        
        // Skip aggregation sensors
        if (entityId.includes('upcoming_anniversaries')) return false;
        
        // Check if it's a birthday entity
        return this.isBirthdayEntity(entity);
      })
      .map(entityId => this._hass.states[entityId])
      .filter(entity => {
        if (!entity || entity.state === 'unavailable') return false;
        
        // Must have birthday category
        const entityCategory = entity.attributes.category || 'other';
        const isBirthday = entityCategory === 'birthday';
        
        if (this.config.debug) {
          console.log(`🎂 [Birthday Card] Entity ${entity.entity_id}: category="${entityCategory}", isBirthday=${isBirthday}`);
        }
        
        return isBirthday;
      })
      .sort((a, b) => {
        // Sort by days until birthday
        return parseInt(a.state) - parseInt(b.state);
      })
      .slice(0, this.config.max_items);
    
    console.log(`🎂 [Birthday Card] Found ${entities.length} birthday entities`);
    return entities;
  }

  isBirthdayEntity(entity) {
    if (!entity || !entity.attributes) return false;
    
    const attrs = entity.attributes;
    
    // Anniversary entities have these specific attributes
    const hasAnniversaryAttributes = (
      attrs.next_date !== undefined &&
      attrs.current_years !== undefined &&
      attrs.category !== undefined &&
      (attrs.zodiac_sign !== undefined ||
       attrs.birthstone !== undefined ||
       attrs.birth_flower !== undefined)
    );
    
    // Must have valid state (days until)
    const hasValidState = (
      entity.state !== 'unavailable' &&
      !isNaN(parseInt(entity.state)) &&
      parseInt(entity.state) >= 0
    );
    
    return hasAnniversaryAttributes && hasValidState;
  }

  formatDate(dateString) {
    if (!dateString) return '';
    
    if (!this.config) {
      console.warn('Birthday Card: formatDate called before config is set');
      return dateString;
    }
    
    console.log(`🎂 [Birthday Card] formatDate called with: "${dateString}", format: "${this.config.date_format}"`);
    
    try {
      const [year, month, day] = dateString.split('-');
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
      
      const locale = navigator.language || 'en-US';
      
      let formattedDate;
      
      switch (this.config.date_format) {
        case 'short':
          formattedDate = date.toLocaleDateString(locale, {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
          });
          break;
          
        case 'numeric':
          formattedDate = date.toLocaleDateString(locale, {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric'
          });
          break;
          
        case 'full':
          formattedDate = date.toLocaleDateString(locale, {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
          });
          break;
          
        case 'long':
        default:
          formattedDate = date.toLocaleDateString(locale, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          });
          break;
      }
      
      // Add day of week if requested and not already included
      if (this.config.show_day_of_week && this.config.date_format !== 'full') {
        const dayOfWeek = date.toLocaleDateString(locale, { weekday: 'long' });
        formattedDate = `${dayOfWeek}, ${formattedDate}`;
      }
      
      console.log(`🎂 [Birthday Card] Final formatted date: "${formattedDate}"`);
      return formattedDate;
      
    } catch (error) {
      console.warn('Birthday Card: Date formatting error:', error);
      return dateString;
    }
  }

  getColorForDays(days) {
    if (!this.config.color_coding) return '#FF9800';
    
    // Universal time-based color scheme: Red (urgent) → Orange (soon) → Green (safe) → Blue (distant)
    if (days === 0) return '#F44336';      // Red - today (urgent!)
    if (days <= 7) return '#FF9800';       // Orange - this week (attention needed)
    if (days <= 30) return '#4CAF50';      // Green - this month (comfortable distance)
    return '#2196F3';                      // Blue - future (distant, calm)
  }

  render() {
    if (!this.config || !this._hass) return;
    
    const entities = this.getBirthdayEntities();
    
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
        .no-birthdays {
          text-align: center;
          color: var(--secondary-text-color);
          padding: 20px;
        }
        .debug-info {
          background: #fff3cd;
          border: 1px solid #ffeaa7;
          border-radius: 4px;
          padding: 8px;
          margin: 8px 0;
          font-size: 12px;
        }
      </style>
      
      <div class="card">
        <div class="card-header">${this.config.title}</div>
        ${this.config.debug ? this.renderDebugInfo(entities) : ''}
        ${entities.length === 0 ? 
          '<div class="no-birthdays">No upcoming birthdays found</div>' :
          entities.map(entity => this.renderTimelineItem(entity)).join('')
        }
      </div>
    `;
  }

  renderDebugInfo(entities) {
    const allEntities = Object.keys(this._hass.states)
      .filter(entityId => entityId.startsWith('sensor.') && !entityId.includes('upcoming_anniversaries'))
      .map(entityId => this._hass.states[entityId])
      .filter(entity => entity && entity.state !== 'unavailable' && this.isBirthdayEntity(entity));
    
    const allCategories = allEntities.map(e => e.attributes.category || 'other');
    
    return `
      <div class="debug-info">
        <strong>🎂 Birthday Card Debug:</strong><br>
        <strong>Date Format:</strong> ${this.config.date_format}<br>
        <strong>Show Day of Week:</strong> ${this.config.show_day_of_week}<br>
        <strong>All Birthday Entities Found:</strong> ${allEntities.length}<br>
        <strong>Categories:</strong> ${[...new Set(allCategories)].join(', ')}<br>
        <strong>Displayed:</strong> ${entities.length}<br>
        <strong>Entity Details:</strong><br>
        ${allEntities.slice(0, 5).map(e => `&nbsp;&nbsp;• ${e.entity_id}: category="${e.attributes.category || 'other'}", days=${e.state}`).join('<br>')}
        ${allEntities.length > 5 ? `<br>&nbsp;&nbsp;... and ${allEntities.length - 5} more` : ''}
      </div>
    `;
  }

  renderTimelineItem(entity) {
    const days = parseInt(entity.state);
    const attrs = entity.attributes;
    const icon = this.config.show_icons ? (entity.attributes.custom_emoji || '🎂') : '';
    const color = this.getColorForDays(days);
    
    return `
      <div class="timeline-item">
        ${icon ? `<div class="timeline-icon">${icon}</div>` : ''}
        <div class="timeline-content">
          <div class="timeline-name">
            ${attrs.friendly_name || attrs.name || entity.entity_id}
          </div>
          <div class="timeline-date">
            ${this.formatDate(attrs.next_date)}
            ${attrs.current_age ? ` (turning ${attrs.current_age + 1})` : ''}
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
    const attributes = [];
    
    if (attrs.zodiac_sign) {
      const zodiacEmojis = {
        'Aquarius': '♒', 'Pisces': '♓', 'Aries': '♈', 'Taurus': '♉',
        'Gemini': '♊', 'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
        'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐', 'Capricorn': '♑'
      };
      const emoji = zodiacEmojis[attrs.zodiac_sign] || '⭐';
      attributes.push(`<span class="attribute-badge">${emoji} ${attrs.zodiac_sign}</span>`);
    }
    
    if (attrs.birthstone) {
      const stoneEmojis = {
        'Garnet': '🔴', 'Amethyst': '🟣', 'Aquamarine': '🔵', 'Diamond': '💎',
        'Emerald': '🟢', 'Pearl': '⚪', 'Ruby': '♦️', 'Peridot': '🟡',
        'Sapphire': '🔷', 'Opal': '🌈', 'Topaz': '🟠', 'Turquoise': '🩵'
      };
      const emoji = stoneEmojis[attrs.birthstone] || '💎';
      attributes.push(`<span class="attribute-badge">${emoji} ${attrs.birthstone}</span>`);
    }
    
    if (attrs.generation) {
      attributes.push(`<span class="attribute-badge">👥 ${attrs.generation}</span>`);
    }
    
    return attributes.join('');
  }

  getCardSize() {
    return 3;
  }

  static getStubConfig() {
    return {
      type: 'custom:birthday-timeline-card',
      title: '🎂 Upcoming Birthdays',
      date_format: 'long',
      max_items: 5
    };
  }
}

// Register the card
customElements.define('birthday-timeline-card', BirthdayTimelineCard);

// Register with Home Assistant
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'birthday-timeline-card',
  name: 'Birthday Timeline Card',
  description: 'Display upcoming birthdays in chronological order with long date format by default',
  preview: true
});

console.info(
  '%c  BIRTHDAY-TIMELINE-CARD  %c  Version 1.0.0 - Birthday-Only Timeline  ',
  'color: #FF69B4; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: #FF1493'
);
