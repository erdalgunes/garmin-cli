#!/usr/bin/env python3
"""
Garmin Development CLI - Micro-kernel Architecture
A modular, extensible CLI for Garmin Connect IQ development

Usage:
  garmin-dev <command> [options]
  
Philosophy:
  - UNIX: Do one thing well, compose tools
  - Modular: Plugin-based architecture  
  - Progressive: CLI → TUI → GUI → IDE
  - Developer-first: Fast, scriptable, automation-friendly
"""

import sys
import os
import json
import argparse
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class GarminDevCore:
    """Core CLI framework with plugin system"""
    
    def __init__(self):
        self.version = "0.1.0"
        self.plugins = {}
        self.config = {}
        self.load_config()
        self.discover_plugins()
    
    def load_config(self):
        """Load configuration from various sources"""
        config_paths = [
            Path.cwd() / ".garmin-dev.json",
            Path.home() / ".garmin-dev.json", 
            Path("/etc/garmin-dev.json")
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        self.config.update(json.load(f))
                    break
                except Exception as e:
                    print(f"Warning: Failed to load config {config_path}: {e}")
        
        # Default configuration
        if not self.config:
            self.config = {
                "default_device": "fenix7",
                "sdk_path": self._find_garmin_sdk(),
                "output_format": "text",
                "verbose": False
            }
    
    def _find_garmin_sdk(self) -> Optional[str]:
        """Auto-detect Garmin SDK installation"""
        common_paths = [
            "/Users/erdalgunes/Library/Application Support/Garmin/ConnectIQ/Sdks",
            "~/Library/Application Support/Garmin/ConnectIQ/Sdks",
            "/opt/garmin-sdk",
            "/usr/local/garmin-sdk"
        ]
        
        for path in common_paths:
            expanded = Path(path).expanduser()
            if expanded.exists():
                # Find latest SDK version
                sdk_dirs = [d for d in expanded.iterdir() if d.is_dir()]
                if sdk_dirs:
                    latest_sdk = sorted(sdk_dirs)[-1]
                    return str(latest_sdk)
        return None
    
    def discover_plugins(self):
        """Discover and load available plugins"""
        # Built-in plugins
        builtin_plugins = {
            "ui-capture": "UI state capture and XML generation",
            "build": "MonkeyC compilation and optimization", 
            "deploy": "Device deployment and simulator management",
            "test": "Testing framework and validation",
            "debug": "Debugging tools and log analysis",
            "device": "Device management and information",
            "project": "Project scaffolding and management"
        }
        
        for name, description in builtin_plugins.items():
            self.plugins[name] = {
                "name": name,
                "description": description, 
                "type": "builtin",
                "module": f"garmin_dev.plugins.{name.replace('-', '_')}"
            }
    
    def list_plugins(self):
        """List available plugins"""
        print("Available plugins:")
        for name, info in self.plugins.items():
            status = "✓" if self._plugin_available(name) else "✗"
            print(f"  {status} {name:<12} - {info['description']}")
    
    def _plugin_available(self, plugin_name: str) -> bool:
        """Check if plugin is available/installed"""
        # For now, assume all builtin plugins are available
        return True
    
    def run_plugin(self, plugin_name: str, args: List[str]) -> int:
        """Execute a plugin with given arguments"""
        if plugin_name not in self.plugins:
            print(f"Error: Unknown plugin '{plugin_name}'")
            print(f"Available plugins: {', '.join(self.plugins.keys())}")
            return 1
        
        plugin_info = self.plugins[plugin_name]
        
        try:
            # Load and execute plugin
            return self._execute_plugin(plugin_name, args)
        except Exception as e:
            print(f"Error executing plugin '{plugin_name}': {e}")
            return 1
    
    def _execute_plugin(self, plugin_name: str, args: List[str]) -> int:
        """Execute specific plugin logic"""
        
        if plugin_name == "ui-capture":
            return self._ui_capture_plugin(args)
        elif plugin_name == "build":
            return self._build_plugin(args)
        elif plugin_name == "deploy":
            return self._deploy_plugin(args)
        elif plugin_name == "device":
            return self._device_plugin(args)
        elif plugin_name == "debug":
            return self._debug_plugin(args)
        else:
            print(f"Plugin '{plugin_name}' not implemented yet")
            return 1
    
    def _ui_capture_plugin(self, args: List[str]) -> int:
        """UI capture plugin - XML generation from debug logs"""
        parser = argparse.ArgumentParser(prog="garmin-dev ui-capture")
        parser.add_argument("--input", "-i", help="Input log file (default: stdin)")
        parser.add_argument("--output", "-o", default="ui-state.xml", help="Output XML file")
        parser.add_argument("--format", "-f", choices=["xml", "json"], default="xml", help="Output format")
        parser.add_argument("--device", "-d", help="Target device")
        
        parsed_args = parser.parse_args(args)
        
        print(f"🎯 UI Capture Plugin")
        print(f"Input: {parsed_args.input or 'stdin'}")
        print(f"Output: {parsed_args.output}")
        print(f"Format: {parsed_args.format}")
        print(f"Device: {parsed_args.device or self.config.get('default_device', 'auto-detect')}")
        
        # Import the UI capture logic
        import re
        import json
        from datetime import datetime
        
        try:
            # Read input
            if parsed_args.input:
                with open(parsed_args.input, 'r') as f:
                    log_content = f.read()
            else:
                import sys
                log_content = sys.stdin.read()
            
            # Parse debug logs into canonical format
            ui_state = self._parse_debug_logs(log_content, parsed_args.device)
            
            if parsed_args.format == "xml":
                # Convert to XML
                xml_content = self._generate_xml(ui_state)
                with open(parsed_args.output, 'w') as f:
                    f.write(xml_content)
                print(f"✅ XML UI state saved to: {parsed_args.output}")
            else:
                # Save as JSON
                with open(parsed_args.output, 'w') as f:
                    json.dump(ui_state, f, indent=2)
                print(f"✅ JSON UI state saved to: {parsed_args.output}")
            
            element_count = len(ui_state.get('elements', []))
            print(f"📊 Captured {element_count} UI elements")
            
            return 0
            
        except Exception as e:
            print(f"❌ Error processing logs: {e}")
            return 1
    
    def _build_plugin(self, args: List[str]) -> int:
        """Build plugin - MonkeyC compilation"""
        parser = argparse.ArgumentParser(prog="garmin-dev build")
        parser.add_argument("--device", "-d", help="Target device")
        parser.add_argument("--output", "-o", help="Output file")
        parser.add_argument("--optimize", "-O", action="store_true", help="Optimize build")
        
        parsed_args = parser.parse_args(args)
        
        print(f"🔨 Build Plugin")
        print(f"Device: {parsed_args.device or self.config.get('default_device')}")
        print(f"Optimize: {parsed_args.optimize}")
        
        # TODO: Implement build logic using monkeyc
        print("✅ Build plugin executed (implementation pending)")
        return 0
    
    def _deploy_plugin(self, args: List[str]) -> int:
        """Deploy plugin - Device/simulator deployment"""
        parser = argparse.ArgumentParser(prog="garmin-dev deploy")
        parser.add_argument("executable", help="Executable file to deploy")
        parser.add_argument("--device", "-d", help="Target device")
        parser.add_argument("--simulator", "-s", action="store_true", help="Deploy to simulator")
        
        parsed_args = parser.parse_args(args)
        
        print(f"🚀 Deploy Plugin")
        print(f"Executable: {parsed_args.executable}")
        print(f"Target: {'simulator' if parsed_args.simulator else 'device'}")
        
        # TODO: Implement deployment using monkeydo
        print("✅ Deploy plugin executed (implementation pending)")
        return 0
    
    def _device_plugin(self, args: List[str]) -> int:
        """Device plugin - Device management"""
        if not args or args[0] == "list":
            print("📱 Supported Devices:")
            devices = [
                "fenix7", "fenix7s", "fenix7x", "fr965", "fr955", 
                "epix2", "venu2", "vivoactive4", "edge1040"
            ]
            for device in devices:
                print(f"  • {device}")
        else:
            print(f"Device command '{args[0]}' not implemented")
        
        return 0
    
    def _debug_plugin(self, args: List[str]) -> int:
        """Debug plugin - Log analysis and debugging"""
        print("🐛 Debug Plugin")
        print("Available debug commands:")
        print("  • analyze-logs - Analyze debug log patterns")
        print("  • performance - Performance analysis")
        print("  • errors - Error detection and reporting")
        
        return 0
    
    def _parse_debug_logs(self, log_content: str, device: Optional[str]) -> Dict[str, Any]:
        """Parse debug logs into canonical UI state format"""
        import re
        from datetime import datetime
        
        # Regex patterns for parsing debug logs
        patterns = {
            'screen': re.compile(r'\[.*?\] RENDER: Screen\((\d+)x(\d+)\) Center\((\d+),(\d+)\)'),
            'text': re.compile(r'\[.*?\] RENDER: (\w+)\(([^)]+)\) Position\((\d+),(\d+)\) Font\((\w+)\) Color\((0x[0-9a-fA-F]+)\)'),
            'circle': re.compile(r'\[.*?\] RENDER: (\w+)\(([^)]+)\) Position\((\d+),(\d+)\) Size\(([0-9.]+)\) Color\((0x[0-9a-fA-F]+)\)'),
            'rect': re.compile(r'\[.*?\] RENDER: (\w+)(?:\(([^)]+)\))? Position\((\d+),(\d+)\) Size\((\d+)x(\d+)\) Color\((0x[0-9a-fA-F]+)\)'),
            'layout': re.compile(r'\[.*?\] LAYOUT: (\w+)\(([^)]+)\)'),
            'state': re.compile(r'\[.*?\] STATE: (\w+)\(([^)]+)\)')
        }
        
        # Initialize UI state
        ui_state = {
            "version": "1.0",
            "metadata": {
                "app_name": "Garmin App",
                "device_model": device or "fenix7",
                "screen_width": 260,
                "screen_height": 260,
                "timestamp": datetime.now().isoformat() + "Z",
                "capture_source": "debug_logs"
            },
            "screen": {
                "background_color": "#000000",
                "scale_factor": 1.0,
                "center_x": 130,
                "center_y": 130
            },
            "elements": [],
            "state": {}
        }
        
        # Parse screen dimensions
        screen_match = patterns['screen'].search(log_content)
        if screen_match:
            width, height, center_x, center_y = screen_match.groups()
            ui_state["metadata"]["screen_width"] = int(width)
            ui_state["metadata"]["screen_height"] = int(height)
            ui_state["screen"]["center_x"] = int(center_x)
            ui_state["screen"]["center_y"] = int(center_y)
        
        # Parse UI elements
        element_id = 1
        
        # Parse text elements
        for match in patterns['text'].finditer(log_content):
            name, content, x, y, font, color = match.groups()
            element = {
                "id": f"{name.lower()}_{element_id}",
                "type": "text",
                "x": int(x),
                "y": int(y),
                "text_content": content,
                "font_family": font.lower(),
                "font_size": self._get_font_size(font),
                "font_weight": "bold" if "LARGE" in font else "normal",
                "fill_color": self._hex_color_convert(color),
                "text_anchor": "middle",
                "z_index": 10,
                "visible": True,
                "opacity": 1.0
            }
            ui_state["elements"].append(element)
            element_id += 1
        
        # Parse circle elements  
        for match in patterns['circle'].finditer(log_content):
            name, content, x, y, size, color = match.groups()
            element = {
                "id": f"{name.lower()}_{element_id}",
                "type": "circle",
                "x": int(x),
                "y": int(y),
                "radius": float(size),
                "fill_color": self._hex_color_convert(color),
                "z_index": 5,
                "visible": True,
                "opacity": 1.0
            }
            ui_state["elements"].append(element)
            element_id += 1
        
        # Parse rectangle elements
        for match in patterns['rect'].finditer(log_content):
            groups = match.groups()
            name = groups[0]
            content = groups[1] if groups[1] else ""  # May be None
            x, y, width, height, color = groups[2], groups[3], groups[4], groups[5], groups[6]
            element = {
                "id": f"{name.lower()}_{element_id}",
                "type": "rect",
                "x": int(x),
                "y": int(y),
                "width": int(width),
                "height": int(height),
                "fill_color": self._hex_color_convert(color),
                "z_index": 8,
                "visible": True,
                "opacity": 1.0
            }
            ui_state["elements"].append(element)
            element_id += 1
        
        return ui_state
    
    def _get_font_size(self, font: str) -> int:
        """Convert Garmin font names to pixel sizes"""
        font_sizes = {
            "LARGE": 24,
            "MEDIUM": 18,
            "SMALL": 14,
            "XTINY": 10
        }
        return font_sizes.get(font.upper(), 16)
    
    def _hex_color_convert(self, garmin_color: str) -> str:
        """Convert Garmin hex color to standard hex"""
        if garmin_color.startswith('0x'):
            return '#' + garmin_color[2:].zfill(6)
        return garmin_color
    
    def _generate_xml(self, ui_state: Dict[str, Any]) -> str:
        """Generate XML representation of UI state"""
        metadata = ui_state['metadata']
        screen = ui_state['screen']
        elements = ui_state['elements']
        
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<garmin-ui-state version="{ui_state["version"]}">',
            '  <metadata>',
            f'    <app-name>{metadata["app_name"]}</app-name>',
            f'    <device-model>{metadata["device_model"]}</device-model>',
            f'    <screen-width>{metadata["screen_width"]}</screen-width>',
            f'    <screen-height>{metadata["screen_height"]}</screen-height>',
            f'    <timestamp>{metadata["timestamp"]}</timestamp>',
            f'    <capture-source>{metadata["capture_source"]}</capture-source>',
            '  </metadata>',
            '  <screen>',
            f'    <background-color>{screen["background_color"]}</background-color>',
            f'    <scale-factor>{screen["scale_factor"]}</scale-factor>',
            f'    <center-x>{screen["center_x"]}</center-x>',
            f'    <center-y>{screen["center_y"]}</center-y>',
            '  </screen>',
            '  <elements>'
        ]
        
        # Sort elements by z-index
        sorted_elements = sorted(elements, key=lambda x: x.get('z_index', 0))
        
        for element in sorted_elements:
            xml_lines.append(f'    <element id="{element["id"]}" type="{element["type"]}">')
            xml_lines.append(f'      <position x="{element["x"]}" y="{element["y"]}"/>')
            
            if element["type"] == "text":
                xml_lines.append(f'      <text-content>{element.get("text_content", "")}</text-content>')
                xml_lines.append(f'      <font-family>{element.get("font_family", "")}</font-family>')
                xml_lines.append(f'      <font-size>{element.get("font_size", 16)}</font-size>')
                xml_lines.append(f'      <font-weight>{element.get("font_weight", "normal")}</font-weight>')
                xml_lines.append(f'      <text-anchor>{element.get("text_anchor", "start")}</text-anchor>')
            elif element["type"] == "circle":
                xml_lines.append(f'      <radius>{element.get("radius", 5)}</radius>')
            elif element["type"] == "rect":
                xml_lines.append(f'      <dimensions width="{element.get("width", 10)}" height="{element.get("height", 10)}"/>')
            
            xml_lines.append(f'      <fill-color>{element.get("fill_color", "#000000")}</fill-color>')
            xml_lines.append(f'      <z-index>{element.get("z_index", 0)}</z-index>')
            xml_lines.append(f'      <visible>{str(element.get("visible", True)).lower()}</visible>')
            xml_lines.append(f'      <opacity>{element.get("opacity", 1.0)}</opacity>')
            xml_lines.append('    </element>')
        
        xml_lines.extend([
            '  </elements>',
            '</garmin-ui-state>'
        ])
        
        return '\n'.join(xml_lines)

