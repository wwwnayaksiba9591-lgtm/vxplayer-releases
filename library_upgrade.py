exec(PathCode if False else 'from pathlib import Path')
p=Path(r'C:\dev\VXPlayer');src=p/'app/src/main/java/com/vxplayer'
def edit(file,old,new):
 f=src/file;t=f.read_text();assert old in t,(file,old[:60]);f.write_text(t.replace(old,new))
edit('library/LibraryScreen.kt','import androidx.compose.ui.draw.clip','import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.input.nestedscroll.nestedScroll\nimport androidx.compose.foundation.shape.CircleShape\nimport androidx.compose.animation.core.animateFloatAsState')
edit('library/LibraryScreen.kt','    // Migrate a restored selection from the removed Videos tab to Folders.\n    LaunchedEffect(tab) { if (tab == 1) tab = 0 }','    val topBar = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()')
edit('library/LibraryScreen.kt','Column(Modifier.safeDrawingPadding())','Column(Modifier.safeDrawingPadding().nestedScroll(topBar.nestedScrollConnection))')
edit('library/LibraryScreen.kt','if (tab != 3) TopAppBar(','if (tab != 3) LargeTopAppBar(scrollBehavior=topBar,')
edit('library/LibraryScreen.kt','if (search && tab != 3) OutlinedTextField','if (tab in 0..2) OutlinedTextField')
edit('library/LibraryScreen.kt','label = { Text("Search videos or folders") }','placeholder = { Text("Search your library") }, leadingIcon = { Icon(Icons.Default.Search,null) }, shape = CircleShape')
edit('library/LibraryScreen.kt','padding(horizontal = 12.dp), singleLine','padding(horizontal = VXSpace.large, vertical = VXSpace.small), singleLine')
edit('library/LibraryScreen.kt','            if (tab in 0..2) Row','''            if (selectedFolder == null && tab in 0..3) SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth().padding(horizontal=VXSpace.large)) {
                listOf(1 to "Videos",0 to "Folders",3 to "Music").forEachIndexed { index,(value,label) ->
                    SegmentedButton(selected=tab==value,onClick={tab=value;selectedFolder=null},shape=SegmentedButtonDefaults.itemShape(index,3)) { Text(label) }
                }
            }
            if (tab in 0..2) Row''')
