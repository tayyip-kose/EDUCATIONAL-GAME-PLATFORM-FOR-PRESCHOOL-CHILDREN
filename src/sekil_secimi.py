def run():
    import cv2
    import mediapipe as mp
    import pygame
    import random
    import time
    import anasayfa
    import csv
    from datetime import datetime
    
    def random_image(true_num, false_num):
        images = {0: "daire.png", 1: "kare.png", 2: "ucgen.png", 3: "yildiz.png"}
        true_num = random.randint(0, 3)
        false_num = random.randint(0, 3)
        
        while false_num == true_num:
            false_num = random.randint(0, 3)
        return true_num, false_num
    
    def print_image(): 
        if case_num == 0:
            true_resized = cv2.resize(true_img, (button_size - 20, button_size - 20))
            frame[margin + 10:margin + button_size - 10, margin + 10:margin + button_size - 10] = true_resized
            false_resized = cv2.resize(false_img, (button_size - 20, button_size - 20))
            frame[margin + 10:margin + button_size - 10, margin + 340:margin + button_size + 320] = false_resized
        else:
            true_resized = cv2.resize(true_img, (button_size - 20, button_size - 20))
            frame[margin + 10:margin + button_size - 10, margin + 340:margin + button_size + 320] = true_resized
            false_resized = cv2.resize(false_img, (button_size - 20, button_size - 20))
            frame[margin + 10:margin + button_size - 10, margin + 10:margin + button_size - 10] = false_resized
    
    def log_game_duration(duration):
        with open('sekiller_dosyalar/sekil_secimi_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), duration])
    
    images = {0: "daire.png", 1: "kare.png", 2: "ucgen.png", 3: "yildiz.png"}
    sounds = {0: "daire.wav", 1: "kare.wav", 2: "ucgen.wav", 3: "yildiz.wav"}
    sound_options = {0: "erkek", 1: "kadin"}
    sound_options_2 = {0:"ingilizce/",1:"turkce/"}
    sound_options_int = 1
    sound_options_int_2 = 1
    # Initialize MediaPipe Hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    # Initialize MediaPipe Drawing module for drawing landmarks
    mp_drawing = mp.solutions.drawing_utils
    true_num = 0
    false_num = 0
    true_num, false_num = random_image(true_num, false_num)
    case_num = random.randint(0, 1)
    print(case_num)
    
    pygame.init()
    pygame.mixer.music.load("sekiller_dosyalar/sounds/ingilizce/kadin/yanlis.wav")
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/kadin/dogru.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/kadin/daire.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/kadin/ucgen.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/kadin/kare.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/kadin/yildiz.wav')
    
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/erkek/yanlis.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/erkek/dogru.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/erkek/daire.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/erkek/ucgen.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/erkek/kare.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/ingilizce/erkek/yildiz.wav')
    
    pygame.mixer.music.load("sekiller_dosyalar/sounds/turkce/kadin/yanlis.wav")
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/kadin/dogru.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/kadin/daire.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/kadin/ucgen.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/kadin/kare.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/kadin/yildiz.wav')
    
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/erkek/yanlis.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/erkek/dogru.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/erkek/daire.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/erkek/ucgen.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/erkek/kare.wav')
    pygame.mixer.music.load('sekiller_dosyalar/sounds/turkce/erkek/yildiz.wav')
    
    sound_yanlis = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/yanlis.wav")
    sound_dogru = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/dogru.wav")
    
    # Open a video capture object (0 for the default camera)
    cap = cv2.VideoCapture(0)
    
    # Define button size and margin
    button_size = 150
    small_button_size = 50
    margin = 80
    current_state = False
    moment = 0
    start_sound_bool = False
    score = 0
    score_txt = "Skor: " + str(score)
    font = cv2.FONT_HERSHEY_SIMPLEX
    filled_button = 1
    filled_button_2 = 1
    paused = False
    closed_int = 0
    start_time_bool =True
    # FULL SCREEN
    cv2.namedWindow('Fullscreen Window', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Fullscreen Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    while cap.isOpened():
        if start_time_bool == True:
            start_time = time.time()
            start_time_bool = False
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, score_txt, (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        if not ret:
            continue
        true_img = cv2.imread("sekiller_dosyalar/images/" + str(images[true_num]))
        false_img = cv2.imread("sekiller_dosyalar/images/" + str(images[false_num]))
    
        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Process the frame to detect hands
        results = hands.process(frame_rgb)
    
        # Get the height and width of the frame
        h, w, _ = frame.shape
    
        # Draw buttons on each corner of the frame
        cv2.rectangle(frame, (margin, margin), (margin + button_size, margin + button_size), (255, 0, 0), 2)  # Top-left (Blue)
        cv2.rectangle(frame, (w - margin - button_size, margin), (w - margin, margin + button_size), (0, 255, 0), 2)  # Top-right (Green)
    
        if not paused:
            print_image()
    
            # Start Sound Loop
            if not start_sound_bool:
                sound_true = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/" + str(sounds[true_num]))
                sound_true.play()
                start_sound_bool = True
                
            # Pause button
            pause_button_pos = (w - small_button_size - 10, 10, w - 10, 10 + small_button_size)
            cv2.rectangle(frame, (pause_button_pos[0], pause_button_pos[1]), (pause_button_pos[2], pause_button_pos[3]), (0, 0, 255), -1)
            cv2.putText(frame, 'Durdur', (pause_button_pos[0]- 1, pause_button_pos[1] + 30), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
           
            # Check if hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w
                    finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h
    
                    # Pause button detection
                    if pause_button_pos[0] < finger_x < pause_button_pos[2] and pause_button_pos[1] < finger_y < pause_button_pos[3]:
                        paused = True
                        
                    # Check if the hand is close to the top-left button
                    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w < margin + button_size and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h < margin + button_size:                
                        if not current_state:
                            if case_num == 0:
                                print("Doğru Seçim!") 
                                sound_dogru.play()
                                score += 1
                            else:
                                print("Yalnış Seçim")
                                sound_yanlis.play()
                            if score > 2:
                                score_txt = "Tebrikler Skoru Tamamladiniz"
                                finish_time = time.time()
                                log_game_duration(finish_time-start_time)
                                current_state = True
                            else: 
                                score_txt = "Skor: " + str(score)
                                true_num, false_num = random_image(true_num, false_num)
                                sound_true = pygame.mixer.Sound('sekiller_dosyalar/sounds/' + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/" + str(sounds[true_num]))
                                sound_true.play()
                                case_num = random.randint(0, 1)
                                moment = time.time()                   
                                current_state = True
                        if time.time() - moment > 3 and not (score > 2):
                            current_state = False                  
                        print("Maviye Bastın")
                    elif hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w > w - margin - button_size and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h < margin + button_size:
                        if not current_state:
                            if case_num == 0:
                                print("Yalnış Seçim!")   
                                sound_yanlis.play()
                            else:
                                print("Doğru Seçim")
                                sound_dogru.play()
                                score += 1
                            if score > 2:
                                score_txt = "Tebrikler Skoru Tamamladiniz"
                                finish_time = time.time()
                                log_game_duration(finish_time-start_time)
                                current_state = True
                            else:
                                score_txt = "Skor: " + str(score)
                                true_num, false_num = random_image(true_num, false_num)
                                sound_true = pygame.mixer.Sound('sekiller_dosyalar/sounds/' + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/" + str(sounds[true_num]))
                                sound_true.play()
                                case_num = random.randint(0, 1)
                                moment = time.time()                   
                                current_state = True
                        if time.time() - moment > 3 and not (score > 2):
                            current_state = False                
                        print("Yeşile bastın")
    
        else:
            # Pause screen
            cv2.putText(frame, 'Oyun Duraklatildi', (w // 2 - 150, h // 2 - 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # Resume button
            resume_button_pos = (w // 2 - 100, h // 2, w // 2 + 100, h // 2 + 50)
            cv2.rectangle(frame, (resume_button_pos[0], resume_button_pos[1]), (resume_button_pos[2], resume_button_pos[3]), (0, 255, 0), -1)
            cv2.putText(frame, 'Devam Ettir', (resume_button_pos[0] + 10, resume_button_pos[1] + 30), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    
            # Restart button
            restart_button_pos = (w // 2 - 100, h // 2 + 60, w // 2 + 100, h // 2 + 110)
            cv2.rectangle(frame, (restart_button_pos[0], restart_button_pos[1]), (restart_button_pos[2], restart_button_pos[3]), (255, 0, 0), -1)
            cv2.putText(frame, 'Yeniden Baslat', (restart_button_pos[0] + 10, restart_button_pos[1] + 30), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    
            # Back to Menu button
            menu_button_pos = (w // 2 - 100, h // 2 + 120, w // 2 + 100, h // 2 + 170)
            cv2.rectangle(frame, (menu_button_pos[0], menu_button_pos[1]), (menu_button_pos[2], menu_button_pos[3]), (255, 0, 0), -1)
            cv2.putText(frame, 'Menuye Don', (menu_button_pos[0] + 10, menu_button_pos[1] + 30), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
            
    
            
            #Small Buttons(Sound Choise)
            #Right Down
            if filled_button == 1:
                cv2.rectangle(frame, (w - small_button_size - 10, h - 2*small_button_size - 20), (w - 10, h - small_button_size - 20), (0, 255, 255), -1)  # Filled
            else:
                cv2.rectangle(frame, (w - small_button_size - 10, h - 2*small_button_size - 20), (w - 10, h - small_button_size - 20), (0, 255, 255), 2)  # Empty
    
            if filled_button == 2:
                cv2.rectangle(frame, (w - small_button_size - 10, h - small_button_size - 10), (w - 10, h - 10), (255, 0, 255), -1)  # Filled
            else:
                cv2.rectangle(frame, (w - small_button_size - 10, h - small_button_size - 10), (w - 10, h - 10), (255, 0, 255), 2)  # Empty
            
            #Left Down
            if filled_button_2 == 1:
                cv2.rectangle(frame, (10, h - 2*small_button_size - 20), (10 + small_button_size, h - small_button_size - 20), (0, 255, 255), -1)  # Filled
            else:
                cv2.rectangle(frame, (10, h - 2*small_button_size - 20), (10 + small_button_size, h - small_button_size - 20), (0, 255, 255), 2)  # Empty
    
            if filled_button_2 == 2:
                 cv2.rectangle(frame, (10, h - small_button_size - 10), (10 + small_button_size, h - 10), (255, 0, 255), -1)  # Filled
            else:
                 cv2.rectangle(frame, (10, h - small_button_size - 10), (10 + small_button_size, h - 10), (255, 0, 255), 2)  # Empty
    
    
            cv2.putText(frame, 'Kadin', (w - small_button_size - 7, h - 2 * small_button_size + 10), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, 'Erkek', (w - small_button_size - 7, h - small_button_size + 20), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, 'TR', (20, h - 2*small_button_size + 10), font, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, 'EN', (20, h - small_button_size + 20), font, 0.6, (0, 0, 0), 2, cv2.LINE_AA)        
    
            # Check if hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w
                    finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h
    
                    # Resume button detection
                    if resume_button_pos[0] < finger_x < resume_button_pos[2] and resume_button_pos[1] < finger_y < resume_button_pos[3]:
                        paused = False
    
                    # Restart button detection
                    if restart_button_pos[0] < finger_x < restart_button_pos[2] and restart_button_pos[1] < finger_y < restart_button_pos[3]:
                        paused = False
                        score = 0
                        score_txt = "Skor: " + str(score)
                        true_num, false_num = random_image(true_num, false_num)
                        sound_true = pygame.mixer.Sound('sekiller_dosyalar/sounds/' + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/" + str(sounds[true_num]))
                        sound_true.play()
                        case_num = random.randint(0, 1)
                        moment = time.time() 
                        start_time_bool= True
                        current_state = True
                    #Menu button detection                     
                    if menu_button_pos[0] < finger_x < menu_button_pos[2] and menu_button_pos[1] < finger_y < menu_button_pos[3]:
                        closed_int = 1
                        anasayfa.run()
                        
                    # Sound choice buttons
                    if w - small_button_size - 10 < finger_x < w - 10 and h - 2 * small_button_size - 20 < finger_y < h - small_button_size - 20:
                        print("Ses 1 e tıkladınız")
                        filled_button = 1
                        sound_options_int = 1
                        sound_yanlis = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/yanlis.wav")
                        sound_dogru = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/dogru.wav")
                    elif w - small_button_size - 10 < finger_x < w - 10 and h - small_button_size - 10 < finger_y < h - 10:
                        print("Ses 2 ye tıkladınız")
                        filled_button = 2
                        sound_options_int = 0
                        sound_yanlis = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/yanlis.wav")
                        sound_dogru = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/dogru.wav")
                        
                    if 10 < finger_x < 10 + small_button_size and h - 2 * small_button_size - 20 < finger_y < h - small_button_size - 20:
                        print("Ses 1 e tıkladınız")
                        filled_button_2 = 1
                        sound_options_int_2 = 1
                        sound_yanlis = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/yanlis.wav")
                        sound_dogru = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/dogru.wav")
                    elif 10 < finger_x <10 + small_button_size and h - small_button_size - 10 < finger_y < h - 10:
                        print("Ses 2 ye tıkladınız")
                        filled_button_2 = 2
                        sound_options_int_2 = 0
                        sound_yanlis = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/yanlis.wav")
                        sound_dogru = pygame.mixer.Sound("sekiller_dosyalar/sounds/" + str(sound_options_2[sound_options_int_2]) + str(sound_options[sound_options_int]) + "/dogru.wav")
    
        if closed_int == 1:
            break
        # Display the frame with hand landmarks
        cv2.imshow('Fullscreen Window', frame)
    
        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
