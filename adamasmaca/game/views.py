from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from . import logic

def index(request):
    categories = logic.get_categories()
    return render(request, 'game/index.html', {'categories': categories})

@require_POST
def start_game(request):
    category = request.POST.get('category')
    logic.init_game(request, category)
    return redirect('game_board')

def game_board(request):
    if 'target_word' not in request.session:
        return redirect('index')
        
    target_word = request.session['target_word']
    guessed_letters = request.session.get('guessed_letters', [])
    lives = request.session.get('lives', 6)
    game_status = request.session.get('game_status', 'playing')
    
    # Process word for display
    display_word = []
    for char in target_word:
        if char in guessed_letters or char == ' ':
            display_word.append(char)
        else:
            display_word.append('_')
            
    # Keyboard setup
    alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    keyboard = []
    for char in alphabet:
        state = 'default'
        if char in guessed_letters:
            if char in target_word:
                state = 'correct'
            else:
                state = 'wrong'
        keyboard.append({'char': char, 'state': state})

    context = {
        'display_word': display_word,
        'lives': lives,
        'keyboard': keyboard,
        'game_status': game_status,
        'category': request.session.get('category'),
        'target_word_revealed': target_word if game_status != 'playing' else None
    }
    return render(request, 'game/board.html', context)

@require_POST
def make_guess(request):
    letter = request.POST.get('letter')
    if letter:
        logic.process_guess(request, letter)
    return redirect('game_board')
