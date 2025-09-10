# Garmin Development CLI

A micro-kernel CLI for Garmin Connect IQ development that can evolve into a full IDE.

## Features

- **Universal UI Capture**: Extract semantic UI state from debug logs (since Garmin blocks screenshots)
- **Micro-kernel Architecture**: Plugin-based system following UNIX philosophy
- **Progressive Enhancement**: CLI → TUI → GUI → IDE evolution path
- **Device-Agnostic**: Works across all Garmin device families
- **MonkeyC Integration**: Native support for Garmin's MonkeyC language

## Installation

```bash
pip install garmin-dev-cli
```

## Quick Start

```bash
# Capture UI state from debug logs
garmin-dev ui-capture --input debug.log --output ui-state.xml

# List supported devices
garmin-dev device list

# Show all available plugins
garmin-dev --list-plugins

# Get help for specific plugin
garmin-dev ui-capture --help
```

## Architecture

### Micro-kernel Design
The CLI follows a micro-kernel architecture where each plugin does one thing well:

- **ui-capture**: UI state capture and XML generation
- **build**: MonkeyC compilation and optimization  
- **deploy**: Device deployment and simulator management
- **test**: Testing framework and validation
- **debug**: Debugging tools and log analysis
- **device**: Device management and information
- **project**: Project scaffolding and management

### Plugin System
```python
# Example plugin usage
garmin-dev ui-capture --input simulator.log --format xml
garmin-dev build --device fenix7 --optimize
garmin-dev deploy app.prg --simulator
```

## UI Capture System

The unique value proposition is universal UI capture from debug logs:

```mc
// In your MonkeyC watch face
System.println("[Jailbot] RENDER: HourNumber(15) Position(240,130) Font(LARGE) Color(0x00ff00)");
System.println("[Jailbot] RENDER: Circle Position(130,25) Size(1.5) Color(0x00ff00)");
```

This generates structured XML:
```xml
<garmin-ui-state version="1.0">
  <elements>
    <element id="hournumber_1" type="text">
      <position x="240" y="130"/>
      <text-content>15</text-content>
      <font-size>24</font-size>
      <fill-color>#00ff00</fill-color>
    </element>
  </elements>
</garmin-ui-state>
```

## Development Roadmap

### Phase 1: CLI Foundation ✅
- [x] Micro-kernel architecture with plugin system
- [x] XML UI capture from debug logs
- [x] Command-line interface with help system

### Phase 2: Enhanced CLI Plugins  
- [ ] Build plugin with MonkeyC compilation
- [ ] Deploy plugin with device management
- [ ] Test plugin with validation framework
- [ ] Debug plugin with log analysis

### Phase 3: TUI (Terminal User Interface)
- [ ] Interactive mode with real-time feedback
- [ ] Visual device selection and project browser
- [ ] Live log viewer with filtering

### Phase 4: GUI Application
- [ ] Desktop app with visual project management
- [ ] WYSIWYG watch face designer
- [ ] Performance visualization dashboard

### Phase 5: Full IDE
- [ ] MonkeyC language server with IntelliSense
- [ ] Visual debugger with variable inspection
- [ ] Connect IQ Store publishing workflow

## Configuration

The CLI auto-detects your Garmin SDK installation and uses sensible defaults:

```json
{
  "default_device": "fenix7",
  "sdk_path": "/path/to/connectiq-sdk",
  "output_format": "xml",
  "verbose": false
}
```

Configuration files are searched in:
- `./.garmin-dev.json` (project-specific)
- `~/.garmin-dev.json` (user-specific)  
- `/etc/garmin-dev.json` (system-wide)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the micro-kernel philosophy
4. Add tests for new plugins
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Philosophy

> Do one thing well, compose tools, progressive enhancement from CLI to IDE.

This tool follows UNIX philosophy while providing a clear evolution path toward sophisticated GUI development environments.