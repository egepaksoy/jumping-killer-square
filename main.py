import pygame
from random import randint
import time


pygame.init()

# -------VALUES-------
FPS = 60
WIN_WIDTH = 400
WIN_HEIGHT = 600
CIRCLE_LEN = 50
WALL_WIDTH = 50
WALL_HEIGHT = 300
OFFSET = 100
VELOCITY = 50
GRAVITY = 5
SPEED = -4


# -------COLORS-------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# ---------SOUNDS----------
JUMP = pygame.mixer.Sound("./sounds/jump2.wav")
EXPLOTION = pygame.mixer.Sound("./sounds/explotion2.wav")
MUSIC = pygame.mixer.music.load("./sounds/music.wav")
pygame.mixer.music.play(-1)


WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

def draw(rect_x, rect_y, walls, score):
	label = pygame.font.SysFont(None, 76)
	rect = pygame.Rect(rect_x-CIRCLE_LEN//2, rect_y-CIRCLE_LEN//2, CIRCLE_LEN, CIRCLE_LEN)

	WIN.fill(WHITE)
	if walls:
		for wall in walls:
			wall_rect = pygame.Rect(wall[0], wall[1], WALL_WIDTH, WALL_HEIGHT)
			pygame.draw.rect(WIN, BLACK, wall_rect)

	text = label.render(str(score), True, (0,0,0))
	WIN.blit(text, (WIN_WIDTH//2-len(str(score))*25//2, 20))
	pygame.draw.rect(WIN, BLACK, rect)

	pygame.display.update()


def main():
	clock = pygame.time.Clock()
	rect_x = WIN_WIDTH//2
	rect_y = WIN_HEIGHT//2
	alive = True
	jumped = False
	old_pos = rect_y
	wall_x = WIN_WIDTH+CIRCLE_LEN
	walls = []
	a = 0
	last = 0
	score = 0

	while alive:
		now = pygame.time.get_ticks()
		wall_Y = randint(OFFSET, WIN_HEIGHT-OFFSET)
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				alive = False

			if event.type == pygame.KEYDOWN:
				old_pos = rect_y
				jumped = True


		if jumped:
			rect_y -= 10
			a = 0

		if old_pos-rect_y >= VELOCITY:
			jumped = False

		if jumped == False:
			a += 0.2

		if rect_y + CIRCLE_LEN - 10 >= WIN_HEIGHT:
			EXPLOTION.play()
			time.sleep(1)
			alive = False

		rect_y += a

		if now-last >=2000:
			walls.append([wall_x, wall_Y])
			last = now

		for wall in walls:
			wall[0] += SPEED
			wall_alan = wall[0] + wall[0]+WALL_WIDTH
			if wall[0]+WALL_WIDTH <= 0:
				walls.remove(wall)

			if (wall[0] <= rect_x <= wall[0] + WALL_WIDTH or
				wall[0] <= rect_x + CIRCLE_LEN//2 <= wall[0] + WALL_WIDTH) and (
				wall[1] <= rect_y <= wall[1] + WALL_HEIGHT or
				wall[1] <= rect_y + CIRCLE_LEN//2 <= wall[1] + WALL_WIDTH):
				EXPLOTION.play()
				time.sleep(5)
				alive = False

			if rect_y == wall[1]+WALL_WIDTH:
				score += 1
			if rect_x == wall[0] + WALL_WIDTH:
				score += 1


		draw(rect_x, rect_y, walls, score)

	pygame.quit()


if __name__ == "__main__":
	main()
