import pygame

def draw_text(screen, text = "some text", pos = (100, 100), size = 10, color = (255, 255, 255), font_type = None):
	text = str(text)
	# font = pygame.font.Font(font_type, size)
	font = pygame.font.SysFont('Times New Roman', size)
	textSurf = font.render(text, True, color)
	textRect = textSurf.get_rect()
	textRect.center = pos
	screen.blit(textSurf, textRect)

def draw_vehicle(screen, pos, color, size, v):
	pygame.draw.circle(screen, color, pos, size)
	text_color = (255, 0, 0)
	draw_text(screen, str(v), pos, 20, text_color)

def draw_card(screen, color, pos = (100, 100), size = (40, 40), v = 10):
	rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
	rect.center = pos
	pygame.draw.rect(screen, color, rect)
	draw_text(screen, str(v), pos, 20)

def draw_simulate(cards, vehicles, solution):
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		# draw solution
		for s in solution:
			color = (128, 128, 0)
			icard = int(s[0])
			ivehicle = int(s[1])
			pos1 = (int(cards[icard][0]), int(cards[icard][1]))
			pos2 = (int(vehicles[ivehicle][0]), int(vehicles[ivehicle][1]))
			pygame.draw.line(screen, color, pos1, pos2, 3)

		# draw cards
		for card in cards:
			pickup_color = (0, 128,255)
			delivery_color = (200, 128,255)
			line_color = (100, 100, 100)
			pickup_pos = (int(card[0]), int(card[1]))
			delivery_pos = (int(card[2]), int(card[3]))
			v = int(card[4])
			pygame.draw.line(screen, line_color, pickup_pos, delivery_pos, 2)	
			draw_card(screen, pickup_color, pickup_pos, (30, 30), v)
			draw_card(screen, delivery_color, delivery_pos, (30, 30), v)

		# draw vehicles
		for vehicle in vehicles:
			color = (0, 255, 0)
			pos = (int(vehicle[0]), int(vehicle[1]))
			v = int(vehicle[2])
			draw_vehicle(screen, pos, color, 15, v)

		pygame.display.flip()