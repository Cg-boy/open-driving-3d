#Welcome to Open-Driving-3D 0.07!
#
#This is still an early version, so don't expect too much.
#Have Fun!
#
from panda3d.core import loadPrcFileData

loadPrcFileData("", "win-size 1200 600")
loadPrcFileData("", "audio-libary-name p3openal-audio")
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletVehicle
from panda3d.core import Vec3
from panda3d.core import Point3
from panda3d.bullet import ZUp
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from panda3d.core import Fog
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight
from panda3d.core import VBase4
from panda3d.core import NodePath
from panda3d.core import Spotlight
from panda3d.core import PerspectiveLens
from direct.gui.OnscreenText import OnscreenText
import sys



class Drive(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		
		#Setup
		scene = BulletWorld()
		scene.setGravity(Vec3(0, 0, -9.81))
		base.setBackgroundColor(0.6,0.9,0.9)
		fog = Fog("The Fog")
		fog.setColor(0.9,0.9,1.0)
		fog.setExpDensity(0.003)
		render.setFog(fog)
		#Lighting
		
		#Sun light
		sun = DirectionalLight("The Sun")
		sun_np = render.attachNewNode(sun)
		sun_np.setHpr(0,-60,0)
		render.setLight(sun_np)
		
		#Ambient light
		amb = AmbientLight("The Ambient Light")
		amb.setColor(VBase4(0.39,0.39,0.39, 1))
		amb_np = render.attachNewNode(amb)
		render.setLight(amb_np)
		
		#Variables
		self.gear = 0
		
		self.start = 0
		
		self.Pbrake = 0
		
		self.terrain_var = 1
		
		self.time = 0
		
		self.headlight_var = 0
		
		self.RPM = 0
		
		self.clutch = 0
		
		self.carmaxspeed = 100 #KPH
		
		self.carmaxreversespeed = -40 #KPH
		
		self.steering = 0
		
		
		#Functions
		def V1():
			camera.setPos(0.25,-1.2,0.5)
			camera.setHpr(0,-13,0)
			
		def V2():
			camera.setPos(0,-15,3)
			camera.setHpr(0,-10,0)
			
		def V3():
			camera.setPos(0,0,9)
			camera.setHpr(0,-90,0)
			
		def up():
			self.gear = self.gear -1
			if self.gear < -1:
				self.gear = -1
				
		def down():
			self.gear = self.gear +1
			if self.gear > 1:
				self.gear = 1
				
		def start_function():
			self.start = 1
			self.start_sound.play()
			self.engine_idle_sound.play()
			self.RPM = 1000
			
		def stop_function():
			self.start = 0
			self.engine_idle_sound.stop()
				
		def parkingbrake():
			self.Pbrake = (self.Pbrake + 1) % 2
			
		def rotate():
			Car_np.setHpr(0, 0, 0)
			
		def horn():
			self.horn_sound.play()
			
		def set_time():
			if self.time == -1:
				sun.setColor(VBase4(0.4, 0.3, 0.3, 1))
				base.setBackgroundColor(0.8,0.7,0.7)
			if self.time == 0:
				sun.setColor(VBase4(0.7, 0.7, 0.7, 1))
				base.setBackgroundColor(0.6,0.9,0.9)
			if self.time == 1:
				sun.setColor(VBase4(0.2, 0.2, 0.2, 1))
				base.setBackgroundColor(0.55,0.5,0.5)
			if self.time == 2:
				sun.setColor(VBase4(0.02, 0.02, 0.05, 1))
				base.setBackgroundColor(0.3,0.3,0.3)
				
			if self.time == -2:
				self.time = -1
			if self.time == 3:
				self.time = 2
			
		def time_forward():
			self.time = self.time + 1
			
		def time_backward():
			self.time = self.time -1
			
		def set_terrain():
			if self.terrain_var == 1:
				self.ground_model.setTexture(self.ground_tex, 1)
				self.ground_model.setScale(3)
			if self.terrain_var == 2:
				self.ground_model.setTexture(self.ground_tex2, 1)
				self.ground_model.setScale(3)
			if self.terrain_var == 3:
				self.ground_model.setTexture(self.ground_tex3, 1)
				self.ground_model.setScale(4)
				
			if self.terrain_var == 4:
				self.terrain_var = 1
			if self.terrain_var == 0:
				self.terrain_var = 3
			
		def next_terrain():
			self.terrain_var = self.terrain_var + 1
			
		def previous_terrain():
			self.terrain_var = self.terrain_var - 1
			
		def show_menu():
			self.menu_win.show()
			self.a1.show()
			self.a2.show()
			self.a3.show()
			self.a4.show()
			self.t1.show()
			self.t2.show()
			self.ok.show()
			self.exit_button.show()
			
		def hide_menu():
			self.menu_win.hide()
			self.a1.hide()
			self.a2.hide()
			self.a3.hide()
			self.a4.hide()
			self.ok.hide()
			self.t1.hide()
			self.t2.hide()
			self.exit_button.hide()
		
		def Menu():
			self.menu_win = OnscreenImage(image = "Textures/menu.png", pos = (0.9,0,0), scale = (0.5))
			self.menu_win.setTransparency(TransparencyAttrib.MAlpha)
			
			#The Arrow Buttons
			self.a1 = DirectButton(text = "<", scale = 0.2, pos = (0.55,0,0.25), command = previous_terrain)
			self.a2 = DirectButton(text = ">", scale = 0.2, pos = (1.15,0,0.25), command = next_terrain)
			self.a3 = DirectButton(text = "<", scale = 0.2, pos = (0.55,0,0.0), command = time_backward)
			self.a4 = DirectButton(text = ">", scale = 0.2, pos = (1.15,0,0.0), command = time_forward)
			
			#The Text
			self.t1 = OnscreenText(text = "Terrain", pos = (0.85,0.25,0), scale = 0.1, fg = (0.4,0.4,0.5,1))
			self.t2 = OnscreenText(text = "Time", pos = (0.85,0,0), scale = 0.1, fg = (0.4,0.4,0.5,1))
			
			#The Buttons
			self.ok = DirectButton(text = "Okay", scale = 0.11, pos = (0.87,0,-0.25), command = hide_menu)
			self.exit_button = DirectButton(text = "Quit", scale = 0.11, pos = (0.87,0,-0.42), command = sys.exit)
			
		Menu()
		
		
		def take_screenshot():
			base.screenshot("Screenshot")
			
		def set_headlights():
			if self.headlight_var == 1:
				Headlight1.setColor(VBase4(9.0,8.9,8.9,1))
				Headlight2.setColor(VBase4(9.0,8.9,8.9,1))
			if self.headlight_var == 0:
				Headlight1.setColor(VBase4(0,0,0,1))
				Headlight2.setColor(VBase4(0,0,0,1))
			
		def headlights():
			self.headlight_var = (self.headlight_var + 1) % 2
			
		def update_rpm():
			
			#Simulate RPM
			if self.start == 1:
				if self.gear == 0:
					self.RPM = self.RPM - self.RPM / 400
				else:
					self.RPM = self.RPM + self.carspeed / 9
					self.RPM = self.RPM - self.RPM / 200
			
			#Reset RPM to 0 when engine is off
			if self.start == 0:
				if self.RPM > 0.0:
					self.RPM = self.RPM - 40
				if self.RPM < 10:
					self.RPM = 0.0
								
			#Idle RPM power
			if self.start == 1:
				if self.RPM < 650:
					self.RPM = self.RPM + 4
				if self.RPM < 600:
					self.clutch = 1
				else:
					self.clutch = 0
					
			#RPM limit		
			if self.RPM > 6000:
				self.RPM = 6000
				

		#Controls 
		inputState.watchWithModifiers("F", "arrow_up")
		inputState.watchWithModifiers("B", "arrow_down")
		inputState.watchWithModifiers("L", "arrow_left")
		inputState.watchWithModifiers("R", "arrow_right")
		
		do = DirectObject()
		
		do.accept("escape", show_menu)
		do.accept("1", V1)
		do.accept("2", V2)
		do.accept("3", V3)
		do.accept("page_up", up)
		do.accept("page_down", down)
		do.accept("x-repeat", start_function)
		do.accept("x", stop_function)
		do.accept("p", parkingbrake)
		do.accept("backspace", rotate)
		do.accept("enter", horn)
		do.accept("f12", take_screenshot)
		do.accept("h", headlights)
		
		#The ground
		self.ground = BulletPlaneShape(Vec3(0, 0, 1,), 1)
		self.ground_node = BulletRigidBodyNode("The ground")
		self.ground_node.addShape(self.ground)
		self.ground_np = render.attachNewNode(self.ground_node)
		self.ground_np.setPos(0, 0, -2)
		scene.attachRigidBody(self.ground_node)
		
		self.ground_model = loader.loadModel("Models/plane.egg")
		self.ground_model.reparentTo(render)
		self.ground_model.setPos(0,0,-1)
		self.ground_model.setScale(3)
		self.ground_tex = loader.loadTexture("Textures/ground.png")
		self.ground_tex2 = loader.loadTexture("Textures/ground2.png")
		self.ground_tex3 = loader.loadTexture("Textures/ground3.png")
		self.ground_model.setTexture(self.ground_tex, 1)
		
		#The car
		Car_shape = BulletBoxShape(Vec3(1, 2.0, 1.0))
		Car_node = BulletRigidBodyNode("The Car")
		Car_node.setMass(1200.0)
		Car_node.addShape(Car_shape)
		Car_np = render.attachNewNode(Car_node)
		Car_np.setPos(0,0,3)
		Car_np.setHpr(0,0,0)
		Car_np.node().setDeactivationEnabled(False)
		scene.attachRigidBody(Car_node)
		
		Car_model = loader.loadModel("Models/Car.egg")
		Car_model.reparentTo(Car_np)
		Car_tex = loader.loadTexture("Textures/Car1.png")
		Car_model.setTexture(Car_tex, 1)
		
		self.Car_sim = BulletVehicle(scene, Car_np.node())
		self.Car_sim.setCoordinateSystem(ZUp)
		scene.attachVehicle(self.Car_sim)
		
		#The inside of the car
		Car_int = loader.loadModel("Models/inside.egg")
		Car_int.reparentTo(Car_np)
		Car_int_tex = loader.loadTexture("Textures/inside.png")
		Car_int.setTexture(Car_int_tex, 1)
		Car_int.setTransparency(TransparencyAttrib.MAlpha)
		
		#The steering wheel
		Sw = loader.loadModel("Models/Steering wheel.egg")
		Sw.reparentTo(Car_np)
		Sw.setPos(0.25,0,-0.025)
		
		#The first headlight
		Headlight1 = Spotlight("Headlight1")
		lens = PerspectiveLens()
		lens.setFov(180)
		Headlight1.setLens(lens)
		Headlight1np = render.attachNewNode(Headlight1)
		Headlight1np.reparentTo(Car_np)
		Headlight1np.setPos(-0.8,2.5,-0.5)
		Headlight1np.setP(-15)
		render.setLight(Headlight1np)
		
		#The second headlight
		Headlight2 = Spotlight("Headlight2")
		Headlight2.setLens(lens)
		Headlight2np = render.attachNewNode(Headlight2)
		Headlight2np.reparentTo(Car_np)
		Headlight2np.setPos(0.8,2.5,-0.5)
		Headlight2np.setP(-15)
		render.setLight(Headlight2np)
		
		#Sounds
		self.horn_sound = loader.loadSfx("Sounds/horn.ogg")
		self.start_sound = loader.loadSfx("Sounds/enginestart.ogg")
		self.engine_idle_sound = loader.loadSfx("Sounds/engineidle.ogg")
		self.engine_idle_sound.setLoop(True)
		self.accelerate_sound = loader.loadSfx("Sounds/enginethrottle.ogg")
				
		#Camera
		base.disableMouse()
		camera.reparentTo(Car_np)
		camera.setPos(0,-15,3)
		camera.setHpr(0,-10,0)
		
		#Wheel function
		def Wheel(pos, np, r, f):
			w = self.Car_sim.createWheel()
			w.setNode(np.node())
			w.setChassisConnectionPointCs(pos)
			w.setFrontWheel(f)
			w.setWheelDirectionCs(Vec3(0, 0, -1))
			w.setWheelAxleCs(Vec3(1, 0, 0))
			w.setWheelRadius(r)
			w.setMaxSuspensionTravelCm(40)
			w.setSuspensionStiffness(120)
			w.setWheelsDampingRelaxation(2.3)
			w.setWheelsDampingCompression(4.4)
			w.setFrictionSlip(50)
			w.setRollInfluence(0.1)
		
		#Wheels	
		w1_np = loader.loadModel("Models/Lwheel")
		w1_np.reparentTo(render)
		w1_np.setColorScale(0,6)
		Wheel(Point3(-1,1,-0.6), w1_np, 0.4, False)
		
		w2_np = loader.loadModel("Models/Rwheel")
		w2_np.reparentTo(render)
		w2_np.setColorScale(0,6)
		Wheel(Point3(-1.1,-1.2,-0.6), w2_np, 0.4, True)
		
		w3_np = loader.loadModel("Models/Lwheel")
		w3_np.reparentTo(render)
		w3_np.setColorScale(0,6)
		Wheel(Point3(1.1,-1,-0.6), w3_np, 0.4, True)
		
		w4_np = loader.loadModel("Models/Rwheel")
		w4_np.reparentTo(render)
		w4_np.setColorScale(0,6)
		Wheel(Point3(1,1,-0.6), w4_np, 0.4, False)
		

		
		#The engine and steering
		def processInput(dt):
			
			#Vehicle properties
			self.steeringClamp = 35.0
			self.steeringIncrement = 70
			engineForce = 0.0
			brakeForce = 0.0
			
			
			#Get the vehicle's current speed
			self.carspeed = self.Car_sim.getCurrentSpeedKmHour()
			
			
			#Engage clutch when in gear 0
			if self.gear == 0:
				self.clutch = 1
			
			
			#Slow the steering when at higher speeds
			self.steeringIncrement = self.steeringIncrement - self.carspeed / 1.5
			
			
			#Reset the steering
			if not inputState.isSet("L") and not inputState.isSet("R"):
				
				if self.steering < 0.00:
					self.steering = self.steering + 0.6
				if self.steering > 0.00:
					self.steering = self.steering - 0.6
					
				if self.steering < 1.0 and self.steering > -1.0:
					self.steering = 0
			
			
			#Slow the car down while it's moving
			if self.clutch == 0:
				brakeForce = brakeForce + self.carspeed / 5
			else:
				brakeForce = brakeForce + self.carspeed / 15
		
			
			#Forward
			if self.start == 1:
				if inputState.isSet("F"):
					self.RPM = self.RPM + 35
					self.accelerate_sound.play()
				if self.clutch == 0:
					
					if self.gear == -1:
						if self.carspeed > self.carmaxreversespeed:	
							engineForce = -self.RPM / 3
							
					if self.gear == 1:
						if self.carspeed < self.carmaxspeed:
							engineForce = self.RPM / 1

			
			#Brake	
			if inputState.isSet("B"):
				engineForce = 0.0
				brakeForce = 12.0
				if self.gear != 0 and self.clutch == 0:
					self.RPM = self.RPM - 20
				
			#Left	
			if inputState.isSet("L"):
				if self.steering < 0.0:
					#This makes the steering reset at the correct speed when turning from right to left
					self.steering += dt * self.steeringIncrement + 0.6
					self.steering = min(self.steering, self.steeringClamp)
				else:
					#Normal steering
					self.steering += dt * self.steeringIncrement
					self.steering = min(self.steering, self.steeringClamp)
			
			#Right	
			if inputState.isSet("R"):
				if self.steering > 0.0:
					#This makes the steering reset at the correct speed when turning from left to right
					self.steering -= dt * self.steeringIncrement + 0.6
					self.steering = max(self.steering, -self.steeringClamp)
				else:
					#Normal steering
					self.steering -= dt * self.steeringIncrement
					self.steering = max(self.steering, -self.steeringClamp)
			
			#Park
			if self.Pbrake == 1:
				brakeForce = 10.0
				if self.gear != 0 and self. clutch == 0:
					self.RPM = self.RPM - 20
				
				
			#Apply forces to wheels	
			self.Car_sim.applyEngineForce(engineForce, 0);
			self.Car_sim.applyEngineForce(engineForce, 3);
			self.Car_sim.setBrake(brakeForce, 1);
			self.Car_sim.setBrake(brakeForce, 2);
			self.Car_sim.setSteeringValue(self.steering, 0);
			self.Car_sim.setSteeringValue(self.steering, 3);
			
			#Steering wheel
			Sw.setHpr(0,0,-self.steering*10)
		
		
		#The HUD
		self.gear_hud = OnscreenImage(image = "Textures/gear_hud.png", pos = (-1,0,-0.85), scale = (0.2))
		self.gear_hud.setTransparency(TransparencyAttrib.MAlpha)
		
		self.gear2_hud = OnscreenImage(image = "Textures/gear2_hud.png", pos = (-1,0,-0.85), scale = (0.2))
		self.gear2_hud.setTransparency(TransparencyAttrib.MAlpha)
		
		self.starter = OnscreenImage(image = "Textures/starter.png", pos = (-1.2,0,-0.85), scale = (0.15))
		self.starter.setTransparency(TransparencyAttrib.MAlpha)
		
		self.park = OnscreenImage(image = "Textures/pbrake.png", pos = (-0.8,0,-0.85), scale = (0.1))
		self.park.setTransparency(TransparencyAttrib.MAlpha)
		
		self.rev_counter = OnscreenImage(image = "Textures/dial.png", pos = (-1.6, 0.0, -0.70), scale = (0.6,0.6,0.4))
		self.rev_counter.setTransparency(TransparencyAttrib.MAlpha)
		
		self.rev_needle = OnscreenImage(image = "Textures/needle.png", pos = (-1.6, 0.0, -0.70), scale = (0.5))
		self.rev_needle.setTransparency(TransparencyAttrib.MAlpha)
		
		self.rev_text = OnscreenText(text = " ", pos = (-1.6, -0.90, 0), scale = 0.05)
		
		self.speedometer = OnscreenImage(image = "Textures/dial.png", pos = (-1.68, 0.0, -0.10), scale = (0.7,0.7,0.5))
		self.speedometer.setTransparency(TransparencyAttrib.MAlpha)
		
		self.speedometer_needle = OnscreenImage(image = "Textures/needle.png", pos = (-1.68, 0.0, -0.10), scale = (0.5))
		self.speedometer_needle.setTransparency(TransparencyAttrib.MAlpha)
		
		self.speedometer_text = OnscreenText(text = " ", pos = (-1.68, -0.35, 0), scale = 0.05)
		
		
		#Update the HUD
		def Update_HUD():
			
			#Move gear selector
			if self.gear == -1:
				self.gear2_hud.setPos(-1,0,-0.785)
			if self.gear == 0:
				self.gear2_hud.setPos(-1,0,-0.85)
			if self.gear == 1:
				self.gear2_hud.setPos(-1,0,-0.91)
				
			#Rotate starter
			if self.start == 0:
				self.starter.setHpr(0,0,0)
			else:
				self.starter.setHpr(0,0,45)	
				
			#Update the parking brake light
			if self.Pbrake == 1:
				self.park.setImage("Textures/pbrake2.png")
				self.park.setTransparency(TransparencyAttrib.MAlpha)
			else:
				self.park.setImage("Textures/pbrake.png")
				self.park.setTransparency(TransparencyAttrib.MAlpha)	
				
			#Update the rev counter
			self.rev_needle.setR(self.RPM/22)	
			rev_string = str(self.RPM)[:4]
			self.rev_text.setText(rev_string+" RPM")
			
			#Update the speedometer
			if self.carspeed > 0.0:
				self.speedometer_needle.setR(self.carspeed*2.5)
			if self.carspeed < 0.0:
				self.speedometer_needle.setR(-self.carspeed*2.5)
			speed_string = str(self.carspeed)[:3]
			self.speedometer_text.setText(speed_string+" KPH")
					
					
						
		#Update the program
		def update(task):
			dt = globalClock.getDt() 
			processInput(dt)
			Update_HUD()
			set_time()
			set_terrain()
			set_headlights()
			update_rpm()
			scene.doPhysics(dt, 5, 1.0/180.0)
			return task.cont
			
		taskMgr.add(update, "Update")
		
#Run the program		
D = Drive()
D.run()
