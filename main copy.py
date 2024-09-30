import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slider Example")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Slider parameters
slider_x = 100
slider_y = 250
slider_width = 600
slider_height = 20
slider_value = 0.5  # Value from 0 to 1
slider_handle_radius = 10

# Function to draw the slider


def draw_slider(screen, x, y, width, value):
    # Draw the slider bar
    pygame.draw.rect(screen, GRAY, (x, y, width, slider_height))

    # Calculate the position of the slider handle
    handle_x = x + value * width

    # Draw the slider handle
    pygame.draw.circle(screen, BLUE, (int(handle_x), y + slider_height // 2), slider_handle_radius)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if mouse is over the slider
                if slider_x <= mouse_x <= slider_x + slider_width and slider_y <= mouse_y <= slider_y + slider_height:
                    # Calculate the slider value based on mouse position
                    slider_value = (mouse_x - slider_x) / slider_width

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Check if left mouse button is held down
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Update slider value based on mouse position
                if slider_x <= mouse_x <= slider_x + slider_width and slider_y <= mouse_y <= slider_y + slider_height:
                    slider_value = (mouse_x - slider_x) / slider_width

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the slider
    draw_slider(screen, slider_x, slider_y, slider_width, slider_value)

    # Display the current slider value
    font = pygame.font.Font(None, 36)
    text = font.render(f"Slider Value: {slider_value:.2f}", True, BLACK)
    screen.blit(text, (slider_x, slider_y + slider_height + 20))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
