# NNK Modules
## Types of modules
Regular modules consists of generic code (library) and wrapper. Library provides specific functions and can be used by itself
in other projects, while wrapper is closer to application using that library, which also connects to the NNK (specifically broker) through api.

Core modules differ because they won't neccessarily have a library module and are more focused on providing specific functionality.
In other words, they are specific to project and are not meant to be freely reusable by themself.

## Core modules:
- CoRe - made up of smaller modules:
	loads other modules, contains knowledge and params database, acts as intermediary between other core modules
- Ava - produces visual part, stickers, maybe live avatar, we'll see
- Comm - multiple routes of communication, telegram, messenger, mail, possibly sms
- Nlang - processing, understanding and generating natural language, calling relevant utils
- Supervisor - a script checking if everything is working, runs periodically

## Utility modules:
- yt music downloader
- calendar (task manager, deadliner)
- music player
- file downloader
- torrent client
- task manager
	- module for tracking tasks as:
	command to add task, 
	add spent time, 
	add percentage,
	add milestones,
	automatically archivize 100% complete
	add deadlines
	auto remind when deadline nearby (?)
	persist to disk
- arkadia client/manager/pipbuck like soft


## Drafts, Sketches and Ideas
The main module will be called ServiceBroker.
One of its tasks is to provide two tables:
	concrete services (directly from attaching modules, other needs to know exactly what it wants)
	and general services (which will be for other modules not knowing about specific implementations)
		example:
		youtube downloader provides method for downloading a movie
		telegram messenger provides method under 'user-output' which all modules can use
	this requires some standarized names to use in all modules for non-specific services
If there aren't any non-specific services, the broker supplies its own methods, which might be minimalistic
like, when there is no service asking to act as user connection, the broker will provide its own method,
which will print to screen.
The table will work as hashmap of stacks, when asking for service broker looks under the name and grabs the last item from the stack,
because every new service appends last (maybe some priorities?)
The broker will also provide some way of communication between services, since they will most likely run in different threads.
either something like rabbitmq or similar.

Second module will be Configurator.
It will be service itself, providing specific configurations to all requesting services.
When the service first connects, it asks the broker for configuration. If no configurator exists, broker replies.
If configurator exists and doesn't know the service, it asks it for the default config which it then stores and later
returns. Also, if wanted, configurator can supply automatically certain fields if it can recognize them.
If it knows the service, it returns the stored configuration.

Services themselves will act as two-part mechanism:
first part is the object itself, for example task manager will be class for retrieveing, storing, creating and deleting tasks.
By itself it cannot interact with the system directly.
Therefore, every module like this will have its service (module: name, service: nameService)
Service instantiates object, possibly some threads, tells the broker of the services it provides, asks for configuration etc.
Can be thought of as interface or wrapper.
Service and object together form a single module.

---

as for security, right now im not going to check that specifically, ill just check inside telegram if the user writing is my id

---

pause until:
https://pypi.org/project/pause/

---

idea: service broker may not be the one responsible for loading the packages. it should be able to do that but also it may not be the one,
add custom handler for that

---

now the services (module+wrapper) will be called services and the functions (generic call handlers) will be called handlers 
=> service registry, handler registry

## Code drafts
All of the modules should be in separate files.
Most likely will run in their own processes.
Program will start in main which will create the broker, which will load everything else.

```python
# Service Broker
import multiprocessing as mp

class ServiceBroker()
	def __init__(self):  # maybe pass as a param location of services?
		self._serviceRegistry = {}
		self._handlerRegistry = {}
		self._messageQueue = mp.Queue()  # docs claim its threadsafe

	def start():
		# threads for handling messages?
		# like spawn few threads to handle requests from different services
		while True:
			# handle some stuff


	def userOutputHandler(self, output):  # default handler
		print(output)

	def loadServices(): # method for loading the services from the folder
		# possibly add second one for refreshing


sb = ServiceBroker()
sb.start()
```

```python
# thread decorator snippet
def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class MyClass:
    somevar = 'someval'

    @threaded
    def func_to_be_threaded(self):
        # main body

```