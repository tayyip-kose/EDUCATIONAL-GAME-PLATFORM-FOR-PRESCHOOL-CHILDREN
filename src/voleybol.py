import cv2
import mediapipe as mp
import pygame
import random
import time
import pandas as pd
from datetime import datetime
import anasayfa

def run():
    global cap, hands, mp_drawing, mp_hands, font, ball_radius, ball_color, ball_x, ball_y, ball_speed_x, ball_speed_y, gravity, scorePlayer1, scorePlayer2, counter, game_over, start_time, pause, elapsed_time, closed_int, csv_file, net_x, net_height, net_thickness

    # Pygame ve ses ayarları
    pygame.mixer.init()
    
    # Kamera ve Mediapipe Ayarları
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils
    
    # Oyun Değişkenleri
    ball_radius = 20
    ball_color = (0, 255, 0)
    ball_x = random.randint(ball_radius, 640 - ball_radius)
    ball_y = ball_radius
    ball_speed_x = random.uniform(-3, 3)  # Rastgele x hız
    ball_speed_y = 5
    gravity = 0.5  # Yerçekimi etkisi
    scorePlayer1 = 0
    scorePlayer2 = 0
    counter = 60
    font = cv2.FONT_HERSHEY_SIMPLEX
    game_over = False
    start_time = time.time()
    pause = False
    elapsed_time = 0
    closed_int = 0
    
    # CSV Dosyası Ayarları
    csv_file = 'game_scores_new.xlsx'  # Yeni dosya adı
    
    # Tam Ekran Pencere Ayarları
    cv2.namedWindow('Fullscreen Window', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Fullscreen Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    def reset_game():
        global ball_x, ball_y, ball_speed_x, ball_speed_y, scorePlayer1, scorePlayer2, game_over, counter, start_time, pause, elapsed_time
        ball_x = random.randint(ball_radius, 640 - ball_radius)
        ball_y = ball_radius
        ball_speed_x = random.uniform(-3, 3)
        ball_speed_y = 5
        scorePlayer1 = 0
        scorePlayer2 = 0
        counter = 60
        game_over = False
        start_time = time.time()
        pause = False
        elapsed_time = 0
    
    def ball_restart():
        global ball_x, ball_y, ball_speed_x, ball_speed_y, game_over
        ball_x = random.randint(ball_radius, 640 - ball_radius)
        ball_y = ball_radius
        ball_speed_x = random.uniform(-3, 3)
        ball_speed_y = 5
        game_over = False
    
    def toggle_pause():
        global pause, start_time, elapsed_time
        pause = not pause
        if pause:
            elapsed_time = time.time() - start_time
        else:
            start_time = time.time() - elapsed_time
    
    def draw_pause_button(frame, w, h):
        if not pause:
            cv2.rectangle(frame, (w - 80, 50), (w, 80), (0, 0, 255), -1)
            cv2.putText(frame, 'Durdur' , (w - 70, 70), font, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        if pause:
            cv2.rectangle(frame, (w - 80, 90), (w, 120), (0, 255, 0), -1)
            cv2.putText(frame, 'Devam', (w - 70, 110), font, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (w - 80, 130), (w, 160), (0, 0, 255), -1)
            cv2.putText(frame, 'Yenile', (w - 70, 150), font, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (w - 110, 170), (w, 200), (200, 100, 200), -1)
            cv2.putText(frame, 'Ana Menu', (w - 100, 190), font, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    
    def save_score_to_csv(player1_score, player2_score):
        date_today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        excel_file = 'game_scores_new.xlsx'  # Yeni dosya adı
        
        # Excel dosyasını oku veya oluştur
        try:
            df = pd.read_excel(excel_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Date Time', 'Player 1 Score', 'Player 2 Score'])
        
        # Yeni veriyi DataFrame'e ekle
        new_data = {'Date Time': date_today, 'Player 1 Score': player1_score, 'Player 2 Score': player2_score}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        
        # DataFrame'i Excel dosyasına yaz
        df.to_excel(excel_file, index=False)
    
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            continue
    
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        h, w, _ = frame.shape
    
        net_x = w // 2
        net_height = h // 2
        net_thickness = 10
    
        if not game_over:
            if not pause:
                elapsed_time = time.time() - start_time
                counter = 60 - int(elapsed_time)
    
                if counter <= 0:
                    game_over = True
                    save_score_to_csv(scorePlayer1, scorePlayer2)
    
                # Topun Hareketi ve Yerçekimi
                ball_speed_y += gravity
                ball_x += ball_speed_x
                ball_y += ball_speed_y
    
                if scorePlayer1 == 5 or scorePlayer2 == 5:
                    game_over = True
                    save_score_to_csv(scorePlayer1, scorePlayer2)
    
                # Player1 sahasına düşüp, player2 score alması:
                if ball_y > h - ball_radius and ball_x < w / 2 - net_thickness:
                    scorePlayer2 += 1  # Player2 score alması
                    ball_restart()
    
                # Player2 sahasına düşüp, player1 score alması:
                if ball_y > h - ball_radius and ball_x > w / 2 - net_thickness:
                    scorePlayer1 += 1  # Player1 score alması
                    ball_restart()
    
                # Kenarlara Çarpma Kontrolü
                if ball_x < ball_radius or ball_x > w - ball_radius:
                    ball_speed_x = -ball_speed_x  # Kenarlara çarpınca yön değiştir
    
                # Fileye Çarpma Kontrolü
                if net_x - net_thickness < ball_x + ball_radius < net_x + net_thickness and ball_y > net_height:
                    ball_speed_x = -(ball_speed_x * 1.5)
                if net_x - net_thickness < ball_x - ball_radius < net_x + net_thickness and ball_y > net_height:
                    ball_speed_x = -(ball_speed_x * 1.5)
    
                # El Tespiti
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w
                        finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h
    
                        # Top ile Elin Çarpışma Kontrolü
                        if (ball_x - finger_x) ** 2 + (ball_y - finger_y) ** 2 < (ball_radius * 2) ** 2:
                            ball_speed_y = -abs(ball_speed_y)  # El ile temas edince yukarı sekme
                            ball_speed_x += (ball_x - finger_x) * 0.15  # El ile temas edince x yönü değiştir
    
            # Topu ve Skoru Çiz
            cv2.circle(frame, (int(ball_x), int(ball_y)), ball_radius, ball_color, -1)
            cv2.putText(frame, f'Player1: {scorePlayer1}', (10, 25), font, 0.75, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Player2: {scorePlayer2}', (w - 130, 25), font, 0.75, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Time: {counter}', (w // 2 - 35, 25), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Player1: {scorePlayer1}', (w // 2 - 250, h // 2 - 200), font, 1, (0, 255, 255), 3, cv2.LINE_AA)
            cv2.putText(frame, f'Player2: {scorePlayer2}', (w - 250, h // 2 - 200), font, 1, (255, 0, 0), 3, cv2.LINE_AA)
            cv2.rectangle(frame, (w // 2 - 35 , h // 2 - 50), (w // 2 + 30 , h // 2 - 10), (255, 0, 0), -1)
            cv2.putText(frame, 'Tekrar', (w // 2 - 30, h // 2 - 20), font, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
     
        # File Çizimi
        cv2.line(frame, (net_x, h), (net_x, net_height), (0, 255, 255), net_thickness)
    
        # Pause butonunu çiz
        draw_pause_button(frame, w, h)
    
        # El tespiti ve butonlara basma kontrolü
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w
                finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h
    
                if not pause and  w - 80 < finger_x < w and 50 < finger_y < 80:
                    toggle_pause()
                if pause and  w - 80 < finger_x < w and 90 < finger_y < 120:
                    toggle_pause()
                if pause and  w - 80 < finger_x < w and 130 < finger_y < 160:
                    reset_game()            
                if pause and  w - 110 < finger_x < w and 170 < finger_y < 200:
                    closed_int = 1
                    anasayfa.run()
                    
                elif w // 2 - 35 < finger_x < w // 2 + 30 and h // 2 - 50 < finger_y < h // 2 - 10 and game_over:
                    reset_game()
                    
    
        cv2.imshow('Fullscreen Window', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if closed_int == 1:
            break
    cap.release()
    cv2.destroyAllWindows()
