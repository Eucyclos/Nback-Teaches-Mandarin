import pygame, random, time, sys, os

pygame.init()
pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('N-Back Game')

# Colors and Fonts
WHITE, BLACK, GRAY, GREEN, RED = (255, 255, 255), (0, 0, 0), (200, 200, 200), (0, 255, 0), (255, 0, 0)
font, input_font, score_font = pygame.font.SysFont('Arial', 50), pygame.font.SysFont('Arial', 30), pygame.font.SysFont('Arial', 20)

# Load assets and scale images to half size
images_folder, sounds_folder = os.path.join('assets', 'images'), os.path.join('assets', 'sounds')

# Load the 'cover' image
cover_image = pygame.image.load(os.path.join(images_folder, 'cover.png')).convert()
cover_image = pygame.transform.scale(cover_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Generate 6 unique random indices
indices = random.sample(range(1, 100), 6)

# Load images and sounds based on the selected indices
images = [pygame.transform.scale(pygame.image.load(os.path.join(images_folder, f'image_{i}.png')).convert(), (pygame.image.load(os.path.join(images_folder, f'image_{i}.png')).get_width() // 2, pygame.image.load(os.path.join(images_folder, f'image_{i}.png')).get_height() // 2)) for i in indices]
sounds = [pygame.mixer.Sound(os.path.join(sounds_folder, f'100 common words.mkv.{i}.wav')) for i in indices]

class NBackGame:
    def __init__(self):
        self.n, self.goal = self.get_user_input()
        self.reset_game()

    def reset_game(self):
        self.sequence, self.game_over, self.current_image, self.current_sound = [], False, None, None
        self.correct_matches, self.total_matches, self.false_positives = 0, 0, 0
        self.start_time, self.last_click_time = time.time(), 0
        self.match_window_closed = False  # Flag to track match window closure
        self.button_color = GRAY  # Default button color

    def draw_button(self, text, font, color, rect):
        pygame.draw.rect(screen, color, rect)
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

    def draw_score(self):
        score_text = f"Correct Matches: {self.correct_matches}/{self.total_matches}   False Positives: {self.false_positives}"
        screen.blit(score_font.render(score_text, True, BLACK), (10, 10))

    def get_user_input(self):
        input_box_n, input_box_goal, start_button = pygame.Rect(350, 270, 100, 50), pygame.Rect(350, 340, 100,
                                                                                                50), pygame.Rect(350,
                                                                                                                 410,
                                                                                                                 100,
                                                                                                                 50)
        user_text_n, user_text_goal = '2', '10'
        input_active_n, input_active_goal = True, False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return pygame.quit(), sys.exit()
                if event.type == pygame.KEYDOWN:
                    if input_active_n:
                        if event.key == pygame.K_RETURN:
                            input_active_n, input_active_goal = False, True
                        elif event.key == pygame.K_BACKSPACE:
                            user_text_n = user_text_n[:-1]
                        else:
                            user_text_n += event.unicode
                    elif input_active_goal:
                        if event.key == pygame.K_RETURN:
                            return int(user_text_n), int(user_text_goal)
                        elif event.key == pygame.K_BACKSPACE:
                            user_text_goal = user_text_goal[:-1]
                        else:
                            user_text_goal += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box_n.collidepoint(event.pos):
                        input_active_n, input_active_goal = True, False
                    elif input_box_goal.collidepoint(event.pos):
                        input_active_n, input_active_goal = False, True
                    elif start_button.collidepoint(event.pos):
                        return int(user_text_n), int(user_text_goal)

            # Blit the cover image as the background
            screen.blit(cover_image, (0, 0))

            # Draw white rectangles behind input boxes and labels
            pygame.draw.rect(screen, WHITE, input_box_n.inflate(10, 10))
            pygame.draw.rect(screen, WHITE, input_box_goal.inflate(10, 10))
            pygame.draw.rect(screen, WHITE, start_button.inflate(10, 10))

            for box, text in [(input_box_n, user_text_n), (input_box_goal, user_text_goal)]:
                pygame.draw.rect(screen, BLACK, box, 2)
                screen.blit(input_font.render(text, True, BLACK), (box.x + 5, box.y + 5))
            self.draw_button("Start", input_font, GRAY, start_button)

            # Draw white rectangles behind labels
            for label, pos in [("Enter n:", (230, 280)), ("# of Matches to Win:", (90, 350))]:
                label_surface = input_font.render(label, True, BLACK)
                label_rect = label_surface.get_rect(topleft=pos).inflate(20, 20)
                pygame.draw.rect(screen, WHITE, label_rect)
                screen.blit(label_surface, pos)
            pygame.display.flip()

    def show_end_screen(self):
        play_again, exit_game = pygame.Rect(300, 450, 200, 60), pygame.Rect(300, 550, 200, 60)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return pygame.quit(), sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again.collidepoint(event.pos): return
                    if exit_game.collidepoint(event.pos): return pygame.quit(), sys.exit()

            # Blit the cover image as the background
            screen.blit(cover_image, (0, 0))

            # Draw white rectangles behind text and center the text
            for text, y in [("Game Over!", 250), (f"Score: {self.correct_matches}/{self.total_matches}", 350),
                            (f"False Positives: {self.false_positives}", 390)]:
                label_surface = input_font.render(text, True, BLACK)
                label_rect = label_surface.get_rect(center=(SCREEN_WIDTH // 2, y)).inflate(20, 20)
                pygame.draw.rect(screen, WHITE, label_rect)

                # Center the text within the rectangle
                text_x = label_rect.centerx - (label_surface.get_width() // 2)
                text_y = label_rect.centery - (label_surface.get_height() // 2)
                screen.blit(label_surface, (text_x, text_y))

            self.draw_button("Play Again", input_font, GRAY, play_again)
            self.draw_button("Exit", input_font, GRAY, exit_game)
            pygame.display.flip()

    def run_game(self):
        match_button = pygame.Rect(350, 410, 100, 50)
        image_changed = False

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if match_button.collidepoint(event.pos) and image_changed:
                        # Check if the user's current turn matches the n-th turn back
                        if len(self.sequence) > self.n:
                            if self.sequence[-self.n - 2] == self.sequence[-2]:
                                self.correct_matches += 1
                                self.button_color = GREEN  # Turn button green for correct match
                            else:
                                self.false_positives += 1
                                self.button_color = RED  # Turn button red for false positive
                        image_changed = False

            screen.fill(WHITE)
            if self.current_image:
                # Calculate the center position for the image
                image_rect = self.current_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(self.current_image, image_rect.topleft)
            if self.current_sound:
                self.current_sound.play()
            self.draw_button("Match", input_font, self.button_color, match_button)
            self.draw_score()
            pygame.display.flip()

            # Choose a random index for both image and sound
            index = random.randint(0, len(images) - 1)
            self.current_image, self.current_sound = images[index], sounds[index]
            image_changed = True

            # Reset button color to default
            self.button_color = GRAY

            # Add new image to sequence, marking the new turn
            self.sequence.append(self.current_image)

            # Check if the match window just closed in the last turn
            if self.match_window_closed:
                self.total_matches += 1
                self.match_window_closed = False

            # Check if the current turn has enough images for a possible match
            if len(self.sequence) > self.n:
                if self.sequence[-self.n - 1] == self.sequence[-1]:
                    self.match_window_closed = True

            # Ensure a delay between displaying images
            pygame.time.delay(1500)  # Delay to show image and play sound

            # Check if the goal is reached
            if self.correct_matches >= self.goal:
                self.game_over = True

        self.show_end_screen()

if __name__ == "__main__":
    while True:
        game = NBackGame()
        game.run_game()







