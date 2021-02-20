

"""
 This python application is used to display pictures. These pictures may be on 
 a directory, and their paths are copied into a list of strings. After this the
 images are displayed on the window application GUI interface, looping through 
 the whole list of images. 
 The looping can be set to move forward or backward.
 Images can be deleted. This action cannot be undone.
 Image file names can be change. This action cannot be undone. In order to 
 undone this action the file name has to be rename with the old file name.
 The delay time can also be changed, increased or decreased.
 The directory where the images are can be changed or selected at any time, but 
 the app has to be on playing mode. Note: On paused mode it does not work.
 The application can be set in paused mode and change the images, forward or 
 backward, manually.
"""



# Importing libraries to complete this image show project.
import glob
import os
# Libs to manage images and switch images
from PIL import Image, ImageTk, ImageDraw, ImageFont
# Libs to manages GUI widges
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import Frame, Label, Button, Spinbox




"""
Class Window is used to manage the whole proces that this app perform.
This class sets all the widgets that are used in this app.
This class sets all the local variables used to manage the diferent states that
this app can be in. These states are playing or paused.
Other local variables are also used to managed and set the different button colors.
Other local variables are used to set the path of the image files that are swapped.
"""
class Window(Frame):
	"""docstring for Window"""


	def __init__(self, master=None):
		super().__init__(master)
		self.master = master


		# Set of widget style configurations to customize buttons
		self.myStyle = ttk.Style()
		self.myStyle.configure('blue.TButton', background='#0000FF', foreground='#0000FF')
		self.myStyle.configure('red.TButton', background='#FF0000', foreground='#FF0000')
		self.myStyle.configure('green.TButton', background='#20F2B8', foreground='#20F2B8')
		# boolean to set the play button to red when the playing show is paused
		self.greenBlue = False


		# Setting the call back function when the key 'q' is clicked.
		# This function is defined as a class method.
		self.bind_all('q', self.do_exit)


		# Debug lines of code to set the directory of pictures to be displayed.
		self.tmpFileName = 'resizedPic.png'
		self.strPath = ''
		#'C:/Users/jjesu/Desktop/experimentos/fotos/'
		#self.strPath = 'C:\\Users\\jjesu\\Documents\\Python\\Investigacion\\Graficas\\fotoShow\\fotos\\'
		# Ending the debug lines of code.

		# Setting the path list of pictures files to be displayed.
		self.imgNames = []#glob.glob(self.strPath + '*.jpg')
		
		# List of picture files index is set to -1, so when this app starts it 
		# is increment by one.
		self.index = -1#0
		# Boolean to set the direction of the picture movement; forward or 
		# backward.
		self.nextBackMode = True
		# The picture file beeing displayed.
		self.photo = None
		# Setting the status of the playing action; playing or paused.
		self.playingStatus = True
		# Setting the time to display the next picture.
		self.delay = 1000
		# Setting the image height, and from this value the image width.
		self.baseHeight = 650
		# A temporary picture file to make the change of pictures to display 
		# the next image.
		self.labelPicture_old = None
		# Variable to hold the path image and file name. This is mainly for 
		# debugging.
		self.txtFileInfo = tk.StringVar()
		# Variable used in the Spinbox to hold a value to increase or decrease 
		# the delay time.
		self.delayChangeBy = tk.IntVar()

		# if statement to set how the app starts. If there is any images in the 
		# list of images, then it starts showing those images. If there is not 
		# images then it jumps to the else statatement.
		if len(self.imgNames) >= 1:
			self.createWidgets()
		# If list is empty, then this app creates an image letting know user that. 
		# User has to select an images directory to display.
		else:
			# App is creating an image with some text on it.
			imgTmp = Image.new('RGB', (600, 500), color=(0, 0, 250))
			fntTmp = ImageFont.truetype('Gabriola.ttf', 35)
			picTmp = ImageDraw.Draw(imgTmp)
			picTmp.text((15, 100), "Hello My Lord Nicky.  Please Make Your Selection", font=fntTmp, fill=(255, 0, 0))
			imgTmp.save('tmpPic.png')
			# Setting a temporary image path.
			strPathTmp ="tmpPic.png"
			# Setting the application display movement direction.
			self.nextBackMode = False
			# Setting the real image path + name to be displayed. 
			self.imgNames = [self.strPath + strPathTmp]
			# Creating all the main window widgets.
			self.createWidgets() 

	#End of __init__() class constructor function.




	"""
	createWidgets(self) function class is used to set and configure all the main 
	window widgets.
	"""
	def createWidgets(self):

		# Button used to set the images directory path.
		self.setDirBtn = Button(self, text="[Op]", style="blue.TButton", width=5,  command=self.setDirectorio)
		self.setDirBtn.grid(row=0, column=0, sticky=tk.NW) 

		# Spinbox used to set the delta time when the delay time needs to be 
		# changed.
		self.delayTimeSB = Spinbox(self, from_=-19, to=90, increment=1, textvariable=self.delayChangeBy, width=3, command=self.on_setDelayTime)
		self.delayTimeSB.grid(row=1, column=0, sticky=tk.NW, padx=2)

		# Button to set the app movement direction backward. Code to configure 
		# button settings.		
		self.backBtn = Button(self)
		self.backBtn.grid(row=2, column=0, sticky=tk.NW)
		self.backBtn["text"] = "[<B]"
		self.backBtn["width"] = 5
		self.backBtn["command"] = self.backPicture
		self.backBtn["style"] = "blue.TButton"

		# Button to set the app on-paused mode. Code to configure button
		# settings.	
		self.playBtn = Button(self, text="[<>]", style="blue.TButton", width=5, command=self.playShow)
		self.playBtn.grid(row=3, column=0, sticky=tk.NW)

		# Button to set the app movement direction forward. Code to configure 
		# button settings.	
		self.forWardBtn = Button(self, text="[N>]", style="blue.TButton", width=5, command=self.nextPicture)
		self.forWardBtn.grid(row=4, column=0, sticky=tk.NW)


		self.renameBtn = Button(self, text="[Re]", style="blue.TButton", width=5, command=self.renamePicture)
		self.renameBtn.grid(row=5, column=0, sticky=tk.NW, pady=0)


		# Button to used to actually delete an image from the real device. Code 
		# to configure button settings.  This action cannot be undone.
		self.deleteBtn = Button(self, text="[De]", style="red.TButton", width=5, command=self.deletePicture)
		self.deleteBtn.grid(row=6, column=0, sticky=tk.NW)

		# Button to shut off the app. Code to configure button settings.	
		self.quitBtn = Button(self, text="[X]", style="red.TButton", width=5, command=self.doExit)#command=self.master.destroy)
		self.quitBtn.grid(row=7, column=0, sticky=tk.NW)

		# Button to display a label with information about the image being displayed.
		# Code to configure button settings.	
		self.labelInfo = Label(self, textvariable=self.txtFileInfo, font=("TkDefaultFont", 9), wraplength=600)
		self.labelInfo.grid(row=8, column=0, sticky=tk.NW, columnspan=5)

		# If list of images is not empty, then display images on the images list.
		if len(self.imgNames) >= 1:
			self.showImagen()
		# else statement to let user know that there is not images to be displayed.
		else:
			self.txtFileInfo.set("There is not pictures in directory")
			self.labelInfo.configure(background="red")

	#End of createWidgets() class function.




	"""
	on_setDelayTime(self) class callback function is used to change the delay 
	time used to swap images. This callback function is called when the Spinbox 
	widget is clicked to increased or decrease the swapping time.  The lowest 
	time is 50 milliseconds. The highest is 5.5 seconds.
	"""
	def on_setDelayTime(self):
		# Variable to always used the default delay time, even when the delay 
		# var is changed.
		loopingTime = 1000
		# Setting the delay time new value.
		self.delay = loopingTime + (self.delayChangeBy.get() * 50 )

		# Debuggin lines
		##print("Setting delay time by: " + str(self.delayChangeBy.get() * 50) )
		#print("delay time set to:  " + str(self.delay))

	#End of on_setDelayTime(self) class function.




	"""
	setIndex(self) Class function is used to set the index next value. If movement
	is forward index value is increased by one. If movement is backward the index 
	value is decreased by one.
	"""
	def setIndex(self):
		if self.nextBackMode:
			self.index += 1
			# Checking the end of the list. Index is set to zero.
			if self.index >= len(self.imgNames):
				self.index = 0
		else:
			self.index -= 1
			# Checking the beginning of the list. Index is set to the length of 
			# the list minus one.
			if self.index <= 0:
				self.index = len(self.imgNames) - 1

	#End of setIndex() class function.




	"""
	showImagen(self) class function is used to actually display the image.
	"""
	def showImagen(self):
		#print('Calling:  showImagen()')
		# Setting the index value.
		if len(self.imgNames) >= 1:
			self.setIndex()

			# Catching any error while getting a file object.
			#try:      ########################################################

			self.img = Image.open(self.imgNames[self.index])

			#except IOError:###################################################
			#print("Error Error : " + str(self.index))
			#	exit(1)


			# Setting the image size to be displayed. This is done on a temporary
			# image file. Original image is not affected by this code.
			hPercent = (self.baseHeight / float(self.img.size[1]))
			widthSized = int(float(self.img.size[0]) * float(hPercent))
			self.img = self.img.resize((widthSized, self.baseHeight), Image.ANTIALIAS)

			#Saving the temporary image with new sizes. This is the image that 
			#is displayed.
			self.img.save(self.strPath + self.tmpFileName)

			self.photo = ImageTk.PhotoImage(self.img)
			self.img.close()
			# Setting the image to be displayed on a label widget.
			self.labelPicture = Label(self, image=self.photo)
			self.labelPicture.image = self.photo
			# Setting position of the label containing the image. 
			self.labelPicture.grid(row=0, column=1, sticky=(tk.N + tk.S), rowspan=8)
			# Setting the displayed imagen file information label.
			self.txtFileInfo.set("FN: " + self.imgNames[self.index])
			# Swapping image between temporary image holder and the next image holder.
			if self.labelPicture_old is not None:
				self.labelPicture_old.destroy()
			self.labelPicture_old = self.labelPicture


			# Changing play button color between blue and greenish hue
			if self.greenBlue:
				self.playBtn["style"] = "green.TButton"
				self.greenBlue = False
			else:
				self.playBtn["style"] = "blue.TButton"
				self.greenBlue = True

			# Setting play button color to red when play show is paused
			if self.playingStatus == False:
				self.playBtn["style"] = "red.TButton"


			# Making the real image swapping after time delay, set on the delay 
			# variable.
			if self.playingStatus:
				self.after(self.delay, self.showImagen)

		# Debugging information.		
		else:
			print("No more pics to show....")
			
	#End of showImagen(self) class function.




	"""
	playShow(self) class function is used to set the application movement, 
	forward-backward, and button caption to reflect the movement direction.
	"""
	def playShow(self):
		#print('Calling:  playShow()')
		# Setting the app in play mode.
		if self.playingStatus == True:
			self.playingStatus = False
			self.playBtn["text"] = "[<>]"
			self.playBtn["style"] = "red.TButton"
		# Setting the app in pause mode.
		else:
			#print("Movement before:" + str(self.nextBackMode))
			self.playingStatus = True
			
			if self.nextBackMode:
				self.playBtn["text"] = ">>>>"
			else:
				self.playBtn["text"] = "<<<<"

			self.playBtn["style"] = "blue.TButton"
			#print("Movement after:" + str(self.nextBackMode))

			self.showImagen()

	#End of playShow() class function.




	"""
	setDirectorio(self) class callback function is used to set the directory 
	containing the images to be displayed. This process has to be done only 
	when the app in playing mode, but the app itself change to the paused mode. 
	Then it opens the file dialog chooser interface to select the directory. 
	When th directory selction is done the function set file path separtor from 
	'\' to '/'. Then it calls the playShow() function to start swapping the 
	images.
	""" 
	def setDirectorio(self):
		
		#Selecting the directory containing the images can be done only when the
		#app is in playing mode (no in paused mode.)
		if self.playingStatus == True:
			#Calling this function to set the app in paused mode.
			self.playShow()
			#Showing the file chooser GUI interface.
			dirName = tk.filedialog.askdirectory()
			#Building the absolute image file paths.
			self.strPath = dirName + '/'
			#Getting only file with estension jpg, png and jpeg.
			self.imgNames = glob.glob(self.strPath + '*.jpg')
			self.imgNames = self.imgNames + glob.glob(self.strPath + '*.png')
			self.imgNames = self.imgNames + glob.glob(self.strPath + '*.jpeg')

			#for loop to change all file path separator from '\' to '/'
			for i in range(len(self.imgNames)):
				self.imgNames[i] = self.imgNames[i].replace('\\', '/')

			# Calling playShow() function to display the image in the new directory.
			self.playShow()

	#End of setDirectorio(self) class function.




	"""
	backPicture(self) class callback function is used to set the application
	movement backward.
	AVISO: ver lo de como elegir un directorio con la funcion bind.
	"""
	def backPicture(self):
		# if statement to set the application movement backward.
		if len(self.imgNames) >= 1:
			self.nextBackMode = False
			self.playBtn["text"] = "<<<<"
			if self.playingStatus == False:
				self.showImagen()
		#  else statement to show debugging info.
		else:
			print("imgNames size esta mas bajo que zero")

	#End of backPicture(self) function.




	"""
	nextPicture(self) class callback function is used to set the application 
	movement forward.
	"""
	def nextPicture(self):
		if len(self.imgNames) >= 1:
			self.nextBackMode = True
			self.playBtn["text"] = ">>>>"
			if self.playingStatus == False:
				self.showImagen()
		#  else statement to show debugging info.
		else:
			print("imgNames size esta mas bajo que zero")

	#End of nextPicture(self) function.




	"""
	deletePicture(self) class callback function that is called when the delete 
	[<D>] button is clicked. This method is used to actually delete an image 
	file from the device. This action cannot be undone.
	"""
	def deletePicture(self):
		# Warning the user that deleting a picture can be done only when the app is 
		# on paused mode. 
		if self.playingStatus == True:
			print("To delete a picture set the app on Paused Mode.")
		else:
			# The app is on paused mode and pictures can be deleted.
			# Checking that the list of pictures files is not empty.
			if len(self.imgNames) > 0:
				# Debbuging output
				print("Deleting picture:  " + self.strPath + self.tmpFileName)
				# Making sure that the picture file exist.
				if os.path.exists(self.strPath + self.tmpFileName):	
					print("File exist:" + "  " + str(os.path.exists(self.strPath + self.tmpFileName)) )			
					# Error catching if there is any problem deleting the picture file.
					try:
						os.remove(self.imgNames[self.index])
					except:
						self.txtFileInfo.set("SYSTEM ERROR REMOVING FILE.")
						self.labelInfo.configure(background="red")
						print("SYSTEM ERROR REMOVING FILE.")
						# Exiting the method-function without chrasing the app
						return
				else:
					print("The file that is been removed does not exist on this folder.")
					print("Exiting the deleting function.")
					return

				# Getting the directory list of picture files, after deleting 
				# or trying to delete a file picture.
				self.imgNames = glob.glob(self.strPath + '*.jpg')
				# Setting the index list after deleting a directory picture file.
				if self.index >= len(self.imgNames):
					self.index = len(self.imgNames) - 1

				# Setting the direction mode: next or back. This depends on the 
				# user last click on the next or back button. 
				if self.nextBackMode:
					self.nextPicture()
				else:
					self.backPicture()

			# Letting know the user that there is not more files that can be deleted.
			else:
				# Out putting a warning on the main window frame. No more picurte 
				# files can be deleted.
				self.txtFileInfo.set("No more files to delete....")
				self.labelInfo.configure(background="red")

	#End of deletePicture() function.




	"""
	cambiarNombre(self) function is used to build the full new file name. In 
	order to build this, it get the file extension from the old file name. It 
	join this file extension to the file name enterd by the user. Finally it 
	join this file name to the absolute file path. After this it startes the 
	renaming process. It also update the file name list with the new file 
	name. It also updates the file name info Label widget on the GUI interface.
	"""
	def cambiarNombre(self):
		#try-except block to try to catch any error during the renaming process.
		try:
			#Getting the file extension, so user does not have to type.
			nombre, fileExte = os.path.splitext(self.imgNames[self.index])
			#Building the new full file path.
			newPicName = os.path.join(self.strPath, self.entry.get())
			#Adding the file extension to the new file name entered by users.
			newPicName = newPicName + fileExte
			#Executing the renaming process.
			os.rename(self.imgNames[self.index], newPicName)
			#Updating the file name list with the new file name.
			self.imgNames[self.index] = newPicName
			#Updating the GUI Label file info with the new file name.
			self.txtFileInfo.set('FN: ' + self.imgNames[self.index])
		#Catching any error, it something goes wrong.
		except OSError as osE:
			print('OS-OS-ERROR-ERROR: ' + osE.strerror)
		#Destroying the dialog GUI interface.
		self.miniWindow.destroy()

	#End of cambiarNombre(self) function.




	"""
	cancelarCambiarNombre(self) function is used to calcel the renaming file 
	process.
	"""
	def cancelarCambiarNombre(self):
		self.miniWindow.destroy()

	#End of cancelarCambiarNombre(self) function.




	"""
	Function createRenameDialog(self) is only used to build a dialog interface
	to ask users to enter the new file name. This GUI interface also has a cancel 
	button to abort the renaming process. All the actual renaming process is done 
	by another function that is called when the change button is clicked.
	"""
	def createRenameDialog(self):
		#Global variables to get the new file name and to handle the dialog 
		#window.
		self.picName = tk.StringVar()
		self.miniWindow = tk.Tk("HelloView")

		#Two label to instruct users what to do on the dialog interface.
		labelInfoTmp1 = tk.Label(master=self.miniWindow, text='Enter New Picture Name:')
		labelInfoTmp1.grid(row=0, column=0, sticky=tk.W)
		labelInfoTmp2 = tk.Label(master=self.miniWindow, text='Don\'t type file extension. It\'ll be added.')
		labelInfoTmp2.grid(row=1, column=0, sticky=tk.W, columnspan=2)

		#Entry widget to get the new file name entered by users.
		self.entry = ttk.Entry(master=self.miniWindow, textvariable=self.picName, text='NIKO.....')
		self.entry.grid(row=2, column=0, sticky=tk.W, columnspan=2)

		#Button to start the file renaming process.
		btnChangeName = ttk.Button(master=self.miniWindow, text='Cambiar', command=self.cambiarNombre)
		btnChangeName.grid(row=3, column=0, sticky=tk.W)

		#Button to cancel the file renaming process.
		btnCancel = ttk.Button(master=self.miniWindow, text='Cancel', command=self.cancelarCambiarNombre)
		btnCancel.grid(row=3, column=1, sticky=tk.W)

	#End of createRenameDialog(self) function.	




	"""
	Function renamePicture(self) is used to start the process to rename a picture
	file name, initiated by user. This function checks the app is in pause mode,
	and that the image path name list is not empty, and it makes sure the file 
	exist. If this is true it calls a function to build a dialog to get the new 
	file name from the user. It also try to let user know of any error that make
	raise about file management.
	"""
	def renamePicture(self):
		# Warning user that renaming a picture can be done only when the app is 
		# on paused mode. 
		if self.playingStatus == True:
			print("To delete a picture set the app on Paused Mode.")
		else:
			#Starting renaming process.
			#Checking path name list is not empty.
			if len(self.imgNames) > 0:
				#Making sure that the picture file exist.
				if os.path.exists(self.imgNames[self.index]):
					#Call function to create dialog to get new file name.
					self.createRenameDialog()

				#Trying to catch the file does not exist error with if-else.
				else:
					print("The file that is been renamed does not exist on this folder.")
					print("Exiting the deleting function.")
					return

	#End of renamePicture(self):function.
			



	"""
	do_exit(self, event) class call back function that is called when the 'q' 
	keyboard key is pressed.
	AVISO: This and the next function are equal. I had to code only one.
	"""
	def do_exit(self, event):
		# if statement to delete the temporary picture create to resize the original picture.
		# This statement keeps the original picture size with out any changes on it.
		if os.path.exists(self.strPath + self.tmpFileName):
			os.remove(self.strPath + self.tmpFileName)
		# Debugging printing
		print("Terminando Programa")
		# Exiting the application
		self.quit()

	#End of do_exit() function.




	"""
	doExit(self) class callback method to shut down this qpp when the X top-right 
	button is clicked.
	"""
	def doExit(self):
		# if statement to delete the temporary picture create to resize the original picture.
		# This statement keeps the original picture size with out any changes on it.
		if os.path.exists(self.strPath + self.tmpFileName):
			os.remove(self.strPath + self.tmpFileName)
		
		print("Terminando Programa")
		# Exiting the application
		self.quit()

	#End of doExit() function.



#End of the main Window class. 





""" 
This class is to start the application. It does just a few main window 
configurations.
"""
class ImageShowApp(tk.Tk):
	"""docstring for ImageShowApp"""

	# Class constructor.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Setting the application name and title.
		self.title("Nicky Picture Show Project")
		# Position of the main window.
		self.geometry("+0+0")
		# self.resizable(width=False, height=False)
		# Starting the class that does all the job.
		Window(self).grid(sticky=(tk.E, tk.W, tk.N, tk.S))
		#self.columnconfigure(0, weight=2)

#End of ImageShowApp class.




"""
Making sure that this file is the one that is runnig as a stand along application. 
"""
if __name__ == '__main__':
	imgShowApp = ImageShowApp()
	imgShowApp.mainloop()




################################### END OF FILE #######################################