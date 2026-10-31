from pathlib import Path
p=Path(r'C:\dev\VXPlayer');src=p/'app/src/main/java/com/vxplayer'
def edit(file,old,new):
 f=src/file;t=f.read_text();assert old in t,(file,old[:60]);f.write_text(t.replace(old,new))
edit('music/MusicScreen.kt','import com.vxplayer.ui.VXIconButton','import com.vxplayer.ui.*\nimport androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.geometry.Offset\nimport androidx.compose.ui.geometry.Size')
edit('music/MusicScreen.kt','else RoundedCornerShape(12.dp)','else VXShapes.medium')
edit('music/MusicScreen.kt','        art?.bitmap?.let { Image(it.asImageBitmap(),null,Modifier.fillMaxSize(),contentScale = scale) }\n            ?: Icon(Icons.Default.MusicNote,null,Modifier.fillMaxSize(.45f),tint = Color.White)','''        Crossfade(art?.bitmap,animationSpec=tween(VXMotion.Emphasis),label="Album art") { bitmap ->
            bitmap?.let { Image(it.asImageBitmap(),null,Modifier.fillMaxSize(),contentScale = scale) }
                ?: Icon(Icons.Default.MusicNote,null,Modifier.fillMaxSize(.45f),tint = MaterialTheme.colorScheme.onPrimaryContainer)
        }''')
old='''    val transition=rememberInfiniteTransition(label="Playing")
    val height by transition.animateFloat(.25f,1f,infiniteRepeatable(tween(450),RepeatMode.Reverse),label="bars")
    Row(Modifier.size(28.dp),verticalAlignment=Alignment.Bottom,horizontalArrangement=Arrangement.spacedBy(3.dp)) {
        repeat(3) { index -> Box(Modifier.width(4.dp).fillMaxHeight(if(index==1)height else 1.1f-height*.7f).background(MaterialTheme.colorScheme.primary,RoundedCornerShape(2.dp))) }
    }'''
new='''    val phase=if(rememberVXMotionEnabled()) {
        val transition=rememberInfiniteTransition(label="Playing")
        transition.animateFloat(.25f,1f,infiniteRepeatable(tween(450),RepeatMode.Reverse),label="bars")
    } else remember {mutableFloatStateOf(.65f)}
    val color=MaterialTheme.colorScheme.primary
    Canvas(Modifier.size(28.dp).semantics {contentDescription="Playing"}) {
        repeat(3) { index ->
            val height=size.height*(if(index==1)phase.value else 1.1f-phase.value*.7f)
            drawRoundRect(color,Offset(index*8.dp.toPx(),size.height-height),Size(4.dp.toPx(),height),androidx.compose.ui.geometry.CornerRadius(2.dp.toPx()))
        }
    }'''
edit('music/MusicScreen.kt',old,new)
edit('music/MusicScreen.kt','import androidx.compose.ui.window.Dialog','import androidx.compose.ui.semantics.semantics\nimport androidx.compose.ui.semantics.contentDescription\nimport androidx.compose.ui.window.Dialog')
edit('music/MusicScreen.kt','    var distance by remember {mutableFloatStateOf(0f)}','    val skipDistance=with(LocalDensity.current){60.dp.toPx()}\n    var distance by remember {mutableFloatStateOf(0f)}')
edit('music/MusicScreen.kt','Card(onClick={model.nowPlaying=true},modifier=','VXCard(onClick={model.nowPlaying=true},modifier=')
edit('music/MusicScreen.kt','if(abs(distance)>60)','if(abs(distance)>skipDistance)')
edit('music/MusicScreen.kt','    LinearProgressIndicator(progress={if(duration>0)(position.toFloat()/duration).coerceIn(0f,1f) else 0f},Modifier.fillMaxWidth().height(2.dp))','    VXProgress({if(duration>0)(position.toFloat()/duration).coerceIn(0f,1f) else 0f})')
edit('music/MusicPlayerOverlay.kt','import androidx.compose.ui.graphics.lerp','import androidx.compose.ui.graphics.lerp\nimport androidx.compose.ui.geometry.Offset\nimport androidx.compose.ui.draw.shadow\nimport androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.animation.core.*')
edit('music/MusicPlayerOverlay.kt','    var menu by remember','''    var entered by remember {mutableStateOf(false)}
    LaunchedEffect(Unit) {entered=true}
    val entrance=animateFloatAsState(if(entered)1f else 0f,tween(VXMotion.Emphasis,easing=VXMotion.Enter),label="Expand music")
    var menu by remember''')
edit('music/MusicPlayerOverlay.kt','.background(Brush.verticalGradient(listOf(background,Color.Black)))','.background(Brush.radialGradient(listOf(background,Color.Black),center=Offset(400f,300f),radius=1200f))')
edit('music/MusicPlayerOverlay.kt','Column(Modifier.fillMaxSize().safeDrawingPadding()','Column(Modifier.fillMaxSize().graphicsLayer {alpha=entrance.value;translationY=(1f-entrance.value)*32.dp.toPx();scaleX=.96f+entrance.value*.04f;scaleY=scaleX}.safeDrawingPadding()')
edit('music/MusicPlayerOverlay.kt','SongArt(model.current,Modifier.size(artworkSize))','SongArt(model.current,Modifier.size(artworkSize).shadow(12.dp,VXShapes.medium))')
edit('music/MusicPlayerOverlay.kt','else Icon(if(model.playing)Icons.Default.Pause else Icons.Default.PlayArrow,if(model.playing)"Pause" else "Play",Modifier.size(40.dp))','else VXPlayPauseIcon(model.playing,Modifier.size(40.dp))')
print('Music presentation applied')
