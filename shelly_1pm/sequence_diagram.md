# Sequence Diagram — Shelly Dynamic Threshold Automation (detailed)

This file contains a Mermaid sequence diagram and an expanded, step-by-step sequence + pseudocode describing every decision the automation makes each time it runs.

Open this file in a Markdown viewer that supports Mermaid (VS Code + Mermaid Preview, GitHub PRs, or mermaid.live).

```plantuml
@startuml
participant Sensor as "sensor.deye_battery"
participant Timer as "TimeTrigger"
participant HA as "HomeAssistant"
participant Automation as "Automation"
participant Template as "TemplateEngine"
participant Switch as "switch.shelly1pm"
participant Notify as "notify.notify"

note over Sensor,Timer: Triggers — sensor state change, scheduled times
Sensor -> Automation: Trigger (battery state changed)
Timer -> Automation: Trigger (05:00 or 08:00)
note over HA,Automation: HA start event triggers evaluation
HA -> Automation: Event: homeassistant_start

Automation -> Template: Read sensor and evaluate variables
Template --> Automation: Returns battery, window_a, on_threshold, off_threshold

alt ON condition (battery >= on_threshold and switch == off)
  Automation -> Switch: switch.turn_on()
  Automation -> Notify: notify "Shelly Activated" (battery, on_threshold, window)
else
  alt OFF condition (battery <= off_threshold and switch == on)
    Automation -> Switch: switch.turn_off()
    Automation -> Notify: notify "Shelly Deactivated" (battery, off_threshold, window)
  else
    Automation --> HA: No action (conditions not met)
  end
end

note right of Template
  Threshold computation:\nwindow_a = now().hour >= 5 and now().hour < 8\non_threshold = 50 if window_a else 75\noff_threshold = 20 if window_a else 60
end note

note over Automation,Switch,Notify: Side-effects: switch state changes and notifications

@enduml
```

## Full step-by-step runtime sequence

1. Trigger: Automation runs when any of the following occur:
   - `sensor.deye_battery` state changes
   - Time at `05:00:00` or `08:00:00`
   - Home Assistant startup (event `homeassistant`)

2. Variable evaluation (Template Engine)
   - `battery = float(states('sensor.deye_battery') | float(0))`
   - `window_a = now().hour >= 5 and now().hour < 8` (true during window A)
   - `on_threshold = 50 if window_a else 75`
   - `off_threshold = 20 if window_a else 60`

3. Decision order (exactly as in the YAML `choose` blocks):
   - First, evaluate the ON branch conditions:
   - Condition A1: `battery >= on_threshold`
   - Condition A2: `switch.shelly1pm` state == `off`
   - If both true: call `switch.turn_on` then `notify.notify` with message:
     - "Battery: {battery}%. Threshold: {on_threshold}%. Time Window: {A/B}. Shelly turned ON."
     - END (automation stops after sequence completes)
   - Else (ON branch not taken): evaluate the OFF branch conditions:
   - Condition B1: `battery <= off_threshold`
   - Condition B2: `switch.shelly1pm` state == `on`
   - If both true: call `switch.turn_off` then `notify.notify` with message:
     - "Battery: {battery}%. Threshold: {off_threshold}%. Time Window: {A/B}. Shelly turned OFF."
     - END
   - Else: No actions performed.

4. Notes about edge cases
   - If the battery sensor is unavailable or non-numeric, `battery` coerces to `0` and the OFF branch may trigger.
   - The automation's `mode: single` prevents concurrent runs; overlapping triggers are ignored while an instance runs.

## Mapping to code (YAML)

- Variables: see the `variables:` block in `shelly_dynamic_threshold.yaml` for the exact Jinja expressions.
- Actions: two `choose` blocks implement the ON and OFF branches respectively; the order is important — ON branch is evaluated first.

## Viewing the diagram

- Open [shelly_1pm/sequence_diagram.md](shelly_1pm/sequence_diagram.md) in VS Code and use a Mermaid preview extension, or paste the mermaid block into mermaid.live.
- If you want, I can render and add a PNG/SVG next to the file and commit it.

