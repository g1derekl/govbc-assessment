# Assignment

This is my submission for the written assignment portion of the application to the position of
ISL 21R Full Stack Developer (Requisition #117214).

## Assumptions

The instructions specified that the rule engine work with the Winter Supplement web application
to determine eligibility for supplementary assistance. However, the Winter Supplement app does not
appear to publish to the `BRE/calculateWinterSupplementInput/<MQTT topic ID>` topic at
`test.mosquitto.org`. Therefore, I have included some shell commands to publish to that topic and
listen to the response at `BRE/calculateWinterSupplementOutput/<MQTT topic ID>` to capture the
output from the rule engine.

## Setup

- Prerequisites:
  - Python 3.10 or newer

- Install the Mosquitto CLI:
  - Ubuntu: `sudo apt-get update && sudo apt-get install mosquitto`
  - MacOS: `brew update && brew install mosquitto`
  
- Install Python dependencies:
  - `pip install -r requirements.txt`

- Set up `.env`
  - Set the environment variables `MQTT_SERVER`, `MQTT_PORT` and `MQTT_TOPIC` in a `.env` file at the root of this project. See `main.py` for example values.
  - Note that the value of `MQTT_TOPIC` is taken from the "MQTT Topic ID" field of the Winter Supplement app, and changes each time the app page is refreshed.

## Unit Tests

Tests are contained in the `tests` folder. To run, simply enter `pytest` in the root directory of this project.

## Run the MQTT service to receive inputs and send outputs

Simply run `python main.py` to start the MQTT service.

## Send input and capture output

Since the Winter Supplement app does not seem to send messages to the MQTT broker, we can do that ourselves in the shell to test the rule engine.
  - With the MQTT service running, set up a listener to subscribe to the output topic:
    `mosquitto_sub -p 1883 -h test.mosquitto.org -t 'BRE/calculateWinterSupplementOutput/<MQTT topic ID>'`
  - Send a message to be captured by the MQTT service and evaluated by the rule engine:
    `mosquitto_pub -p 1883 -h test.mosquitto.org -t 'BRE/calculateWinterSupplementInput/<MQTT topic ID>' -m '{"id": "foo", "numberOfChildren": 2, "familyComposition": "couple", "familyUnitInPayForDecember": true}'`

## Customization

To write custom conditions or to use this rule engine in your project with an entirely new set of conditions, follow these steps:

#### Create rule conditions

To create a rule condition, create an instance of the `Condition` class defined in `rule.py`. The instance must have the following properties:
  - `name` of the condition
  - `evaluation` - a Python function that takes the input object and evaluates whether the condition is met
  - `result` - a Python function that returns a dictionary in the following format:
    ```
    {
      "id": "str", // the unique ID value taken from the input
      "isEligible": "bool", // whether the family is eligible for supplementary assistance
      "baseAmount": 60, // base amount of eligibility calculated from family composition
      "childrenAmount": 0, // additional amount based on number of children, if applicable
      "supplementAmount": 60 // total amount of eligible supplementary assistance
    }
    ```
    This is the object that will be converted to JSON and published to the output topic.

#### Initialize the rule engine

To create an instance of the rule engine with the created conditions, use
```
rule = Rule(conditions=conditions)
```
where `conditions` is a list of the conditions created according to the previous step.

#### Evaluate an input

When an input object is received from the message queue, load it into a Python dictionary and evaluate it against the rule engine
```
import json
output = rule.evaluate(json.loads(input_dict))
```

## Possible future enhancements

- Package the project in a container (e.g. Docker) to allow one-step setup and running and ensure consistency with runtime environments across machines
- A UI to send input data to MQTT and capture output from the rule engine