def main():
    """Main CLI entry point"""
    
    # Initialize core
    core = GarminDevCore()
    
    # Parse global arguments
    parser = argparse.ArgumentParser(
        prog="garmin-dev",
        description="Garmin Connect IQ Development CLI",
        add_help=False  # We'll handle help manually
    )
    
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("--version", "-V", action="store_true", help="Show version")
    parser.add_argument("--list-plugins", "-L", action="store_true", help="List available plugins")
    parser.add_argument("--config", "-c", help="Config file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output") 
    parser.add_argument("--json", action="store_true", help="JSON output format")
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    
    # Parse known args to allow plugin-specific arguments
    args, remaining = parser.parse_known_args()
    
    # Handle global options
    if args.version:
        print(f"garmin-dev {core.version}")
        return 0
    
    if args.list_plugins:
        core.list_plugins()
        return 0
    
    if args.help or not args.command:
        print(f"Garmin Connect IQ Development CLI v{core.version}")
        print("A micro-kernel CLI for Garmin development")
        print()
        print("Usage: garmin-dev <command> [options]")
        print()
        print("Commands:")
        for name, info in core.plugins.items():
            print(f"  {name:<12} {info['description']}")
        print()
        print("Global Options:")
        print("  --version, -V       Show version")
        print("  --list-plugins, -L  List available plugins") 
        print("  --config, -c        Config file path")
        print("  --verbose, -v       Verbose output")
        print("  --json              JSON output format")
        print("  --help, -h          Show help")
        print()
        print("Examples:")
        print("  garmin-dev ui-capture --input debug.log --output ui-state.xml")
        print("  garmin-dev build --device fenix7 --optimize")
        print("  garmin-dev deploy app.prg --simulator")
        print()
        print("🚀 Micro-kernel architecture: CLI → TUI → GUI → IDE")
        return 0
    
    # Execute plugin
    return core.run_plugin(args.command, remaining)

if __name__ == "__main__":
    sys.exit(main())