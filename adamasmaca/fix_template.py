
import os

file_path = r"c:\Users\fatih\OneDrive\Masaüstü\adamasmaca\game\templates\game\board.html"

new_content = """{% extends 'game/base.html' %}

{% block content %}
<div class="game-card">
    <div class="game-header">
        <span class="category-badge">{{ category }}</span>
        <span class="lives-counter">❤️ {{ lives }}</span>
    </div>

    <!-- Hangman Visual Area -->
    <div class="hangman-container">
        <svg viewBox="0 0 100 100" class="hangman-svg">
            <!-- Stand -->
            <line x1="10" y1="90" x2="90" y2="90" class="draw" />
            <line x1="30" y1="90" x2="30" y2="10" class="draw" />
            <line x1="30" y1="10" x2="70" y2="10" class="draw" />
            <line x1="70" y1="10" x2="70" y2="20" class="draw" />
            
            <!-- Body Parts (Conditional) -->
            {% if lives <= 5 %}<circle cx="70" cy="30" r="10" class="draw" />{% endif %}
            {% if lives <= 4 %}<line x1="70" y1="40" x2="70" y2="70" class="draw" />{% endif %}
            {% if lives <= 3 %}<line x1="70" y1="50" x2="50" y2="40" class="draw" />{% endif %}
            {% if lives <= 2 %}<line x1="70" y1="50" x2="90" y2="40" class="draw" />{% endif %}
            {% if lives <= 1 %}<line x1="70" y1="70" x2="50" y2="85" class="draw" />{% endif %}
            {% if lives <= 0 %}<line x1="70" y1="70" x2="90" y2="85" class="draw" />{% endif %}
        </svg>
    </div>

    <!-- Word Display Area -->
    <div class="word-display">
        {% for letter in display_word %}
            <span class="letter-slot {% if letter == '_' %}empty{% endif %}">{{ letter }}</span>
        {% endfor %}
    </div>

    <!-- Interface (Keyboard or Game Over) -->
    <div class="interaction-area">
        {% if game_status == 'playing' %}
            <div class="keyboard">
                {% for key in keyboard %}
                <form action="{% url 'make_guess' %}" method="post" style="display: inline;">
                    {% csrf_token %}
                    <input type="hidden" name="letter" value="{{ key.char }}">
                    <button type="submit" class="key-button {{ key.state }}" {% if key.state != 'default' %}disabled{% endif %}>{{ key.char }}</button>
                </form>
                {% endfor %}
            </div>
        {% else %}
            <div class="result-overlay {{ game_status }}">
                <h2>{% if game_status == 'won' %}Tebrikler! 🎉{% else %}Maalesef Kaybettin... 💀{% endif %}</h2>
                {% if target_word_revealed %}
                    <p>Kelime: <strong>{{ target_word_revealed }}</strong></p>
                {% endif %}
                <a href="{% url 'index' %}" class="primary-button">YENİDEN OYNA</a>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("File successfully fixed.")
