This was entirely created with Claude.ai with the following prompt:

"I need to create an integration for homeassistant that will sync the time to a switchbot meter pro device over bluetooth without using the switchbot app"

Issues with adding devices:

"The integration doesn't seem to work.  It doesn't find a device if it is already added to the switchbot integration.  Even without the device added to the official switchbot integration, it was not able to find the device"

Final prompt:

"That worked better!  The integration is recognizing the switchbot meter.  However, using the integration, the time was set to 2:00 on January 1st."

After Claude:

- Changed format to big endian long long to get all 8 bytes.
- Added Timezone offset code to coordinator.  Otherwise you get UTC.

Stuff that still does not work:

- button has a few references to self.hass.  They seem to error out with "'AttributeError: 'HomeAssistant' object has no attribute 'components'"
