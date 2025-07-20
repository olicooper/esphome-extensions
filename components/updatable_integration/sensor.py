import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
# from esphome.components import integration
from esphome.components.integration import sensor as integration
from esphome.components import sensor
from esphome.const import (
    CONF_ICON,
    CONF_ID,
    CONF_SENSOR,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ACCURACY_DECIMALS,
)
from esphome.core.entity_helpers import inherit_property_from

updatable_integration_ns = cg.esphome_ns.namespace("updatable_integration")
UpdatableIntegrationSensor = updatable_integration_ns.class_(
    "UpdatableIntegrationSensor", integration.IntegrationSensor
)
SetValueAction = updatable_integration_ns.class_("SetValueAction", automation.Action)

CONF_VALUE = "value"

CONFIG_SCHEMA = (
    integration.CONFIG_SCHEMA
    .extend(
        {
            cv.GenerateID(): cv.declare_id(UpdatableIntegrationSensor)
        }
    )
)

# FINAL_VALIDATE_SCHEMA = integration.FINAL_VALIDATE_SCHEMA.extend({
#     cv.Required(CONF_ID): cv.use_id(UpdatableIntegrationSensor),
# })

FINAL_VALIDATE_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.use_id(UpdatableIntegrationSensor),
            cv.Optional(CONF_ICON): cv.icon,
            cv.Optional(CONF_UNIT_OF_MEASUREMENT): sensor.validate_unit_of_measurement,
            cv.Optional(CONF_ACCURACY_DECIMALS): sensor.validate_accuracy_decimals,
            cv.Required(CONF_SENSOR): cv.use_id(sensor.Sensor),
        },
        extra=cv.ALLOW_EXTRA,
    ),
    inherit_property_from(CONF_ICON, CONF_SENSOR),
    inherit_property_from(
        CONF_UNIT_OF_MEASUREMENT, CONF_SENSOR, transform=integration.inherit_unit_of_measurement
    ),
    inherit_property_from(
        CONF_ACCURACY_DECIMALS, CONF_SENSOR, transform=integration.inherit_accuracy_decimals
    ),
)

async def to_code(config):
    await integration.to_code(config)
    # var = await cg.get_variable(config[CONF_ID])
    # cg.add(var.set_component_source("updatable_integration.sensor"))

@automation.register_action(
    "sensor.updatable_integration.set_value",
    SetValueAction,
    automation.maybe_simple_id(
        {
            cv.Required(CONF_ID): cv.use_id(UpdatableIntegrationSensor),
            cv.Optional(CONF_VALUE): cv.templatable(cv.float_)
        }
    ),
)
async def sensor_updatable_integration_set_value_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    template_ = await cg.templatable(config[CONF_VALUE], args, float)
    var = cg.new_Pvariable(action_id, template_arg, paren)
    cg.add(var.set_value(template_))

    return var