edit('library/LibraryScreen.kt','tween(160)','tween(VXMotion.Standard)')
edit('library/LibraryScreen.kt','state.loading && state.folders.isEmpty() -> Column(Modifier.fillMaxSize(), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically)) { CircularProgressIndicator(); Text("Finding videos…") }','state.loading && state.folders.isEmpty() -> LibrarySkeleton()')
edit('library/LibraryScreen.kt','Triple(0,"Folders",Icons.Default.Folder)','Triple(1,"Videos",Icons.Default.Movie),Triple(0,"Folders",Icons.Default.Folder)')
edit('library/LibraryScreen.kt','modifier = Modifier.fillMaxWidth()) {\n                                    Row','modifier = Modifier.fillMaxWidth().animateItem()) {\n                                    Row')
edit('library/LibraryScreen.kt','VXCard(onClick = { onVideoClick(video, video.folderKey) })','VXCard(onClick = { onVideoClick(video, video.folderKey) }, modifier=Modifier.animateItem())')
edit('library/LibraryScreen.kt','VideoRow(video, onClick =','VideoRow(video, modifier=Modifier.animateItem(), onClick =')
edit('library/LibraryScreen.kt','fun VideoRow(video: Video, onClick:','fun VideoRow(video: Video, modifier: Modifier = Modifier, onClick:')
edit('library/LibraryScreen.kt','VXCard(onClick = onClick, modifier = Modifier.fillMaxWidth())','VXCard(onClick = onClick, modifier = modifier.fillMaxWidth())')
edit('library/LibraryScreen.kt','    Icon(Icons.Default.Folder, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(44.dp))','    LibraryIllustration(Modifier.size(80.dp))')
edit('library/LibraryScreen.kt','    Column(modifier.clip(VXShapes.small))','    val imageAlpha by animateFloatAsState(if(bitmap==null)0f else 1f,tween(VXMotion.Standard),label="Thumbnail reveal")\n    Column(modifier.clip(VXShapes.medium))')
edit('library/LibraryScreen.kt','Modifier.fillMaxSize(), contentScale = ContentScale.Crop','Modifier.fillMaxSize().graphicsLayer { alpha=imageAlpha }, contentScale = ContentScale.Crop')
edit('library/LibraryScreen.kt','if (video.positionMs > 0L && video.durationMs > 0L) LinearProgressIndicator(\n            progress = { (video.positionMs.toFloat() / video.durationMs).coerceIn(0f, 1f) }, modifier = Modifier.fillMaxWidth().height(2.dp))','if (video.positionMs > 0L && video.durationMs > 0L) VXProgress({ (video.positionMs.toFloat()/video.durationMs).coerceIn(0f,1f) })')
(src/'ui/LibraryPresentation.kt').write_text('''package com.vxplayer.ui

import android.database.ContentObserver
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.*
import androidx.compose.ui.graphics.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp

@Composable
fun rememberVXMotionEnabled(): Boolean {
    val resolver=LocalContext.current.contentResolver
    fun enabled()=Settings.Global.getFloat(resolver,Settings.Global.ANIMATOR_DURATION_SCALE,1f)>0f
    var value by remember {mutableStateOf(enabled())}
    DisposableEffect(resolver) {
        val observer=object: ContentObserver(Handler(Looper.getMainLooper())) {override fun onChange(selfChange:Boolean) {value=enabled()}}
        resolver.registerContentObserver(Settings.Global.getUriFor(Settings.Global.ANIMATOR_DURATION_SCALE),false,observer)
        onDispose {resolver.unregisterContentObserver(observer)}
    }
    return value
}

@Composable
fun VXProgress(progress: ()->Float, modifier: Modifier=Modifier) {
    val track=MaterialTheme.colorScheme.outlineVariant
    Canvas(modifier.fillMaxWidth().height(2.dp)) {
        drawRect(track)
        drawRect(VXBrand.gradient,size=Size(size.width*progress().coerceIn(0f,1f),size.height))
    }
}

@Composable
fun LibraryIllustration(modifier:Modifier=Modifier) {
    val base=MaterialTheme.colorScheme.primaryContainer
    val accent=MaterialTheme.colorScheme.primary
    Canvas(modifier) {
        drawCircle(accent.copy(alpha=.08f))
        drawRoundRect(base,Offset(size.width*.12f,size.height*.24f),Size(size.width*.76f,size.height*.55f),CornerRadius(12.dp.toPx()))
        drawRoundRect(accent.copy(alpha=.45f),Offset(size.width*.18f,size.height*.18f),Size(size.width*.32f,size.height*.16f),CornerRadius(4.dp.toPx()))
        val play=Path().apply {moveTo(size.width*.44f,size.height*.39f);lineTo(size.width*.44f,size.height*.65f);lineTo(size.width*.65f,size.height*.52f);close()}
        drawPath(play,accent)
    }
}

@Composable
fun LibrarySkeleton() {
    val motion=rememberVXMotionEnabled()
    val phase=if(motion) {
        val transition=rememberInfiniteTransition(label="Library loading")
        transition.animateFloat(-1f,2f,infiniteRepeatable(tween(1200,easing=LinearEasing)),label="Shimmer")
    } else remember {mutableFloatStateOf(0f)}
    val surface=MaterialTheme.colorScheme.surfaceContainerHigh
    val shine=MaterialTheme.colorScheme.onSurface.copy(alpha=.06f)
    Column(Modifier.fillMaxSize().padding(VXSpace.large).semantics {contentDescription="Finding your videos"},verticalArrangement=Arrangement.spacedBy(VXSpace.large)) {
        repeat(5) {
            Canvas(Modifier.fillMaxWidth().height(96.dp).clip(VXShapes.medium).background(surface)) {
                val x=phase.value*size.width
                drawRect(Brush.linearGradient(listOf(Color.Transparent,shine,Color.Transparent),Offset(x-size.width*.5f,0f),Offset(x+size.width*.5f,size.height)))
            }
        }
    }
}
''')
print('Library presentation applied')
