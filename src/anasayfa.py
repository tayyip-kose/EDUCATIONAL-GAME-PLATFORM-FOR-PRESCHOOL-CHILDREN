def run():
    import cv2
    import mediapipe as mp
    import pygame
    import random
    import time
    import math
    import sekil_secimi as oyun1
    import dikkat_oyunu as oyun2
    import renk_secimi as oyun3
    import voleybol as oyun4
    
    pygame.init()
    pygame.mixer.music.load("start_music.mp3")
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils
    font = cv2.FONT_HERSHEY_SIMPLEX
    button_size = 100
    margin = 40
    closed_int = 0
    music_bool = True
    
    #FULL SCREEN
    cv2.namedWindow('Fullscreen Window', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Fullscreen Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    
    while cap.isOpened() :
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        if not ret:
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        h, w, _ = frame.shape
        # Draw buttons on each corner of the frame
        cv2.rectangle(frame, (margin, margin), (margin + button_size, margin + button_size), (255, 0, 0), 2)  # Top-left 
        cv2.rectangle(frame, (w - margin - button_size, margin), (w - margin, margin + button_size), (255, 0, 0), 2)  # Top-right 
        cv2.rectangle(frame, (margin, h - margin - button_size), (margin + button_size, h - margin), (255, 0, 0), 2)  # Bottom-left 
        cv2.rectangle(frame, (w - margin - button_size, h - margin - button_size), (w - margin, h - margin), (255, 0, 0), 2)  # Bottom-right 
        
        cv2.putText(frame, 'Sekiller', (margin + 10, margin + 60), font, 0.6, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Dikkat!', (w - margin - button_size + 10, margin + 60), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Renkler', (margin + 10, h - margin - 40), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Voleybol', (w - margin - button_size + 10, h - margin - 40), font, 0.6, (255, 255, 0), 2, cv2.LINE_AA)
    
        if music_bool == True:
            pygame.mixer.music.play(loops=-1)
            music_bool = False
    
         # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
                # Check if the hand is close to any of the buttons
                finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w
                finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h
                
                if margin < finger_x < margin + button_size and margin < finger_y < margin + button_size:
                    print("Sol Üst Kutucuğa Tıkladınız")
                    pygame.mixer.music.stop()
                    closed_int = 1
                    oyun1.run()
    
                elif w - margin - button_size < finger_x < w - margin and margin < finger_y < margin + button_size:
                    print("Sağ Üst Kutucuğa Tıkladınız")
                    pygame.mixer.music.stop()
                    closed_int = 1
                    oyun2.run()
    
                elif margin < finger_x < margin + button_size and h - margin - button_size < finger_y < h - margin:
                    print("Sol Alt Kutucuğa Tıkladınız")
                    pygame.mixer.music.stop()
                    closed_int = 1
                    oyun3.run()
                elif w - margin - button_size < finger_x < w - margin and h - margin - button_size < finger_y < h - margin:
                    print("Sağ Alt Kutucuğa Tıkladınız")
                    pygame.mixer.music.stop()
                    closed_int = 1
                    oyun4.run()
                  
    
        
            
        cv2.imshow('Fullscreen Window', frame)
        
        if closed_int == 1:
            break
    
        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    pygame.mixer.music.stop()       
    cap.release()
    cv2.destroyAllWindows()