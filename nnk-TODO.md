# TODO's
figure out file structure of models
decide how the message class should look like

Note:
queues appear not to be pickle'able,
therefore it would make sense to use threads for core 

(the broker wouldnt be able to receive the queues from loader)

draw a schematic, maybe instead running whole object in thread run just a threaded method,
maybe add something on top of broker (core or smth, supervisor, dunno)

input preprocessor - wouldnt make sense to add it to regular handler library
options:
    add as a layer (functional style) to the last added handler
    add another library (dict) like handlers but for preprocessor, would work as a layer between regular handlers
        and the preprocessors (like nltk)


configuration - either through loader (as parameter) or through broker (as request)

figure out how to pass loader config and broker between themselves as to not create circular dependencies
--> solved, broker is independent from other core, other core requires loader at creation

use abstract classes to build modules