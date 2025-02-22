import pygame
from pygame import Surface
from pygame.event import Event as PygameEvent
from src.pygapp.to_refactor.bases import BasicInputManagement
from src.pygapp.to_refactor.buttons import Button
from src.pygapp.utils import graphics as grp


# provides a simple structure for a menu. The Main Menu directly uses it
class MenuInterface_A(BasicInputManagement):
	link: str  # this is the link to this interface
	
	def __init__(self, screen: Surface, direct: str, buttons: [Button], e_coo: {int: (int, int, int)}, eff: [Surface]):
		super().__init__(buttons)
		self.screen = screen  # screen surface
		self.name = direct.split("/")[-1][:-4]  # the name of the menu (extracted from its directory)
		self.menu_image = grp.load_image(direct)  # image of the menu's background (loaded based on its name)
		self.navigation_image = grp.load_image(f"menu/interfaces/navigation/navigation.png")  # img with info about menu
		self.info_images = [grp.load_image(f"menu/info/info_{self.name}/{i + 1}.png") for i, _ in enumerate(buttons)]
		self.effect = eff  # list of effects to be used for evidencing the buttons
		self.active_code = 0  # index of the active button
		self.current_frame = 0  # frame representing the current state of the button's evidencing effect
		self.effect_coo = e_coo  # coordinates where the effects will be displayed
		self.coord_effect: (int, int) = (0, 0)  # coordinates of the effect currently at use
		self.update_coord_effect()
	
	@staticmethod
	def display_interface(screen) -> str:
		pass
	
	def draw_buttons(self) -> None:
		for i, button in enumerate(self.button_list):  # draw all the buttons
			button.draw(self.screen, self.active_code == i)  # the active button is drawn with surrounding effect
		self.button_list[self.active_code].draw_info(self.screen)  # displays information about current active button
		self.current_frame = (self.current_frame + 0.25) % 3  # update frame in a way that it restarts at a value of 3
	
	def update_coord_effect(self) -> None:
		self.coord_effect = self.button_list[self.active_code].x - 12, self.button_list[self.active_code].y - 12
	
	def get_effect_by_input(self, event: PygameEvent = None) -> str:
		effect = super().get_effect_by_input(event)
		return effect
	
	def start(self) -> str:
		background = Surface(self.screen.get_size())
		background.convert().fill((0, 0, 0))
		while True:
			self.clock.tick(30)
			# effect carries information about what to do based on input. None is base case and means "do nothing"
			effect = self.manage_events()  # taking and evaluating input
			if effect != "":  # if meaningful input is given take respective action
				return effect
			if not self.already_checked_cursor:  # saves time avoiding iterating over buttons when it was done already
				self.cursor_is_on_button()  # mouse visual interaction with interface
			self.refresh(background)
	
	def manage_buttons(self, event: PygameEvent) -> str:
		new_active_code = self.active_code  # go up if value is -1 and down if it's 1
		if event.key == pygame.K_UP:
			new_active_code -= 1
		elif event.key == pygame.K_DOWN:
			new_active_code += 1
		elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
			return self.enter_action()
		new_active_code = new_active_code % len(self.button_list)  # make sure active_code doesn't go off-boundaries
		self.set_button_to_active(new_active_code)
	
	def refresh(self, background: Surface):
		self.screen.blit(background, (0, 0))
		self.screen.blit(self.menu_image, (305, 0))
		self.screen.blit(self.navigation_image, (355, 620))
		self.draw_buttons()
		self.screen.blit(self.info_images[self.active_code], (786, 195))
		pygame.display.update()
