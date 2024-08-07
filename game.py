import pygame
import sys
from button import Button
from gesture_recognition import GestureRecognition

pygame.init()

# Setup screen
screen = pygame.display.set_mode((1024, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Quiz Game')

# Font
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Background image
image_bg_global = pygame.image.load('bg.jpg').convert()
image_rect_global = image_bg_global.get_rect(topleft=(0, 0))
image_gameover = pygame.image.load('pics/gameover.jpg').convert()
image_rect_gameover = image_gameover.get_rect(topleft=(0, 0))
image_hearts3 = pygame.image.load('buttons/hearts3.png').convert_alpha()
image_rect_hearts3 = image_hearts3.get_rect(topleft=(10, 10))
image_hearts2 = pygame.image.load('buttons/hearts2.png').convert_alpha()
image_rect_hearts2 = image_hearts2.get_rect(topleft=(10, 10))
image_hearts1 = pygame.image.load('buttons/hearts1.png').convert_alpha()
image_rect_hearts1 = image_hearts1.get_rect(topleft=(10, 10))

# Image for quiz introductions
image_earthquake_introduction = pygame.image.load('pics/earth_intro.jpg').convert()
image_earth_rect = image_earthquake_introduction.get_rect(topleft=(0, 0))
image_flood_introduction = pygame.image.load('pics/flood_intro.jpg').convert()
image_flood_rect = image_flood_introduction.get_rect(topleft=(0, 0))
image_fire_introduction = pygame.image.load('pics/fire_intro.jpg').convert()
image_fire_rect = image_fire_introduction.get_rect(topleft=(0, 0))

#Image for quiz ending
image_earth_end = pygame.image.load('pics/earth_end.jpg').convert()
image_earthend_rect = image_earth_end.get_rect(topleft=(0,0))
image_flood_end = pygame.image.load('pics/flood_end.jpg').convert()
image_floodend_rect = image_flood_end.get_rect(topleft=(0,0))
image_fire_end = pygame.image.load('pics/fire_end.jpg').convert()
image_fireend_rect = image_fire_end.get_rect(topleft=(0,0))

# Load question images, correct answers, and wrong answers for Earthquake quiz
question_images = {}
correct_images = {}
wrong_images1 = {}
wrong_images2 = {}

# Define the images for questions
list_questions = ['earth_q1', 'earth_q2', 'earth_q3', 'earth_q4', 'earth_q5',
                  'flood_q1', 'flood_q2', 'flood_q3', 'flood_q4', 'flood_q5',
                  'fire_q1', 'fire_q2', 'fire_q3', 'fire_q4', 'fire_q5']
for i, q in enumerate(list_questions):
    question_images[f'q{i + 1}'] = pygame.image.load(f'pics/{q}.jpg').convert()
    question_images[f'q{i + 1}_rect'] = question_images[f'q{i + 1}'].get_rect(topleft=(0, 0))

# Define the images for correct answers
correct_answers = ['earth_q1_c1', 'earth_q2_c1', 'earth_q3_c1', 'earth_q4_c1', 'earth_q5_c1',
                   'flood_q1_c1', 'flood_q2_c1', 'flood_q3_c1', 'flood_q4_c1', 'flood_q5_c1',
                   'fire_q1_c1', 'fire_q2_c1', 'fire_q3_c1', 'fire_q4_c1', 'fire_q5_c1']
for i, ca in enumerate(correct_answers):
    correct_images[f'q{i + 1}_c1'] = pygame.image.load(f'pics/{ca}.jpg').convert()
    correct_images[f'q{i + 1}_c1_rect'] = correct_images[f'q{i + 1}_c1'].get_rect(topleft=(0, 0))

# Define the images for wrong answers
wrong_answers1 = ['earth_q1_w1', 'earth_q2_w1', 'earth_q3_w1', 'earth_q4_w1', 'earth_q5_w1',
                  'flood_q1_w1', 'flood_q2_w1', 'flood_q3_w1', 'flood_q4_w1', 'flood_q5_w1',
                  'fire_q1_w1', 'fire_q2_w1', 'fire_q3_w1', 'fire_q4_w1', 'fire_q5_w1']
for i, wa in enumerate(wrong_answers1):
    wrong_images1[f'q{i + 1}_w1'] = pygame.image.load(f'pics/{wa}.jpg').convert()
    wrong_images1[f'q{i + 1}_w1_rect'] = wrong_images1[f'q{i + 1}_w1'].get_rect(topleft=(0, 0))

wrong_answers2 = ['earth_q1_w2', 'earth_q2_w2', 'earth_q3_w2', 'earth_q4_w2', 'earth_q5_w2',
                  'flood_q1_w2', 'flood_q2_w2', 'flood_q3_w2', 'flood_q4_w2', 'flood_q5_w2',
                  'fire_q1_w2', 'fire_q1_w2', 'fire_q3_w2', 'fire_q4_w2', 'fire_q5_w2']
for i, wa in enumerate(wrong_answers2):
    wrong_images2[f'q{i + 1}_w2'] = pygame.image.load(f'pics/{wa}.jpg').convert()
    wrong_images2[f'q{i + 1}_w2_rect'] = wrong_images2[f'q{i + 1}_w2'].get_rect(topleft=(0, 0))    

# Load button images
start_img = pygame.image.load('buttons/but_play.png').convert_alpha()
exit_img = pygame.image.load('buttons/but_exit.png').convert_alpha()
back_img = pygame.image.load('buttons/but_back.png').convert_alpha()
settings_img = pygame.image.load('buttons/but_settings.png').convert_alpha()
next_img = pygame.image.load('buttons/but_next.png').convert_alpha()
retry_img = pygame.image.load('buttons/but_retry.png').convert_alpha()
earthquake_img = pygame.image.load('buttons/but_earthquake.png').convert_alpha()
flood_img = pygame.image.load('buttons/but_flood.png').convert_alpha()
fire_img = pygame.image.load('buttons/but_fire.png').convert_alpha()
cam_img = pygame.image.load('buttons/but_cam.png').convert_alpha()

# Functional Buttons
start_button = Button(50, 100, start_img, 1)
settings_button = Button(50, 200, settings_img, 1)
exit_button = Button(50, 300, exit_img, 1)
back_button = Button(50, 400, back_img, 1)
next_button = Button(820, 470, next_img, 1)
retry_button = Button(820, 470, retry_img, 1)
earthquake_button = Button(50, 100, earthquake_img, 1)
flood_button = Button(50, 200, flood_img, 1)
fire_button = Button(50, 300, fire_img, 1)
cam_button = Button(900, 500, cam_img, 0.7)

#sound fx
correct_sfx = pygame.mixer.Sound("sounds/correct.mp3")
wrong_sfx = pygame.mixer.Sound("sounds/wrong.mp3")
gameover_sfx = pygame.mixer.Sound("sounds/gameover.mp3")

# Quiz data
quizzes = {
    'earthquake': {
        'introduction': image_earthquake_introduction,
        'ending' : image_earth_end,
        'questions': [
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 2,
                'images': {
                    'question': question_images['q1'],
                    'question_rect': question_images['q1_rect'],
                    'correct': correct_images['q1_c1'],
                    'correct_rect': correct_images['q1_c1_rect'],
                    'wrong1': wrong_images1['q1_w1'],
                    'wrong1_rect': wrong_images1['q1_w1_rect'],
                    'wrong2': wrong_images2['q1_w2'],
                    'wrong2_rect': wrong_images2['q1_w2_rect'],
                }
            },
            {
                'choices': ['Yolo', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q2'],
                    'question_rect': question_images['q2_rect'],
                    'correct': correct_images['q2_c1'],
                    'correct_rect': correct_images['q2_c1_rect'],
                    'wrong1': wrong_images1['q2_w1'],
                    'wrong1_rect': wrong_images1['q2_w1_rect'],
                    'wrong2': wrong_images2['q2_w2'],
                    'wrong2_rect': wrong_images2['q2_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q3'],
                    'question_rect': question_images['q3_rect'],
                    'correct': correct_images['q3_c1'],
                    'correct_rect': correct_images['q3_c1_rect'],
                    'wrong1': wrong_images1['q3_w1'],
                    'wrong1_rect': wrong_images1['q3_w1_rect'],
                    'wrong2': wrong_images2['q3_w2'],
                    'wrong2_rect': wrong_images2['q3_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q4'],
                    'question_rect': question_images['q4_rect'],
                    'correct': correct_images['q4_c1'],
                    'correct_rect': correct_images['q4_c1_rect'],
                    'wrong1': wrong_images1['q4_w1'],
                    'wrong1_rect': wrong_images1['q4_w1_rect'],
                    'wrong2': wrong_images2['q4_w2'],
                    'wrong2_rect': wrong_images2['q4_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q5'],
                    'question_rect': question_images['q5_rect'],
                    'correct': correct_images['q5_c1'],
                    'correct_rect': correct_images['q5_c1_rect'],
                    'wrong1': wrong_images1['q5_w1'],
                    'wrong1_rect': wrong_images1['q5_w1_rect'],
                    'wrong2': wrong_images2['q5_w2'],
                    'wrong2_rect': wrong_images2['q5_w2_rect'],
                }
            },
            # Add more questions here
        ]
    },
    'flood': {
        'introduction': image_flood_introduction,
        'ending' : image_flood_end,
        'questions': [
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q6'],
                    'question_rect': question_images['q6_rect'],
                    'correct': correct_images['q6_c1'],
                    'correct_rect': correct_images['q6_c1_rect'],
                    'wrong1': wrong_images1['q6_w1'],
                    'wrong1_rect': wrong_images1['q6_w1_rect'],
                    'wrong2': wrong_images2['q6_w2'],
                    'wrong2_rect': wrong_images2['q6_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q7'],
                    'question_rect': question_images['q7_rect'],
                    'correct': correct_images['q7_c1'],
                    'correct_rect': correct_images['q7_c1_rect'],
                    'wrong1': wrong_images1['q7_w1'],
                    'wrong1_rect': wrong_images1['q7_w1_rect'],
                    'wrong2': wrong_images2['q7_w2'],
                    'wrong2_rect': wrong_images2['q7_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q8'],
                    'question_rect': question_images['q8_rect'],
                    'correct': correct_images['q8_c1'],
                    'correct_rect': correct_images['q8_c1_rect'],
                    'wrong1': wrong_images1['q8_w1'],
                    'wrong1_rect': wrong_images1['q8_w1_rect'],
                    'wrong2': wrong_images2['q8_w2'],
                    'wrong2_rect': wrong_images2['q8_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q9'],
                    'question_rect': question_images['q9_rect'],
                    'correct': correct_images['q9_c1'],
                    'correct_rect': correct_images['q9_c1_rect'],
                    'wrong1': wrong_images1['q9_w1'],
                    'wrong1_rect': wrong_images1['q9_w1_rect'],
                    'wrong2': wrong_images2['q9_w2'],
                    'wrong2_rect': wrong_images2['q9_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q10'],
                    'question_rect': question_images['q10_rect'],
                    'correct': correct_images['q10_c1'],
                    'correct_rect': correct_images['q10_c1_rect'],
                    'wrong1': wrong_images1['q10_w1'],
                    'wrong1_rect': wrong_images1['q10_w1_rect'],
                    'wrong2': wrong_images2['q10_w2'],
                    'wrong2_rect': wrong_images2['q10_w2_rect'],
                }
            },
            # Add more questions here
        ]
    },
    'fire': {
        'introduction': image_fire_introduction,
        'ending' : image_fire_end,
        'questions': [
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q11'],
                    'question_rect': question_images['q11_rect'],
                    'correct': correct_images['q11_c1'],
                    'correct_rect': correct_images['q11_c1_rect'],
                    'wrong1': wrong_images1['q11_w1'],
                    'wrong1_rect': wrong_images1['q11_w1_rect'],
                    'wrong2': wrong_images2['q11_w2'],
                    'wrong2_rect': wrong_images2['q11_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q12'],
                    'question_rect': question_images['q12_rect'],
                    'correct': correct_images['q12_c1'],
                    'correct_rect': correct_images['q12_c1_rect'],
                    'wrong1': wrong_images1['q12_w1'],
                    'wrong1_rect': wrong_images1['q12_w1_rect'],
                    'wrong2': wrong_images2['q12_w2'],
                    'wrong2_rect': wrong_images2['q12_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q13'],
                    'question_rect': question_images['q13_rect'],
                    'correct': correct_images['q13_c1'],
                    'correct_rect': correct_images['q13_c1_rect'],
                    'wrong1': wrong_images1['q13_w1'],
                    'wrong1_rect': wrong_images1['q13_w1_rect'],
                    'wrong2': wrong_images2['q13_w2'],
                    'wrong2_rect': wrong_images2['q13_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q14'],
                    'question_rect': question_images['q14_rect'],
                    'correct': correct_images['q14_c1'],
                    'correct_rect': correct_images['q14_c1_rect'],
                    'wrong1': wrong_images1['q14_w1'],
                    'wrong1_rect': wrong_images1['q14_w1_rect'],
                    'wrong2': wrong_images2['q14_w2'],
                    'wrong2_rect': wrong_images2['q14_w2_rect'],
                }
            },
            {
                'choices': ['Open', 'Close', 'Pointer'],
                'correct': 0,
                'images': {
                    'question': question_images['q15'],
                    'question_rect': question_images['q15_rect'],
                    'correct': correct_images['q15_c1'],
                    'correct_rect': correct_images['q15_c1_rect'],
                    'wrong1': wrong_images1['q15_w1'],
                    'wrong1_rect': wrong_images1['q15_w1_rect'],
                    'wrong2': wrong_images2['q15_w2'],
                    'wrong2_rect': wrong_images2['q15_w2_rect'],
                }
            },
            # Add more questions here
        ]
    }
}


