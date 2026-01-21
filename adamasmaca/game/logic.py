import random
from .models import Word

def get_categories():
    return Word.objects.values_list('category', flat=True).distinct()

def get_random_word(category):
    words = Word.objects.filter(category=category)
    if not words.exists():
        words = Word.objects.all()
    
    if not words.exists():
        return None
        
    return random.choice(list(words))

def init_game(request, category):
    word_obj = get_random_word(category)
    # Default to ANKARA if DB empty
    target_word = word_obj.text if word_obj else "ANKARA"
    
    request.session['target_word'] = target_word
    request.session['category'] = category
    request.session['guessed_letters'] = []
    request.session['lives'] = 6
    request.session['game_status'] = 'playing'
    request.session.modified = True

def process_guess(request, letter):
    if request.session.get('game_status') != 'playing':
        return

    # Letter normalizing
    # We assume letter comes in correct form, but just in case
    letter = letter.upper() 
    if letter == 'i': letter = 'İ'
    if letter == 'ı': letter = 'I'
    
    target_word = request.session.get('target_word', '')
    guessed = request.session.get('guessed_letters', [])
    lives = request.session.get('lives', 6)
    
    if letter not in guessed:
        guessed.append(letter)
        request.session['guessed_letters'] = guessed
        
        if letter not in target_word:
            lives -= 1
            request.session['lives'] = lives
            
    # Check Win/Loss
    if lives <= 0:
        request.session['game_status'] = 'lost'
    else:
        # Check if all letters in target are in guessed
        # Filter out spaces or special chars if any (though we sanitize them)
        remaining = [l for l in target_word if l not in guessed and l.strip()]
        if not remaining:
            request.session['game_status'] = 'won'
    
    request.session.modified = True
