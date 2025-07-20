# ESPHome Extensions

This repository contains useful components that extend the functionality of ESPHome.
Some components such as the 'updatable_integration' sensor extend existing components to make them more flexible or modify their behaviour.

To including this repository in your project, use the following in your ESPHome configuration:

```yaml
external_components:
  - source: github://olicooper/esphome-extensions
    components:
      - updatable_integration
```

You can find the list of extensions that are available to use below.


## Updatable Integration Sensor

An extension to the [Integration Sensor](https://esphome.io/components/sensor/integration.html) which provides an additional `set_value` funtion to manually update the value of the sensor.

```yaml
sensor:
  - platform: updatable_integration
    id: updatable_integration_1
    ## All other options available from the standard Integration Sensor

  - platform: template
    name: Some other component
    on_value:
      then:
        ## Option 1
        - updatable_integration.set_value:
            id: updatable_integration_1
            value: !lambda 'return x;'
        ## Option 2
        - lambda: 'id(updatable_integration_1).set_value(x);'

```