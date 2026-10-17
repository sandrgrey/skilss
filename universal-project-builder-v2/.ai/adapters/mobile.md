# Adapter: Mobile (native or cross-platform)

**Enable:** architecture, design-system, security; add backend-data for remote APIs.

Choose SwiftUI, Android-native or cross-platform based on target platforms, toolchains and user constraints. Confirm signing/build environment before promising distributable IPA/APK.

Account for touch sizes, safe areas, keyboard appearance, navigation lifecycle, permissions, background behavior, network loss, offline state and accessibility settings.

If working on Windows for iOS, distinguish code authoring from signed iOS builds that typically require compatible Apple tooling or an authorized cloud build service.

Test on available emulator/simulator/device; do not claim device verification without evidence.
