import random
from time import sleep
import socket
import pygame
import atexit
import json
import select
import asyncio
import websockets
import websocket
import sys


class CarRacing:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.clientId=0
        self.initialize()
                # Create a socket object
        
        #self.client_socket.bind(('localhost', 3030))
        # Define the server address and port
        server_address = ('localhost', 8888)
        self.ws = websocket.WebSocket()
        self.ws.connect('ws://localhost:8888')
        # Connect to the server


        message2 = 'run'
        self.ws.send('run')
        #asyncio.run(self.async_main())
        ####data = self.client_socket.recv(1024)
        ####int_decoded_data=int(data.decode())
        #####print(int_decoded_data)
        # Convert the received data to coordinates
        #coordinates = json.loads(data)
        #print("x value",coordinates['x'])

        atexit.register(self.disconnect_socket)
        
    async def async_main(self):
        loop = asyncio.get_running_loop()
        await asyncio.gather(self.receive_messages(), loop.run_in_executor(None, blocking_function))
    async def receive_messages():
        uri = "ws://localhost:8888"  # Replace with the WebSocket server URI
        async with websockets.connect(uri) as websocket:
         while True:
            message = await websocket.recv()
            print("Received message:", message)
    def disconnect_socket(self):
        print("Disconnecting from the socket...")
        self.ws.close()
    def initialize(self):

        self.crashed = False

        self.carImg = pygame.image.load('.\\img\\car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car_1 = pygame.image.load('.\\img\\enemy_car_1.png')
        self.enemy_car_1_startx = 0#random.randrange(310, 450)
        self.enemy_car_1_starty = 0#-600
        self.enemy_car_1_speed = 5
        self.enemy_car_1_width = 49
        self.enemy_car_1_height = 100
        self.enemy_car_1_state='run'

        self.enemy_car_2 = pygame.image.load('.\\img\\enemy_car_2.png')
        self.enemy_car_2_startx = random.randrange(310, 450)
        self.enemy_car_2_starty = -600
        self.enemy_car_2_speed = 5
        self.enemy_car_2_width = 49
        self.enemy_car_2_height = 100
        self.enemy_car_2_state='run'

        # Background
        self.bgImg = pygame.image.load(".\\img\\back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        state_json = json.dumps({})
        json_data_3={}
        location_change_flag=False
        x=True
        while x:
            if self.ws.recv():
                data = self.ws.recv()
                print('Received:', data)
                json_data = json.loads(data)
                print(json_data)
                if (json_data['type']=="run"):
                    self.clientId=json_data['client']
                    self.car_x_coordinate=json_data['x']
                    self.car_y_coordinate=json_data['y']
                    x=False
        print("out of the while x")
        
        # readable, writable, exceptional = select.select([self.client_socket], [], [], 0)
        # if self.client_socket in readable:
        data = self.ws.recv()
        json_data = json.loads(data)
        print("json_data",json_data)
        if self.clientId==1:
            print("json_data[0]",json_data[0])
            print("json_data[1][x]",json_data[1]["x"])
            
            self.enemy_car_1_startx=json_data[1]["x"]
            self.enemy_car_1_starty=json_data[1]["y"]
            self.enemy_car_2_startx=json_data[2]["x"]
            self.enemy_car_2_starty=json_data[2]["y"]
        elif self.clientId==2:
            print("json_data[1]",json_data[1])
            self.enemy_car_1_startx=json_data[0]["x"]
            self.enemy_car_1_starty=json_data[0]["y"]
            self.enemy_car_2_startx=json_data[2]["x"]
            self.enemy_car_2_starty=json_data[2]["y"]
        elif self.clientId==3:
            print("json_data[2]",json_data[2])
            self.enemy_car_1_startx=json_data[0]["x"]
            self.enemy_car_1_starty=json_data[0]["y"]
            self.enemy_car_2_startx=json_data[1]["x"]
            self.enemy_car_2_starty=json_data[1]["y"]
        while not self.crashed:
            location_change_flag=False

            r, w, e = select.select([self.ws.sock], [], [], 0)
            if self.ws.sock in r:
                print ("mestanni a receive fe lie 139")
                data = self.ws.recv()
                print('Received in line 139:', data)
                json_data_2 = json.loads(data)
                if self.clientId==1:
                    if json_data_2["type"]=="run":
                        if json_data_2["client"]==2:
                            self.enemy_car_1_startx=json_data_2["x"]
                        elif json_data_2["client"]==3:
                            self.enemy_car_2_startx=json_data_2["x"]
                    elif json_data_2["type"]=="crash":
                        self.remove_enemy()
                        if json_data_2["client"]==2:
                            self.enemy_car_1_state='crashed'
                        elif json_data_2["client"]==3:
                            self.enemy_car_2_state="crashed"
                elif self.clientId==2:
                    if json_data_2["type"]=="run":
                        if json_data_2["client"]==1:
                            self.enemy_car_1_startx=json_data_2["x"]
                        elif json_data_2["client"]==3:
                            self.enemy_car_2_startx=json_data_2["x"]
                    elif json_data_2["type"]=="crash":
                        self.remove_enemy()
                        if json_data_2["client"]==1:
                            self.enemy_car_1_state='crashed'
                        elif json_data_2["client"]==3:
                            self.enemy_car_2_state="crashed"
                elif self.clientId==3:
                    if json_data_2["type"]=="run":
                        if json_data_2["client"]==1:
                            self.enemy_car_1_startx=json_data_2["x"]
                        elif json_data_2["client"]==2:
                            self.enemy_car_2_startx=json_data_2["x"]
                    elif json_data_2["type"]=="crash":
                        self.remove_enemy()
                        if json_data_2["client"]==1:
                            self.enemy_car_1_state='crashed'
                        elif json_data_2["client"]==2:
                            self.enemy_car_2_state="crashed"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                # print(event)

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 50
                        location_change_flag=True
                        state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate }
                        json_data_3 = json.dumps(state_json)
                        #self.ws.send(json_data_3)   
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 50
                        location_change_flag=True
                        state_json={ "client": self.clientId, "type": 'run', "x": self.car_x_coordinate, "y": self.car_y_coordinate }
                        json_data_3 = json.dumps(state_json)
                        #self.ws.send(json_data_3)    
                     
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))

            self.gameDisplay.fill(self.black)
            self.back_ground_raod()
            if self.enemy_car_1_state=='run':
                #print("i will run enemy 1")
                self.run_enemy_car(self.enemy_car_1,self.enemy_car_1_startx, self.enemy_car_1_starty)
            if self.enemy_car_2_state=='run':
                #print("i will run enemy 2")
                self.run_enemy_car(self.enemy_car_2,self.enemy_car_2_startx, self.enemy_car_2_starty)
            
            ####self.enemy_car_1_starty -= self.enemy_car_1_speed

            #if self.enemy_car_1_starty > self.display_height:
            #    self.enemy_car_1_starty = 0 - self.enemy_car_1_height
            #    self.enemy_car_1_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            #print("el mafroud self.car teshtaghal, be x=",self.car_x_coordinate,"we y:",self.car_y_coordinate)
            self.highscore(self.count)
            self.count += 1
            if (self.count % 100 == 0):
                # self.enemy_car_speed += 1
                self.bg_speed += 1
            if self.car_y_coordinate <= self.enemy_car_1_starty + self.enemy_car_1_height:
                if self.car_x_coordinate >= self.enemy_car_1_startx and self.car_x_coordinate <= self.enemy_car_1_startx + self.enemy_car_1_width or self.car_x_coordinate + self.car_width >= self.enemy_car_1_startx and self.car_x_coordinate + self.car_width <= self.enemy_car_1_startx + self.enemy_car_1_width:
                    print("self.car_x_coordinate",self.car_x_coordinate,"self.enemy_car_1_startx",self.enemy_car_1_startx)
                    print("mafrud crash 1")
                    self.crashed = True
                    state_json={ "client": self.clientId, "type": 'crash', "x": self.car_x_coordinate, "y": self.car_y_coordinate }
                    json_data = json.dumps(state_json)
                    self.ws.send(json_data)
                    self.display_message("Game Over !!!")
                    self.disconnect_socket()
                    self.gameDisplay.quit()
                    pygame.quit()
                    break
            if self.car_y_coordinate <= self.enemy_car_2_starty + self.enemy_car_2_height:
                if self.car_x_coordinate >= self.enemy_car_2_startx and self.car_x_coordinate <= self.enemy_car_2_startx + self.enemy_car_2_width or self.car_x_coordinate + self.car_width >= self.enemy_car_2_startx and self.car_x_coordinate + self.car_width <= self.enemy_car_2_startx + self.enemy_car_2_width:
                    print("self.car_x_coordinate",self.car_x_coordinate,"self.enemy_car_1_startx",self.enemy_car_1_startx)
                    print("mafrud crash 2")
                    self.crashed = True
                    state_json={ "client": self.clientId, "type": 'crash', "x": self.car_x_coordinate, "y": self.car_y_coordinate }
                    json_data = json.dumps(state_json)
                    self.ws.send(json_data)
                    self.display_message("Game Over !!!")
                    self.disconnect_socket()
                    self.gameDisplay.quit()
                    pygame.quit()
                    break
                    

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                state_json={ "client": self.clientId, "type": 'crash', "x": self.car_x_coordinate, "y": self.car_y_coordinate }
                json_data = json.dumps(state_json)
                self.ws.send(json_data)
                self.display_message("Game Over !!!")
                self.disconnect_socket()
                self.gameDisplay.quit()
                
                pygame.quit()
                break
            if ((not self.crashed )and location_change_flag):
                self.ws.send(json_data_3) 
            # r, w, e = select.select([self.ws.sock], [], [], 0)
            # if self.ws.sock in r:
            #     print ("mestanni a receive fe lie 170")
            #     data = self.ws.recv()
            #     print('Received in line 170:', data.decode())
            #print("3addet fe line 173")
            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        car_racing.initialize()
        car_racing.racing_window()

    def back_ground_raod(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, car,thingx, thingy):
        self.gameDisplay.blit(car, (thingx, thingy))
    def remove_enemy (self):
        self.gameDisplay.fill((0, 0, 0))

    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()