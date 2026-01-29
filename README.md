This was entirely created with Claude.ai starting with the following prompt:

_I need to create an integration for homeassistant that will sync the time to a switchbot meter pro device over bluetooth without using the switchbot app_

Issues with adding devices:

_The integration doesn't seem to work.  It doesn't find a device if it is already added to the switchbot integration.  Even without the device added to the official switchbot integration, it was not able to find the device_

Final prompt that tried to move it to Little Endian:

_That worked better!  The integration is recognizing the switchbot meter.  However, using the integration, the time was set to 2:00 on January 1st._

After Claude:

- Changed format to big endian long long to get all 8 bytes. ('>Q' instead of '<I')
- Added Timezone offset code to coordinator.  Otherwise you get UTC.

Stuff that still does not work:

- button has a few references to self.hass.  They seem to error out with "'AttributeError: 'HomeAssistant' object has no attribute 'components'"
