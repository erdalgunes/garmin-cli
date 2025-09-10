#!/bin/bash
# Garmin Dev CLI Demo Script

echo "🚀 Garmin Development CLI Demo"
echo "================================"
echo

echo "📋 CLI Information:"
garmin-dev --version
echo

echo "🔌 Available Plugins:"
garmin-dev --list-plugins
echo

echo "📱 Supported Devices:"
garmin-dev device list
echo

echo "🎯 UI Capture Demo:"
echo "Input: Enhanced debug log"
cat > demo_log.txt << 'EOF'
[Jailbot] INFO: DebugLogger initialized
[Jailbot] RENDER: Screen(260x260) Center(130,130)
[Jailbot] RENDER: HourNumber(12) Position(130,40) Font(LARGE) Color(0x00ff00)
[Jailbot] RENDER: MinuteMarker(30) Position(235,130) Size(2.0) Color(0xff0000)
[Jailbot] RENDER: JailbotEye(LEFT) Position(110,125) Size(8x3) Color(0x00ff00)
[Jailbot] RENDER: JailbotEye(RIGHT) Position(150,125) Size(8x3) Color(0x00ff00)
[Jailbot] STATE: CurrentTime(12:30) DisplayHour(12) MinuteAngle(90°)
[Jailbot] DEBUG: Memory: 15% (19000/126792)
[Jailbot] DEBUG: Battery: 85.0%
EOF

echo "Generating XML UI state..."
garmin-dev ui-capture --input demo_log.txt --output demo_ui.xml
echo

echo "📄 Generated XML:"
head -20 demo_ui.xml
echo "..."
echo

echo "🔄 Pipeline Demo (log → JSON):"
cat demo_log.txt | garmin-dev ui-capture --format json --output demo_ui.json
echo

echo "📊 JSON Structure:"
head -15 demo_ui.json
echo "..."
echo

echo "✅ Demo Complete!"
echo "   CLI installed as: $(which garmin-dev)"
echo "   Package structure: ./src/garmin_dev/"
echo "   Ready for development workflow integration"