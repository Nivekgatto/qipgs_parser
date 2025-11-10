import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import CONF_ID, CONF_NAME, UNIT_VOLT, UNIT_PERCENT, ICON_FLASH, ICON_PERCENT

DEPENDENCIES = ["uart"]

qpigs_ns = cg.esphome_ns.namespace("qpigs_parser")
QPIGSSensor = qpigs_ns.class_("QPIGSSensor", sensor.Sensor, cg.Component)

CONF_UART_ID = "uart_id"
CONF_AC_INPUT_VOLTAGE = "ac_input_voltage"
CONF_AC_OUTPUT_VOLTAGE = "ac_output_voltage"
CONF_LOAD_PERCENT = "load_percent"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(QPIGSSensor),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    cv.Optional(CONF_AC_INPUT_VOLTAGE): sensor.sensor_schema(unit=UNIT_VOLT, icon=ICON_FLASH, accuracy_decimals=1),
    cv.Optional(CONF_AC_OUTPUT_VOLTAGE): sensor.sensor_schema(unit=UNIT_VOLT, icon=ICON_FLASH, accuracy_decimals=1),
    cv.Optional(CONF_LOAD_PERCENT): sensor.sensor_schema(unit=UNIT_PERCENT, icon=ICON_PERCENT, accuracy_decimals=1),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    uart_comp = await cg.get_variable(config[CONF_UART_ID])
    cg.add(var.set_uart(uart_comp))

    if CONF_AC_INPUT_VOLTAGE in config:
        sens = await sensor.new_sensor(config[CONF_AC_INPUT_VOLTAGE])
        cg.add(var.set_ac_input_voltage_sensor(sens))

    if CONF_AC_OUTPUT_VOLTAGE in config:
        sens = await sensor.new_sensor(config[CONF_AC_OUTPUT_VOLTAGE])
        cg.add(var.set_ac_output_voltage_sensor(sens))

    if CONF_LOAD_PERCENT in config:
        sens = await sensor.new_sensor(config[CONF_LOAD_PERCENT])
        cg.add(var.set_load_percent_sensor(sens))

