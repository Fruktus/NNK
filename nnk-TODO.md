# TODO's
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
--> solved, broker is independent from other core, other core requires broker at creation

use abstract classes to build modules


requirements per module?

create supervisor which would initialize the core. supervisor would also have a separate thread
(see here: https://stackoverflow.com/questions/39089776/python-read-named-pipe)
which would wait blocked for other process to write to pipe, this would be used by perhaps cron-scheduled
job which would check the nnk's state and restart whole server if necessary
TODO: related to above, create constants for modules status like normal, warning, exited etc
(active-okay, inactive-normal exit, dead-exception caused exit, ...?)