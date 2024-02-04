import asyncio, pygame, random, time, pymunk
from elements import elements_NO, elements_NO_simplified

async def main():
    # Backspace
    backspace_held_timer = 0
    backspace_held = False
    pygame.init()

    def draw_text(textstring : str, font : pygame.font.Font, color : pygame.Color, center : tuple):
        text = font.render(textstring, True, color)
        text_rect = text.get_rect(center = center)
        screen.blit(text, text_rect)

    def pick_element(list):
        element = random.choice(list)
        list.remove(element)
        return element

    def drop_confetti():
        global space
        space = pymunk.Space()
        space.gravity = (0, 300)
        global confetti_list
        confetti_list = []
        for n in range(100):
            confetti = Confetti(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()/2))
            confetti_list.append(confetti)
            space.add(confetti.body, confetti.shape)
            confetti.body.apply_impulse_at_local_point((random.randint(0, 250)-125, -400), (0.1, 0))

    class Confetti:
        def __init__(self, start_x, start_y):
            self.body = pymunk.Body()
            self.body.position = (start_x, start_y)
            self.width = 5
            self.height = 5
            self.shape = pymunk.Poly(self.body, [(-self.width, -self.height), (self.width, self.height), (-self.width, self.height), (self.width, -self.height)])
            self.shape.mass = 1
            self.color = random.choice([
                pygame.Color(168, 100, 253),
                pygame.Color(41, 205, 255),
                pygame.Color(125, 255, 68),
                pygame.Color(255, 113, 141),
                pygame.Color(253, 255, 106)
            ])
        
        def draw(self):
            pygame.draw.polygon(screen, self.color, [pos.rotated(self.shape.body.angle) + self.shape.body.position for pos in self.shape.get_vertices()])
            #pygame.draw.lines(screen, self.color, True, [pos.rotated(self.shape.body.angle) + self.shape.body.position for pos in self.shape.get_vertices()])

    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()
    background_color = pygame.Color(35, 35, 48)
    whiteish = pygame.Color(199, 203, 212)
    hint_font = pygame.font.Font("times_new_roman.ttf", round(screen.get_width()/45))
    heading_font = pygame.font.Font("times_new_roman.ttf", round(screen.get_width()/12))
    symbol_font = pygame.font.Font("times_new_roman.ttf", round(screen.get_width()/10))
    paragraph_font = pygame.font.Font("times_new_roman.ttf", round(screen.get_width()/25))
    selection_font = pygame.font.Font("times_new_roman.ttf", round(screen.get_width()/40))
    atomic_number_font = pygame.font.Font("times_new_roman.ttf", round(screen.get_width()/35))

    # Frames per second
    FPS = 60

    # String for tracking input
    input_text = ""

    # Tracking lists
    number_of_correct = 0

    # Tracking if backspace is held
    backspace_held = False

    # Mode tracking
    mode_selector = 0
    mode_selector_animator = 0

    # Game states
    STARTING = True
    INGAME = False
    ENDING = False

    RUNNING = True
    while RUNNING:
        # Check if backspace is held
        if backspace_held and (time.time() - backspace_held_timer) > 0.2:
            input_text = input_text[:-1]

        # Event loop
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                RUNNING = False

            # Keydown
            if event.type == pygame.KEYDOWN:
                # Starting
                if STARTING:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if mode_selector == 0:
                            element_list = elements_NO_simplified.copy()
                            number_of_elements = len(element_list)
                            current_element = pick_element(element_list)
                        elif mode_selector == 1:
                            element_list = elements_NO.copy()
                            number_of_elements = len(element_list)
                            current_element = pick_element(element_list)
                        pygame.mouse.set_cursor() # Reset cursor
                        STARTING = False
                        INGAME = True
                        start_time = time.time()
                        break

                # Mode keys
                if event.key == pygame.K_2:
                    mode_selector = 1
                if event.key == pygame.K_1:
                    mode_selector = 0
                if event.key == pygame.K_TAB:
                    if mode_selector == 1:
                        mode_selector = 0
                    else:
                        mode_selector = 1

                # Backspace
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    backspace_held_timer = time.time()
                    backspace_held = True

                # Word input keys
                if INGAME and event.key != pygame.K_BACKSPACE:
                    input_text += event.unicode

                # INGAME Logic
                if INGAME:
                    # If correct
                    if input_text.upper() == current_element[2].upper():
                        number_of_correct += 1

                        # If done
                        if number_of_correct == number_of_elements:
                            total_time = round(time.time() - start_time, 1)
                            input_text = ""
                            drop_confetti()
                            INGAME = False
                            ENDING = True

                        # If not done
                        else:
                            current_element = pick_element(element_list)
                            input_text = ""
                
                if ENDING:
                    # Restart
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        number_of_correct = 0
                        ENDING = False
                        STARTING = True
            
            # Keyup
            if event.type == pygame.KEYUP:
                # Backspace
                if event.key == pygame.K_BACKSPACE:
                    backspace_held = False

            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if outer_selection_box.collidepoint(mouse_pos):
                    if mode_selector == 1:
                        mode_selector = 0
                    else:
                        mode_selector = 1
            
        screen.fill(background_color)

        if STARTING:
            # Draw heading text
            heading_text = heading_font.render("Grunnstofftreneren", True, whiteish)
            heading_rect = heading_text.get_rect(center = (screen.get_width()/2, screen.get_height()/4))
            screen.blit(heading_text, heading_rect)

            # Heading underline
            pygame.draw.line(screen, whiteish, (heading_rect.x, heading_rect.y + heading_rect.height), (heading_rect.x + heading_rect.width, heading_rect.y + heading_rect.height))

            # Selection text
            draw_text("Et lite utvalg", selection_font, whiteish, (screen.get_width()/2 - screen.get_width()/6, 55*screen.get_height()/100))
            draw_text("       Alle grunnstoffer", selection_font, whiteish,(screen.get_width()/2 + screen.get_width()/6, 55*screen.get_height()/100))

            # Outer selection box
            outer_selection_box = pygame.rect.Rect(0, 0, screen.get_width()/15, round(screen.get_width()/40))
            outer_selection_box.center = (screen.get_width()/2, 55*screen.get_height()/100)
            pygame.draw.rect(screen, whiteish, outer_selection_box, width=2, border_radius=8)

            # Inner selection box
            if round((mode_selector - mode_selector_animator), 1) > 0:
                mode_selector_animator += 0.1
            elif round((mode_selector - mode_selector_animator), 1) < 0:
                mode_selector_animator -= 0.1
            inner_selection_box = pygame.rect.Rect(outer_selection_box.x + mode_selector_animator*outer_selection_box.width/2, outer_selection_box.y, screen.get_width()/30, round(screen.get_width()/40))
            pygame.draw.rect(screen, whiteish, inner_selection_box, border_radius=8)

            # Draw hint
            draw_text("Trykk på RETURN eller SPACE for å starte.", hint_font, whiteish, (screen.get_width()/2, 95*screen.get_height()/100))

            # Cursor changing
            mouse_pos = pygame.mouse.get_pos()
            if outer_selection_box.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor()

        elif INGAME:
            # Draw progress bar
            progress_bar_outer_rect = pygame.Rect(0, 0, screen.get_width()/2, screen.get_height()/100)
            progress_bar_outer_rect.center = (screen.get_width()/2, 0 + progress_bar_outer_rect.height)
            progress_bar_inner_rect = pygame.Rect(screen.get_width()/2 - progress_bar_outer_rect.width/2, progress_bar_outer_rect.height/2, (number_of_correct/number_of_elements) * progress_bar_outer_rect.width, screen.get_height()/100)
            pygame.draw.rect(screen, whiteish, progress_bar_outer_rect, width = 1, border_radius = 3)
            pygame.draw.rect(screen, whiteish, progress_bar_inner_rect, border_radius = 3)

            # Draw element name
            symbol = symbol_font.render(current_element[1], True, whiteish)
            symbol_rect = symbol.get_rect(center = (screen.get_width()/2, screen.get_height()/3))
            screen.blit(symbol, symbol_rect)

            # Draw border for element
            margin = 2*round(screen.get_width()/35)
            pygame.draw.lines(screen, whiteish, True, [(symbol_rect.x - margin, symbol_rect.y - margin), (symbol_rect.x + symbol_rect.width + margin, symbol_rect.y - margin), (symbol_rect.x + symbol_rect.width + margin, symbol_rect.y + symbol_rect.height + margin), (symbol_rect.x - margin, symbol_rect.y + symbol_rect.height + margin)])

            # Draw element atomic number
            draw_text(str(current_element[0]), atomic_number_font, whiteish, (symbol_rect.x - margin + round(screen.get_width()/35) , symbol_rect.y - margin + round(screen.get_width()/35)))

            # Draw current word
            draw_text(input_text.upper(), paragraph_font, whiteish, (screen.get_width()/2, 2*screen.get_height()/3))

            # Draw text line
            pygame.draw.line(screen, whiteish, (screen.get_width()/3, 2*screen.get_height()/3 + paragraph_font.get_height()/2), (2*screen.get_width()/3, 2*screen.get_height()/3 + paragraph_font.get_height()/2))

            
        if ENDING:
            # Ending text
            draw_text("Du klarte alle grunnstoffene!", paragraph_font, whiteish, (screen.get_width()/2, 40*screen.get_height()/100))

            # Ending time
            draw_text(f"{str(total_time)} s", hint_font, whiteish, (screen.get_width()/2, 60*screen.get_height()/100))

            # Ending hint
            draw_text("Trykk på RETURN eller SPACE for å starte om igjen.", hint_font, whiteish, (screen.get_width()/2, 95*screen.get_height()/100))

            # Pymunk physics for confetti
            for x in confetti_list:
                x.draw()
                x.body.apply_force_at_local_point((0, random.randint(0, 300))) # Wind?
            space.step(1/FPS)

        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)

asyncio.run(main())