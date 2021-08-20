import arcade

#Step 1
#Physics
MOVEMENT_SPEED = 3
JUMP_SPEED = 12
GRAVITY = 1.0

#Step 2
#Map
MAP_WIDTH = 100*48  #There are 1000 tiles horizontally in the map, each of length 48 pixels
MAP_HEIGHT = 20*48 #There are 20 tiles vertically in the map,each of length 48 pixels
TILE_WIDTH = 48    #Each tile in our map is of the dimensions 32x32

#Step 3
#Window
WINDOW_HEIGHT = 675
WINDOW_WIDTH = 1200
WINDOW_HALF_WIDTH = WINDOW_WIDTH // 2

class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width,height, title)
        self.set_location(100,100)

        arcade.set_background_color(arcade.color.BLACK)

        #Step 4
        self.ground_list = None
        self.player_list = None
        self.coin_list = None
        self.player = None
        self.physics_engine = None
        self.collected_coins = 0
        self.chances = 3
        self.background = None
        self.setup()

    def setup(self):

        #Adding Display Features
        self.heart = arcade.Sprite("images/heart pixel art 254x254.png", center_x=9, center_y=9)
        self.coin = arcade.Sprite("images/Coin_01.png", center_x=9, center_y=9)

        #Step 5 - Adding Map Layers
        my_map = arcade.tilemap.read_tmx("myMap.tmx")
        self.ground_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="ground", scaling=1)
        self.coin_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="coin", scaling=1)
        self.background2_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="background2", scaling=1)
        self.ladder_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="ladder", scaling=1)
        self.death_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="death", scaling=1)
        self.background_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="background", scaling=1)

        #Step 6 - Adding Background
        self.background = arcade.Sprite("images/background.jpeg")
        self.background.center_x = 600
        self.background.center_y = 337
        self.background.set_position(arcade.get_viewport()[0]+600,arcade.get_viewport()[3]-337)
        self.background.scale = 1


        #Step 7 - Adding Player
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()
        self.player.center_x = 15.6
        self.player.center_y = 24
        self.player.scale = 1.5
        self.player.set_position(10, 500)

        # Step 8.1 - Adding Player Textures
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("images/Biker/Biker_idle.png"))

        # Step 8.2 - Adding Player Textures
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("images/Biker/Biker_idle.png", mirrored=True))

        # Step 8.3 - Adding Player Textures
        self.player.texture = arcade.load_texture("images/Biker/Biker_idle.png")

        # Step 8.4 - Adding Player Textures
        self.player.walk_right_textures = []
        for i in range(6):
            self.player.walk_right_textures.append(arcade.load_texture("images/Biker/Biker_run.png", x=i*48, y=0, width=48, height=48))


        # Step 8.5 - Adding Player Textures
        self.player.walk_left_textures = []
        for i in range(6):
            self.player.walk_left_textures.append(arcade.load_texture("images/Biker/Biker_run.png", x=i*48, y=0, width=48, height=48, mirrored=True))


        #Step 9
        self.player_list.append(self.player)

        #Step 10 - Using this function, we make the physics engine. In the first argument we give the sprite which will interact
        #with the layer of the map. If we have multiple players/interactable sprites, we will have to call this function multiple times
        #The Gravity constant is a float. The higher its value the more the gravity intensity will be. It will also make our Avatar come down
        #faster and harder
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground_list,gravity_constant=GRAVITY)
        self.physics_engine.ladders = self.ladder_list

    def check_fall(self):
        if self.player.center_y <0:
            self.player.set_position(10, 500)
            arcade.set_viewport(0,120,0,675)
            self.chances-=1

        spikes = arcade.check_for_collision_with_list(self.player, self.death_list)
        if len(spikes) > 0:
            self.player.set_position(10, 500)
            arcade.set_viewport(0, 1200, 0, 675)
            self.chances -= 1

    def on_draw(self):
        arcade.start_render()

        #Step 11
        self.background.draw()

        if self.chances > 0:
            self.background_list.draw()
            self.background2_list.draw()
            self.ground_list.draw()
            self.death_list.draw()
            self.ladder_list.draw()
            self.coin_list.draw()
            self.player_list.draw()

            # Step 12
            # Observe the arcade.viewport() function. It returns a tuple of 4 elements. (left, right, bottom, top) where left is at the 0th index
            # right is at index 1 and can be accessed by arcade.viewport()[1] and so on so forth.
            # Drawing an element at (x,y) = (arcade.viewport()[0],arcade.viewport()[2]) will put it at the bottom left of the screen.
            self.coin.set_position(arcade.get_viewport()[0] + 10, arcade.get_viewport()[3] - 28)
            self.heart.set_position(arcade.get_viewport()[0] + 10, arcade.get_viewport()[3] - 52)
            self.coin.draw()
            self.heart.draw()
            arcade.draw_text(f"{self.collected_coins}", arcade.get_viewport()[0] + 30, arcade.get_viewport()[3] - 43,
                             arcade.color.GOLD, font_size=20)
            arcade.draw_text(f"{self.chances}", arcade.get_viewport()[0] + 30, arcade.get_viewport()[3] - 67,
                             arcade.color.RED, font_size=20)

        else:
            #quit()
            arcade.draw_text("GAME OVER", 220,537,arcade.color.BLACK, font_size=70)
            arcade.draw_text("(Press Space to try again)", 370, 527, arcade.color.BLACK, font_size=15)


    #Step 13
    #This is the clamp function. We will use it to make the game map stop moving forward once our avatar reaches the edges of a map.
    #How it works is, this function will take 3 parameters, value will be the current position of the avatar. mini will be the minimum
    #position of the map i.e. 0 and maxi will be equal to the last value to which our avatar can move.
    #First the clamp function will compare the maximum value with the current position and return the smaller of the two
    #Then it will compare the minimum value with the current position and return the largest of the two
    #later we will equate the returned value with the center_x of our avatar.
    #In other words, our Avatar's x position will never be smaller than mini and never be larger than maxi
    def clamp(self, value, mini, maxi):
        return max(min(value, maxi), mini)

    def on_update(self, delta_time: float):

        self.check_fall()

        #Step 14
        #It is important to constantly update our physics engine
        self.physics_engine.update()
        self.player.center_x = self.clamp(self.player.center_x, 0, MAP_WIDTH)
        self.background.set_position(arcade.get_viewport()[0] + 600, arcade.get_viewport()[3] - 337)
        #Step 15
        #This conditional statement is responsible for changing the view i.e. making the map move alongside the player
        if self.player.center_x > WINDOW_HALF_WIDTH and self.player.center_x < MAP_WIDTH - TILE_WIDTH - WINDOW_HALF_WIDTH:
            #Change_View is a boolean type variable
            change_view = True
        else:
            change_view = False

        #Step 16
        #This step works in coalition with Step 15. If change_view is true, we will set arcade.viewport with accordance to the avatar's
        #Current position.
        #This conditional is setting the viewport for horizontal movements only, if you observe the last two indexes, i.e. bottom and top
        #They are constant values. Whereas the left and right of the viewports are being constantly calculated as functions of the avatars
        #current position.
        if change_view:
            arcade.set_viewport(self.player.center_x - WINDOW_HALF_WIDTH, self.player.center_x + WINDOW_HALF_WIDTH, 0, WINDOW_HEIGHT)

        #Step 17. The following lines of code are to detect collisions with coins and increment the coin collected count. Here coin == box

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            self.collected_coins+=1
            #Coin.kill() removes the coin from the sprite list. this command is an alias for remove_from_sprite_list
            coin.kill()

        #Step 18. Your program will return an error if you don't update player list and animations
        self.player_list.update()
        self.player_list.update_animation()

    def reset(self):
        self.collected_coins = 0
        self.chances = 3
        self.coin_list = arcade.tilemap.process_layer(map_object=my_map, layer_name="coin", scaling=1)

    #Step 19
    #You can make the player go faster or slower by increasing or decreasing movement speed. Though don't make it too fast
    #Or else the game will start glitching
    #You can also make the player jump higher by increasing the JUMP_SPEED
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        if symbol == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        if symbol == arcade.key.UP:
            #The can_jump() function automatically takes care of a lot of things for us. Like detecting surfaces on top etc.
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED

    #Step 20
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player.change_x = 0
        if symbol == arcade.key.SPACE and self.chances<1:
            self.reset()

MyGameWindow(WINDOW_WIDTH,WINDOW_HEIGHT, 'Medival Treasure Hunt')
arcade.run()