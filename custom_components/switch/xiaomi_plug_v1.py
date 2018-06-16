"""
Support for Xiaomi Smart WiFi Socket and Smart Power Strip.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/switch.xiaomi_plug/
"""
import asyncio
from functools import partial
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA, )
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN, )
from homeassistant.exceptions import PlatformNotReady

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Xiaomi Plug V1'
PLATFORM = 'xiaomi_plug_v1'
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_TOKEN): vol.All(cv.string, vol.Length(min=32, max=32)),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

REQUIREMENTS = ['python-mirobo>=0.1.3']

ATTR_POWER = 'power'
ATTR_CURRENT = 'current'
ATTR_LOAD_POWER = 'load_power'
SUCCESS = ['ok']
CONF_USB = '_usb'


# pylint: disable=unused-argument
@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the plug from config."""
    from mirobo import PlugV1, DeviceException
    if PLATFORM not in hass.data:
        hass.data[PLATFORM] = {}

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing with host %s (token %s...)", host, token[:5])

    try:
        plug = PlugV1(host, token)

        xiaomi_plug_switch = XiaomiPlugSwitch(name, plug, False)
        xiaomi_plug_switch_usb = XiaomiPlugSwitch(name+CONF_USB, plug, True)
        hass.data[PLATFORM][host] = xiaomi_plug_switch
        hass.data[PLATFORM][host+CONF_USB] = xiaomi_plug_switch_usb
    except DeviceException:
        raise PlatformNotReady

    async_add_devices([xiaomi_plug_switch], update_before_add=True)
    async_add_devices([xiaomi_plug_switch_usb], update_before_add=True)


class XiaomiPlugSwitch(SwitchDevice):
    """Representation of a Xiaomi Plug."""

    def __init__(self, name, plug, is_usb):
        """Initialize the plug switch."""
        self._name = name
        self._icon = is_usb and 'mdi:usb' or 'mdi:power-socket'

        self._plug = plug
        self._state = None
        self._state_attrs = {}
        self._skip_update = False
        self._is_usb = is_usb

    @property
    def should_poll(self):
        """Poll the plug."""
        return True

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use for device if any."""
        return self._icon

    @property
    def available(self):
        """Return true when state is known."""
        return self._state is not None

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    @asyncio.coroutine
    def _try_command(self, mask_error, func, *args, **kwargs):
        """Call a plug command handling error messages."""
        from mirobo import DeviceException
        try:
            result = yield from self.hass.async_add_job(
                partial(func, *args, **kwargs))

            _LOGGER.debug("Response received from plug: %s", result)

            return result == SUCCESS
        except DeviceException as exc:
            _LOGGER.error(mask_error, exc)
            return False

    @asyncio.coroutine
    def async_turn_on(self, **kwargs):
        """Turn the plug on."""
        if self._is_usb:
            result = yield from self._try_command(
                "Turning the plug usb on failed.", self._plug.usb_on)
        else:
            result = yield from self._try_command(
                "Turning the plug on failed.", self._plug.on)

        if result:
            self._state = True
            self._skip_update = True

    @asyncio.coroutine
    def async_turn_off(self, **kwargs):
        """Turn the plug off."""
        if self._is_usb:
            result = yield from self._try_command(
                "Turning the plug usb off failed.", self._plug.usb_off)
        else:
            result = yield from self._try_command(
                "Turning the plug off failed.", self._plug.off)

        if result:
            self._state = False
            self._skip_update = True

    @asyncio.coroutine
    def async_update(self):
        """Fetch state from the device."""
        from mirobo import DeviceException

        # On state change the device doesn't provide the new state immediately.
        if self._skip_update:
            self._skip_update = False
            return

        try:
            state = yield from self.hass.async_add_job(self._plug.status)
            _LOGGER.warn("%s Got new state: %s", self._name, state)

            self._state = self._is_usb and state.usb_power or state.is_on
            self._state_attrs = {
                ATTR_LOAD_POWER: hasattr(state, ATTR_LOAD_POWER) and state.load_power or None,
                ATTR_CURRENT: hasattr(state, ATTR_CURRENT) and state.current or None,
            }

        except DeviceException as ex:
            _LOGGER.error("Got exception while fetching the state: %s", ex)
