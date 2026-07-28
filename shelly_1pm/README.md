# Shelly Dynamic Threshold Automation

This folder contains `shelly_dynamic_threshold.yaml`, a Home Assistant automation that controls a Shelly 1PM switch based on a battery sensor and time windows.

**Software / Integration Requirements**

- Home Assistant Core (running on a supported platform)
- Shelly integration (for `switch.shelly1pm`)
- A battery sensor entity providing a numeric state, e.g. `sensor.deye_battery`
- Notify integration configured with `notify.notify` (or update the automation to use your notifier)

**Features used**

- Jinja2 templating and `variables` (Home Assistant template support)
- `choose` action and `time` triggers
- `state` triggers and `switch.turn_on` / `switch.turn_off` actions

**Installation / Usage**

1. Place `shelly_dynamic_threshold.yaml` in your automations folder (or include it from your main `automations.yaml`).
2. Reload automations from Settings → Server Controls → Reload Automations, or restart Home Assistant.
3. Ensure entities referenced in the file exist and update entity IDs if necessary.

**Testing**

- Use Developer Tools → Templates to test template expressions like `{{ states('sensor.deye_battery') | float(0) }}`.
- Manually trigger the automation from the UI to verify actions.

If you want, I can create a small checklist to validate each dependency, or add a Home Assistant `blueprint` version of this automation.
