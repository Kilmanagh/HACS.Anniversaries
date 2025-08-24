console.error('🚨🚨🚨 STATS CARD JAVASCRIPT FILE LOADED! 🚨🚨🚨');

/**
 * Anniversary Stats Card
 * Summary statistics and quick overview of anniversaries
 */

class AnniversaryStatsCard extends HTMLElement {
  constructor() {
    super();
    console.error('🚨🚨🚨 STATS CARD CONSTRUCTOR CALLED! 🚨🚨🚨');
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    this.config = {
      title: config.title || 'Anniversary Statistics',
      show_next_3: config.show_next_3 !== false,
      show_stats: config.show_stats !== false,
      show_charts: config.show_charts !== false,
      entity_filter: config.entity_filter || 'sensor.anniversary_*',
      ...config
    };
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getAnniversaryEntities() {
    if (!this._hass) return [];
    
    return Object.keys(this._hass.states)
      .filter(entityId => {
        if (this.config.entities) {
          return this.config.entities.includes(entityId);
        }
        return entityId.match(/^sensor\.anniversary_.*/) && 
               !entityId.includes('upcoming_anniversaries');
      })
      .map(entityId => this._hass.states[entityId])
      .filter(entity => entity && entity.state !== 'unavailable')
      .sort((a, b) => parseInt(a.state) - parseInt(b.state));
  }

  calculateStats() {
    const entities = this.getAnniversaryEntities();
    
    const stats = {
      total: entities.length,
      today: entities.filter(e => parseInt(e.state) === 0).length,
      thisWeek: entities.filter(e => parseInt(e.state) <= 7).length,
      thisMonth: entities.filter(e => parseInt(e.state) <= 30).length,
      milestones: entities.filter(e => e.attributes.is_milestone).length,
    };
    
    // Zodiac signs distribution
    const zodiacSigns = {};
    entities.forEach(entity => {
      const sign = entity.attributes.zodiac_sign;
      if (sign) {
        zodiacSigns[sign] = (zodiacSigns[sign] || 0) + 1;
      }
    });
    
    // Generation distribution
    const generations = {};
    entities.forEach(entity => {
      const gen = entity.attributes.generation;
      if (gen) {
        generations[gen] = (generations[gen] || 0) + 1;
      }
    });
    
    // Birthstones this month
    const currentMonth = new Date().getMonth() + 1;
    const birthstones = {};
    entities.forEach(entity => {
      const stone = entity.attributes.birthstone;
      if (stone) {
        birthstones[stone] = (birthstones[stone] || 0) + 1;
      }
    });
    
    return {
      ...stats,
      zodiacSigns,
      generations,
      birthstones,
      next3: entities.slice(0, 3)
    };
  }

  getZodiacEmoji(sign) {
    const zodiacEmojis = {
      'Aquarius': '♒', 'Pisces': '♓', 'Aries': '♈', 'Taurus': '♉',
      'Gemini': '♊', 'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
      'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐', 'Capricorn': '♑'
    };
    return zodiacEmojis[sign] || '⭐';
  }

  render() {
    if (!this._hass) return;
    
    const stats = this.calculateStats();
    
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
          text-align: center;
        }
        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 12px;
          margin-bottom: 20px;
        }
        .stat-item {
          background: var(--secondary-background-color);
          padding: 16px;
          border-radius: 8px;
          text-align: center;
        }
        .stat-number {
          font-size: 2em;
          font-weight: bold;
          color: var(--primary-color);
          margin-bottom: 4px;
        }
        .stat-label {
          font-size: 0.9em;
          color: var(--secondary-text-color);
          text-transform: uppercase;
          letter-spacing: 1px;
        }
        .next-anniversaries {
          margin-bottom: 20px;
        }
        .section-title {
          font-size: 1.1em;
          font-weight: bold;
          margin-bottom: 12px;
          color: var(--primary-text-color);
        }
        .next-item {
          display: flex;
          align-items: center;
          padding: 8px 0;
          border-bottom: 1px solid var(--divider-color);
        }
        .next-item:last-child {
          border-bottom: none;
        }
        .next-days {
          background: var(--primary-color);
          color: white;
          padding: 4px 8px;
          border-radius: 16px;
          font-size: 0.8em;
          font-weight: bold;
          margin-right: 12px;
          min-width: 40px;
          text-align: center;
        }
        .next-name {
          flex: 1;
          color: var(--primary-text-color);
        }
        .next-date {
          color: var(--secondary-text-color);
          font-size: 0.9em;
        }
        .distribution-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 16px;
        }
        .distribution-section {
          background: var(--secondary-background-color);
          padding: 16px;
          border-radius: 8px;
        }
        .distribution-title {
          font-weight: bold;
          margin-bottom: 8px;
          color: var(--primary-text-color);
        }
        .distribution-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 4px 0;
        }
        .distribution-label {
          color: var(--primary-text-color);
        }
        .distribution-count {
          background: var(--primary-color);
          color: white;
          padding: 2px 6px;
          border-radius: 12px;
          font-size: 0.8em;
          font-weight: bold;
        }
        .progress-bar {
          width: 100%;
          height: 6px;
          background: var(--divider-color);
          border-radius: 3px;
          margin-top: 8px;
          overflow: hidden;
        }
        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, var(--success-color), var(--primary-color));
          transition: width 0.3s ease;
        }
        .no-data {
          text-align: center;
          color: var(--secondary-text-color);
          padding: 20px;
        }
      </style>
      
      <div class="card">
        <div class="card-header">${this.config.title}</div>
        
        ${stats.total === 0 ? 
          '<div class="no-data">No anniversaries configured</div>' :
          `
            ${this.config.show_stats ? this.renderStats(stats) : ''}
            ${this.config.show_next_3 ? this.renderNext3(stats) : ''}
            ${this.config.show_charts ? this.renderDistributions(stats) : ''}
          `
        }
      </div>
    `;
  }

  renderStats(stats) {
    return `
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-number">${stats.total}</div>
          <div class="stat-label">Total</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">${stats.today}</div>
          <div class="stat-label">Today</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">${stats.thisWeek}</div>
          <div class="stat-label">This Week</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">${stats.thisMonth}</div>
          <div class="stat-label">This Month</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">${stats.milestones}</div>
          <div class="stat-label">Milestones</div>
        </div>
      </div>
    `;
  }

  renderNext3(stats) {
    if (stats.next3.length === 0) return '';
    
    return `
      <div class="next-anniversaries">
        <div class="section-title">🔥 Next 3 Anniversaries</div>
        ${stats.next3.map(entity => {
          const days = parseInt(entity.state);
          return `
            <div class="next-item">
              <div class="next-days">${days}d</div>
              <div class="next-name">${entity.attributes.friendly_name}</div>
              <div class="next-date">${entity.attributes.next_date}</div>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  renderDistributions(stats) {
    return `
      <div class="distribution-grid">
        ${Object.keys(stats.zodiacSigns).length > 0 ? `
          <div class="distribution-section">
            <div class="distribution-title">⭐ Zodiac Signs</div>
            ${Object.entries(stats.zodiacSigns)
              .sort(([,a], [,b]) => b - a)
              .slice(0, 5)
              .map(([sign, count]) => `
                <div class="distribution-item">
                  <span class="distribution-label">${this.getZodiacEmoji(sign)} ${sign}</span>
                  <span class="distribution-count">${count}</span>
                </div>
              `).join('')}
          </div>
        ` : ''}
        
        ${Object.keys(stats.generations).length > 0 ? `
          <div class="distribution-section">
            <div class="distribution-title">👥 Generations</div>
            ${Object.entries(stats.generations)
              .sort(([,a], [,b]) => b - a)
              .map(([gen, count]) => `
                <div class="distribution-item">
                  <span class="distribution-label">${gen}</span>
                  <span class="distribution-count">${count}</span>
                </div>
              `).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }

  getCardSize() {
    return 4;
  }

  // Required method for Home Assistant card validation
  static getStubConfig() {
    return {
      type: 'custom:anniversary-stats-card',
      title: 'Anniversary Statistics'
    };
  }
}

customElements.define('anniversary-stats-card', AnniversaryStatsCard);

// Register the card
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'custom:anniversary-stats-card',
  name: 'Anniversary Stats Card',
  description: 'Summary statistics and overview of all anniversaries',
  preview: true
});

console.info(
  '%c  ANNIVERSARY-STATS-CARD  %c  Version 1.0.0  ',
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray'
);
