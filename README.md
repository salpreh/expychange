# expychange
Messaging system implementation in python.

## Overview
Implementation is based on 3 concepts:
- `Exchange`: A broker between `Emitters` and `Listeners`. I'ts organized in **channels** where emitters and listeners subscribe.
- `Emitter`: Emits events in an `Exchange` to a concrete **channel** (for now emitter only send events to one channel)
- `Listeners`: Subscribes to a **channel** in an `Exchange`. `Exchange` will notify the listener when an event arrives to subscribed **channel**

_**NOTE**: Under construction_