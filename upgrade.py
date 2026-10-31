from pathlib import Path
p=Path(r'C:\dev\VXPlayer')
src=p/'app/src/main/java/com/vxplayer'
def edit(file, old, new):
    f=src/file
    text=f.read_text(encoding='utf-8')
    assert old in text, (file,old[:70])
    f.write_text(text.replace(old,new),encoding='utf-8')
edit('ui/DesignSystem.kt','import androidx.compose.foundation.interaction.MutableInteractionSource','import androidx.compose.foundation.BorderStroke\nimport androidx.compose.animation.core.FastOutSlowInEasing\nimport androidx.compose.animation.core.LinearOutSlowInEasing\nimport androidx.compose.animation.core.tween\nimport androidx.compose.ui.graphics.Brush\nimport androidx.compose.ui.text.font.Font\nimport androidx.compose.ui.text.font.FontFamily\nimport com.vxplayer.R\nimport androidx.compose.foundation.interaction.MutableInteractionSource')
edit('ui/DesignSystem.kt','val VXTypography = Typography(','''object VXMotion {
    const val Quick = 120
    const val Standard = 200
    const val Emphasis = 320
    val Enter = LinearOutSlowInEasing
    val Move = FastOutSlowInEasing
}
object VXSize {
    val touch = 48.dp
    val icon = 24.dp
    val card = 20.dp
    val sheet = 28.dp
    val border = 1.dp
}
object VXBrand {
    val Blue = androidx.compose.ui.graphics.Color(0xFF79B8FF)
    val Violet = androidx.compose.ui.graphics.Color(0xFFBFA3FF)
    val gradient = Brush.linearGradient(listOf(Blue, Violet))
}
private val VXFont = FontFamily(
    Font(R.font.plus_jakarta_sans, FontWeight.Normal),
    Font(R.font.plus_jakarta_sans, FontWeight.Medium),
    Font(R.font.plus_jakarta_sans, FontWeight.SemiBold),
    Font(R.font.plus_jakarta_sans, FontWeight.Bold),
)
private val BaseTypography = Typography(''')
edit('ui/DesignSystem.kt','@Composable\nfun VXIconButton','''val VXTypography = BaseTypography.let { t ->
    fun TextStyle.brand() = copy(fontFamily = VXFont)
    Typography(
        displayLarge=t.displayLarge.brand(), displayMedium=t.displayMedium.brand(), displaySmall=t.displaySmall.brand(),
        headlineLarge=t.headlineLarge.brand().copy(fontWeight=FontWeight.Bold), headlineMedium=t.headlineMedium.brand().copy(fontWeight=FontWeight.Bold), headlineSmall=t.headlineSmall.brand(),
        titleLarge=t.titleLarge.brand(), titleMedium=t.titleMedium.brand(), titleSmall=t.titleSmall.brand(),
        bodyLarge=t.bodyLarge.brand(), bodyMedium=t.bodyMedium.brand(), bodySmall=t.bodySmall.brand(),
        labelLarge=t.labelLarge.brand(), labelMedium=t.labelMedium.brand().copy(fontFeatureSettings="tnum"), labelSmall=t.labelSmall.brand().copy(fontFeatureSettings="tnum")
    )
}

@Composable
fun VXIconButton''')
edit('ui/DesignSystem.kt','if (pressed) .985f else 1f, label','if (pressed) .985f else 1f, animationSpec = tween(VXMotion.Quick, easing = VXMotion.Move), label')
edit('ui/DesignSystem.kt','elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),','border = BorderStroke(VXSize.border, MaterialTheme.colorScheme.outlineVariant.copy(alpha=.4f)),\n        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),')
edit('ui/DesignSystem.kt','medium = RoundedCornerShape(16.dp)','medium = RoundedCornerShape(20.dp)')
edit('settings/AppSettings.kt','val theme: String = "System"','val theme: String = "AMOLED"')
edit('settings/AppSettings.kt','val accent: String = "Orange"','val haptics: Boolean = true, val accent: String = "Blue"')
edit('settings/AppSettings.kt','data class PlaybackDefaults','@androidx.compose.runtime.Immutable\ndata class PlaybackDefaults')
edit('settings/AppSettings.kt','.putString("playbackMode", value.playbackMode.name)','.putBoolean("haptics",value.haptics).putString("playbackMode", value.playbackMode.name)')
edit('settings/SettingsParser.kt','listOf("System","Light","Dark"), "System"','listOf("System","Light","Dark","AMOLED"), "AMOLED"')
edit('settings/SettingsParser.kt','accent = choice','haptics = boolean(values["haptics"],true),\n        accent = choice')
edit('settings/SettingsParser.kt','"Purple"), "Orange"','"Purple"), "Blue"')
edit('settings/ThemePolicy.kt','System, Light, Dark','System, Light, Dark, AMOLED')
edit('settings/ThemePolicy.kt','ThemeMode.Dark.name -> true','ThemeMode.Dark.name, ThemeMode.AMOLED.name -> true')
edit('settings/VXTheme.kt','0xFF101720','0xFF080A10')
for a,b in [('0xFF0B1119','0xFF050609'),('0xFF17212D','0xFF11141D'),('0xFF1B2633','0xFF181C28'),('0xFF263240','0xFF222737'),('0xFF313E4D','0xFF2C3244')]:
    # Dark surface tokens only; retain light foreground contrast.
    f=src/'settings/VXTheme.kt';t=f.read_text();start=t.index('val VXDarkColors');t=t[:start]+t[start:].replace(a,b);f.write_text(t)
edit('settings/VXTheme.kt','val colors = if','val branded = if')
edit('settings/VXTheme.kt','    MaterialTheme(colorScheme = colors,','''    val colors = if (settings.theme == "AMOLED" && !playerMode) branded.copy(background=Color.Black,surface=Color.Black) else branded
    CompositionLocalProvider(com.vxplayer.ui.LocalVXHaptics provides settings.haptics) {
    MaterialTheme(colorScheme = colors,''')
edit('settings/VXTheme.kt','shapes = VXShapes, content = content)\n}','shapes = VXShapes, content = content)\n    }\n}')
edit('ui/DesignSystem.kt','@Composable\nfun VXIconButton','val LocalVXHaptics = staticCompositionLocalOf { true }\n\n@Composable\nfun VXIconButton')
edit('ui/DesignSystem.kt','    IconButton(onClick, enabled','''    val haptics = androidx.compose.ui.platform.LocalHapticFeedback.current
    val feedback = LocalVXHaptics.current
    IconButton({ if(feedback) haptics.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove); onClick() }, enabled''')
edit('settings/SettingsScreen.kt','listOf("System", "Light", "Dark")','listOf("Dark", "AMOLED", "Light", "System")')
edit('settings/SettingsScreen.kt','            val webPrefs=','''            Row(Modifier.fillMaxWidth(),verticalAlignment=Alignment.CenterVertically) {
                Text("Touch feedback",Modifier.weight(1f))
                Switch(settings.haptics,{ checked -> store.update {it.copy(haptics=checked)} })
            }
            val webPrefs=''')
print('Design system applied')
