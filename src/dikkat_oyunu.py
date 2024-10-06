def run():
    import cv2
    import mediapipe as mp
    import random
    import math
    import time
    import os
    import pandas as pd
    from datetime import datetime
    import anasayfa
    
    def save_score_to_csv(score):
        date_today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        excel_file = 'game_scores_balloon.xlsx'
        
        # Excel dosyasını oku veya oluştur
        try:
            df = pd.read_excel(excel_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Date Time', 'Player Score'])
        
        # Yeni veriyi DataFrame'e ekle
        new_data = {'Date Time': date_today, 'Player Score': score }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        
        # DataFrame'i Excel dosyasına yaz
        df.to_excel(excel_file, index=False)
    
    def run():
        # Initialize MediaPipe Hands module
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
    
        # Initialize MediaPipe Drawing module for drawing landmarks
        mp_drawing = mp.solutions.drawing_utils
    
        # Open a video capture object (0 for the default camera)
        cap = cv2.VideoCapture(0)
    
        # Define button coordinates
        button_width, button_height = 150, 50
        button_y = 10
        button_y_bottom = 550
        high_score_button_y = 100
    
        # Pause menu buttons coordinates
        continue_button_coords = (200, 200, 200 + button_width, 200 + button_height)
        restart_button_coords = (200, 300, 200 + button_width, 300 + button_height)
        main_menu_button_coords = (200, 400, 200 + button_width, 400 + button_height)
        
        # High score close button coordinates
        high_score_close_button_coords = (10, 140, 10 + button_width, 140 + button_height)
    
        # Initialize variables for ball position and speed
        ball_radius = 20
    
        # Initialize score variable
        score = 0
    
        # Initialize index finger coordinates
        index_finger_x, index_finger_y = 0, 0
    
        # Initialize game state
        game_highscore = False
        game_paused = False
        game_over = False
        paused_ball_x, paused_ball_y = 0, 0
        start_time = time.time()
        elapsed_time = 0
        game_duration = 60 # 60 seconds
        closed_int=0
    
        # Initialize list for red balls
        red_balls = []
    
        # Initialize list for green balls
        green_balls = []
    
        # Initialize high score variable
        high_score_file = "high_score.txt"
        if os.path.exists(high_score_file):
            with open(high_score_file, "r") as file:
                high_score = int(file.read().strip())
        else:
            high_score = 0
    
        def create_red_ball():
            """Create a red ball at a random position"""
            return {
                'x': random.randint(50, 590),
                'y': -ball_radius,
                'speed': random.randint(2, 5)
            }
    
        def create_green_ball():
            """Create a green ball at a random position"""
            return {
                'x': random.randint(50, 590),
                'y': -ball_radius,
                'speed': random.randint(2, 5)
            }
    
        # FULL SCREEN
        cv2.namedWindow('Fullscreen Window', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Fullscreen Window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
        # Initialize flag for displaying high score
        show_high_score = False
    
        # Game loop
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
    
            if not ret:
                continue
    
            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
            # Process the frame to detect hands
            results = hands.process(frame_rgb)
    
            # Get the height and width of the frame
            h, w, _ = frame.shape
    
            # Update elapsed time if the game is not paused
            if not game_paused:
                elapsed_time = time.time() - start_time
    
            # Check if time is up
            if not game_over and not game_paused and time.time() - start_time >= game_duration:
                game_over = True
                save_score_to_csv(score)
                
            if game_over:
                red_balls.clear()
                green_balls.clear()
    
            # Check if hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
                    # Get the coordinates of the index finger (landmark 8)
                    index_finger_x = int(hand_landmarks.landmark[8].x * w)
                    index_finger_y = int(hand_landmarks.landmark[8].y * h)
    
                    # Check if the index finger is over the pause button
                    if not game_paused:
                        if w - button_width - 10 < index_finger_x < w - 10 and button_y < index_finger_y < button_y + button_height:
                            game_paused = True
                            paused_ball_x, paused_ball_y = index_finger_x, index_finger_y
    
                    # Check if the index finger is over the reset button
                    if w - button_width - 10 < index_finger_x < w - 10 and button_y_bottom < index_finger_y < button_y_bottom + button_height:
                        # Reset the game
                        score = 0
                        game_paused = False
                        game_over = False
                        red_balls = []
                        green_balls = []
                        start_time = time.time()
                        elapsed_time = 0
    
    
                    # Check if the index finger is over the continue button in pause menu
                    if game_paused:
                        if continue_button_coords[0] < index_finger_x < continue_button_coords[2] and continue_button_coords[1] < index_finger_y < continue_button_coords[3]:
                            game_paused = False
                            start_time = time.time() - elapsed_time
    
                        # Check if the index finger is over the restart button in pause menu
                        elif restart_button_coords[0] < index_finger_x < restart_button_coords[2] and restart_button_coords[1] < index_finger_y < restart_button_coords[3]:
                            score = 0
                            game_paused = False
                            game_over = False
                            red_balls = []
                            green_balls = []
                            start_time = time.time()
                            elapsed_time = 0
    
                        # Check if the index finger is over the main menu button in pause menu
                        elif main_menu_button_coords[0] < index_finger_x < main_menu_button_coords[2] and main_menu_button_coords[1] < index_finger_y < main_menu_button_coords[3]:
                            closed_int = 1
                            anasayfa.run()
    
    
            # Move the balls if the game is not paused
            if not game_paused:
                # Move the red balls
                for ball in red_balls:
                    ball['y'] += ball['speed']
                    if ball['y'] > h + ball_radius:
                        ball['y'] = -ball_radius
                        ball['x'] = random.randint(50, 590)
    
                    # Check collision with hand
                    distance = math.sqrt((index_finger_x - ball['x']) ** 2 + (index_finger_y - ball['y']) ** 2)
                    if distance < ball_radius and ball['y'] > 0:
                        score -= 1
                        ball['y'] = -ball_radius
                        ball['x'] = random.randint(50, 590)
    
                # Move the green balls
                for ball in green_balls:
                    ball['y'] += ball['speed']
                    if ball['y'] > h + ball_radius:
                        ball['y'] = -ball_radius
                        ball['x'] = random.randint(50, 590)
    
                    # Check collision with hand
                    distance = math.sqrt((index_finger_x - ball['x']) ** 2 + (index_finger_y - ball['y']) ** 2)
                    if distance < ball_radius and ball['y'] > 0:
                        score += 1
                        ball['y'] = -ball_radius
                        ball['x'] = random.randint(50, 590)
    
                # Add new balls at random intervals
                if random.random() < 0.02:
                    red_balls.append(create_red_ball())
                if random.random() < 0.02:
                    green_balls.append(create_green_ball())
    
            # Draw pause button rectangle
            cv2.rectangle(frame, (w - button_width - 10, button_y), (w - 10, button_y + button_height), (255, 0, 0), -1)
            cv2.putText(frame, 'Pause', (w - button_width + 20, button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
            # Draw reset button rectangle
            cv2.rectangle(frame, (w - button_width - 10, button_y_bottom), (w - 10, button_y_bottom + button_height), (0, 0, 255), -1)
            cv2.putText(frame, 'Reset', (w - button_width + 5, button_y_bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
            
            # Draw high score close button rectangle if high score is displayed
    
            # Draw elapsed time
            if not game_over:
                cv2.putText(frame, f'Time: {int(game_duration - elapsed_time)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                cv2.putText(frame, 'Game Over', (w // 2 - 100, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    
            # Draw current score on the frame
            cv2.putText(frame, f'Score: {score}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
            # Draw the balls
            for ball in red_balls:
                cv2.circle(frame, (ball['x'], ball['y']), ball_radius, (0, 0, 255), -1)
            for ball in green_balls:
                cv2.circle(frame, (ball['x'], ball['y']), ball_radius, (0, 255, 0), -1)
    
            # Draw pause menu buttons if the game is paused
            if game_paused:
                cv2.rectangle(frame, continue_button_coords[:2], continue_button_coords[2:], (0, 255, 0), -1)
                cv2.putText(frame, 'Continue', (continue_button_coords[0] + 10, continue_button_coords[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.rectangle(frame, restart_button_coords[:2], restart_button_coords[2:], (0, 255, 255), -1)
                cv2.putText(frame, 'Restart', (restart_button_coords[0] + 10, restart_button_coords[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.rectangle(frame, main_menu_button_coords[:2], main_menu_button_coords[2:], (255, 0, 0), -1)
                cv2.putText(frame, 'Main Menu', (main_menu_button_coords[0] + 10, main_menu_button_coords[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                if show_high_score:
                    cv2.putText(frame, f'High Score: {high_score}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.rectangle(frame, high_score_close_button_coords[:2], high_score_close_button_coords[2:], (255, 0, 0), -1)
                    cv2.putText(frame, 'High Score Close', (high_score_close_button_coords[0] + 5, high_score_close_button_coords[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    
                if game_highscore:
                        if high_score_close_button_coords[0] < index_finger_x < high_score_close_button_coords[2] and high_score_close_button_coords[1] < index_finger_y < high_score_close_button_coords[3]:
                            # Close high score display
                            show_high_score = False
                            game_highscore = False
    
                if not game_highscore:      
                    cv2.rectangle(frame, (w - button_width - 10, high_score_button_y), (w - 10, high_score_button_y + button_height), (0, 255, 0), -1)
                    cv2.putText(frame, 'High Score', (w - button_width + 5, high_score_button_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
                if not game_highscore:
                        if w - button_width - 10 < index_finger_x < w - 10 and high_score_button_y < index_finger_y < high_score_button_y + button_height:
                            # Toggle high score display
                            show_high_score = True
                            game_highscore = True
    
                
    
            
            
            if game_over:
                cv2.rectangle(frame, restart_button_coords[:2], restart_button_coords[2:], (0, 255, 255), -1)
                cv2.putText(frame, 'Restart', (restart_button_coords[0] + 10, restart_button_coords[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.rectangle(frame, main_menu_button_coords[:2], main_menu_button_coords[2:], (255, 0, 0), -1)
                cv2.putText(frame, 'Main Menu', (main_menu_button_coords[0] + 10, main_menu_button_coords[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
                if restart_button_coords[0] < index_finger_x < restart_button_coords[2] and restart_button_coords[1] < index_finger_y < restart_button_coords[3]:
                            score = 0
                            game_paused = False
                            game_over = False
                            red_balls = []
                            green_balls = []
                            start_time = time.time()
                            elapsed_time = 0
    
                        # Check if the index finger is over the main menu button in pause menu
                if main_menu_button_coords[0] < index_finger_x < main_menu_button_coords[2] and main_menu_button_coords[1] < index_finger_y < main_menu_button_coords[3]:
                            closed_interval = 1
                            anasayfa.run()
    
            if closed_int == 1:
                break
            # Display the frame
            cv2.imshow('Fullscreen Window', frame)
    
            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        # Release the video capture object and close the windows
        cap.release()
        cv2.destroyAllWindows()
    
    run()