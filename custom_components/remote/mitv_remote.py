"""
Demo platform that has two fake remotes.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
from homeassistant.components.remote import RemoteDevice
from homeassistant.const import DEVICE_DEFAULT_NAME
import voluptuous as vol

import homeassistant.components.remote as remote
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_NAME, CONF_HOST, CONF_PORT, ATTR_ENTITY_ID)
from homeassistant.components.remote import (
    PLATFORM_SCHEMA, DOMAIN, ATTR_DEVICE, ATTR_ACTIVITY, ATTR_NUM_REPEATS,
    ATTR_DELAY_SECS)
import logging
import requests

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
})
_Log=logging.getLogger(__name__)
COMMANDS = {
    'isalive':'/request?action=isalive',
    'power':'/controller?action=keyevent&keycode=power',
    'enter':'/controller?action=keyevent&keycode=enter',
    'back':'/controller?action=keyevent&keycode=back',
    'home':'/controller?action=keyevent&keycode=home',
    'menu':'/controller?action=keyevent&keycode=menu',
    'right':'/controller?action=keyevent&keycode=right',
    'left':'/controller?action=keyevent&keycode=left',
    'up':'/controller?action=keyevent&keycode=up',
    'down':'/controller?action=keyevent&keycode=down',
    'volumedown':'/controller?action=keyevent&keycode=volumedown',
    'volumeup':'/controller?action=keyevent&keycode=volumeup',
}
# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the demo remotes."""
    host = config.get(CONF_HOST)
    if host == None:
        _Log.error('pls enter host ip address!')
        return False
    name = config.get(CONF_NAME)
    add_devices_callback([
        mitvRemote(hass, host, name+'_mitv_power', 'power', False, True, 'mdi:power-plug-off'),
        mitvRemote(hass, host, name+'_mitv_isalive', 'isalive', False, True, 'mdi:power'),
        mitvRemote(hass, host, name+'_mitv_enter', 'enter', False, True, 'mdi:adjust'),
        mitvRemote(hass, host, name+'_mitv_back', 'back', False, True, 'mdi:keyboard-backspace'),
        mitvRemote(hass, host, name+'_mitv_home', 'home', False, True, 'mdi:home'),
        mitvRemote(hass, host, name+'_mitv_menu', 'menu', False, True, 'mdi:menu'),
        mitvRemote(hass, host, name+'_mitv_right', 'right', False, True, 'mdi:arrow-right-bold-circle'),
        mitvRemote(hass, host, name+'_mitv_left', 'left', False, True, 'mdi:arrow-left-bold-circle'),
        mitvRemote(hass, host, name+'_mitv_up', 'up', False, True, 'mdi:arrow-up-bold-circle'),
        mitvRemote(hass, host, name+'_mitv_down', 'down', False, True, 'mdi:arrow-down-bold-circle'),
        mitvRemote(hass, host, name+'_mitv_volumedown', 'volumedown', False, True, 'mdi:volume-plus'),
        mitvRemote(hass, host, name+'_mitv_volumeup', 'volumeup', False, True, 'mdi:volume-minus'),
    ])


class mitvRemote(RemoteDevice):
    """Representation of a demo remote."""

    def __init__(self, hass, host, name, command, state, assumed, icon):
        """Initialize the Demo Remote."""
        self._name = name or DEVICE_DEFAULT_NAME
        self._state = state
        self._icon = icon
        self._last_command_sent = None
        self._assumed = assumed
        self._command = command
        self._host = host


    @property
    def should_poll(self):
        """No polling needed for a demo remote."""
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
    def assumed_state(self):
        """Return if the state is based on assumptions."""
        return self._assumed


    @property
    def is_on(self):
        """Return true if remote is on."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return device state attributes."""
        if self._last_command_sent is not None:
            return {'last_command_sent': self._last_command_sent}

    def turn_on(self, **kwargs):
        """Turn the remote on."""
        self._state = self.send_command()
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the remote off."""
        self._state = self.send_command()
        self.schedule_update_ha_state()


    def send_command(self):
        """Send a command to a device."""
        if self._command == None:
            _Log.error('Command Code is nil!')
            return

        url = 'http://{host}:6095/controller?action=keyevent&keycode={code}'.format(host=self._host, code=self._command)
        return self.sendHttpRequest(url)

    def sendHttpRequest(self,url):
        try:
            resp = requests.get(url)
            if resp.status_code and resp.text == 'success':
                return False
            return True
        except Exception as e:
            _Log.error("requst url:{url} Error:{err}".format(url=url,err=e))
            return False