def reset_button_states():
    start_button.reset()
    exit_button.reset()
    settings_button.reset()
    back_button.reset()
    next_button.reset()
    retry_button.reset()
    earthquake_button.reset()
    flood_button.reset()
    fire_button.reset()
    cam_button.reset()

def main_menu():
    while True:
        screen.blit(image_bg_global, image_rect_global)
        if start_button.draw(screen):
            reset_button_states()
            
            play_game()
            
        if settings_button.draw(screen):
            pass
        if exit_button.draw(screen):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

    

def play_game():
    running = True
    while running:
        screen.blit(image_bg_global, image_rect_global)

        if earthquake_button.draw(screen):
            play_quiz('earthquake')
        if flood_button.draw(screen):
            play_quiz('flood')
        if fire_button.draw(screen):
            play_quiz('fire')
        if back_button.draw(screen):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    reset_button_states()
    main_menu()



def play_quiz(quiz_type):
    quiz = quizzes[quiz_type]
    questions = quiz['questions']
    current_question = 0
    scenario = 'introduction'
    recognized_gesture = "None"
    life = 3

    running = True
    while running:
        screen.blit(image_bg_global, image_rect_global)

        if scenario == 'introduction':
            if quiz['introduction'] is not None:
                screen.blit(quiz['introduction'], (0, 0))
            if next_button.draw(screen):
                scenario = 'question'
        
        if scenario == 'question':
            question_data = questions[current_question]
            screen.blit(question_data['images']['question'], question_data['images']['question_rect'])
            
            if life == 3:
                screen.blit(image_hearts3, image_rect_hearts3)
            elif life == 2:
                screen.blit(image_hearts2, image_rect_hearts2)
            elif life == 1:
                screen.blit(image_hearts1, image_rect_hearts1)

            if cam_button.draw(screen):
                gesture_recognition = GestureRecognition(target_gestures = question_data['choices'])
                recognized_gesture = gesture_recognition.detect_gesture()

                if recognized_gesture in question_data['choices']:
                    selected_choice = question_data['choices'].index(recognized_gesture)
                    if selected_choice == question_data['correct']:
                        correct_sfx.play()
                        scenario = 'correct'
                    else:
                        life -= 1
                        wrong_sfx.play()
                        scenario = 'wrong'

            elif life == 0:
                gameover_sfx.play()
                scenario = 'gameover'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif scenario == 'correct':
            screen.blit(question_data['images']['correct'], question_data['images']['correct_rect'])
            if next_button.draw(screen):
                current_question += 1
                if current_question < len(questions):
                    scenario = 'question'
                else:
                    scenario = 'ending'

        elif scenario == 'wrong':
            if selected_choice == 1:
                wrong_key = 'wrong1'
            else:
                wrong_key = 'wrong2'
            screen.blit(question_data['images'][wrong_key], question_data['images'][wrong_key + '_rect'])
            if retry_button.draw(screen):
                scenario = 'question'

        elif scenario == 'ending':
            if quiz['ending'] is not None:
                screen.blit(quiz['ending'], (0, 0))
            if next_button.draw(screen):
                running = False

        elif scenario == 'gameover':
            screen.blit(image_gameover, (0, 0))
            if next_button.draw(screen):
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(30)

reset_button_states()
main_menu()
