# Pseudocode Diagram — Shelly Dynamic Threshold

This diagram visualizes the exact decision flow and actions executed by `shelly_dynamic_threshold.yaml`.

View in VS Code with a Mermaid preview extension or paste the mermaid block into https://mermaid.live.

```mermaid
flowchart TB
  %% Nodes
  Start((Start))
  Trigger[/Trigger: sensor change | time(05:00,08:00) | HA start/]
  EvalVars[[Evaluate variables\n- battery = float(states('sensor.deye_battery') | default(0))\n- window_a = now().hour >=5 and now().hour <8\n- on_threshold = 50 if window_a else 75\n- off_threshold = 20 if window_a else 60]]
  D1{battery >= on_threshold?}
  D1b{switch.shelly1pm == 'off'?}
  ActionOn[/Action: switch.turn_on\nNotify: "Shelly Activated"/]
  D2{battery <= off_threshold?}
  D2b{switch.shelly1pm == 'on'?}
  ActionOff[/Action: switch.turn_off\nNotify: "Shelly Deactivated"/]
  NoAction["No action — conditions not met"]
  End((End))

  %% Flow
  Start --> Trigger --> EvalVars --> D1
  D1 -- Yes --> D1b
  D1b -- Yes --> ActionOn --> End
  D1b -- No --> D2
  D1 -- No --> D2
  D2 -- Yes --> D2b
  D2b -- Yes --> ActionOff --> End
  D2b -- No --> NoAction --> End
  D2 -- No --> NoAction --> End

  %% Notes / edge cases
  classDef note fill:#f9f,stroke:#333,stroke-width:1px;
  BatteryNote["Note: If sensor missing or non-numeric, battery coerces to 0"]
  ModeNote["Automation mode: single — concurrent runs prevented"]
  BatteryNote:::note
  ModeNote:::note
  EvalVars --> BatteryNote
  Trigger --> ModeNote

``` 

## Pseudocode (equivalent)

```text
battery = float(states('sensor.deye_battery') or 0)
window_a = (now().hour >= 5) and (now().hour < 8)
on_threshold = 50 if window_a else 75
off_threshold = 20 if window_a else 60

if battery >= on_threshold and states('switch.shelly1pm') == 'off':
    call service switch.turn_on
    notify("Shelly Activated", details)
elif battery <= off_threshold and states('switch.shelly1pm') == 'on':
    call service switch.turn_off
    notify("Shelly Deactivated", details)
else:
    # No action
    pass
```

If you want a PNG/SVG export of this diagram, I can render it and add the image file to the repo.
