from pathlib import Path
p=Path(r'C:\dev\VXPlayer');src=p/'app/src/main/java/com/vxplayer'
def edit(file,old,new):
 f=src/file;t=f.read_text();assert old in t,(file,old[:60]);f.write_text(t.replace(old,new))
edit('ui/PlayerControls.kt','import androidx.compose.foundation.background','import androidx.compose.foundation.BorderStroke\nimport androidx.compose.foundation.border\nimport androidx.compose.foundation.shape.RoundedCornerShape\nimport androidx.compose.ui.draw.clip\nimport androidx.compose.ui.graphics.Brush\nimport androidx.compose.foundation.background')
edit('ui/PlayerControls.kt','.width(maxWidth * .25f)','.width((maxWidth * .25f).coerceIn(104.dp,168.dp))')
edit('ui/PlayerControls.kt','.background(Color.Black.copy(alpha=.72f))','''.clip(RoundedCornerShape(topStart=VXSize.sheet,bottomStart=VXSize.sheet))
        .border(BorderStroke(VXSize.border,Brush.verticalGradient(listOf(VXBrand.Blue.copy(alpha=.35f),VXBrand.Violet.copy(alpha=.12f)))),RoundedCornerShape(topStart=VXSize.sheet,bottomStart=VXSize.sheet))
        .background(Brush.verticalGradient(listOf(Color(0xEF111725),Color(0xF0080B13))))''')
edit('ui/PlayerControls.kt','layout.order.filter {it !in layout.hidden}.forEach { item ->','''val motion = rememberVXMotionEnabled()
        layout.order.filter {it !in layout.hidden}.forEachIndexed { index,item ->
            val entrance=remember {androidx.compose.animation.core.Animatable(0f)}
            LaunchedEffect(open) {
                if(open) {
                    if(motion) {delay(index*16L);entrance.animateTo(1f,tween(VXMotion.Standard))} else entrance.snapTo(1f)
                } else entrance.snapTo(0f)
            }''')
edit('ui/PlayerControls.kt','Column(Modifier.width(80.dp),horizontalAlignment','Column(Modifier.width(96.dp).graphicsLayer {alpha=entrance.value;translationX=(1f-entrance.value)*16.dp.toPx()},horizontalAlignment')
edit('ui/PlayerControls.kt','color=if(item in active)Color(0xFF1565C0) else Color.White.copy(alpha=.12f)','color=Color.Transparent')
edit('ui/PlayerControls.kt','modifier=Modifier.size(48.dp).semantics','modifier=Modifier.size(VXSize.touch).clip(CircleShape).background(if(item in active)VXBrand.gradient else Brush.linearGradient(listOf(Color.White.copy(alpha=.12f),Color.White.copy(alpha=.08f)))).semantics')
edit('ui/PlayerControls.kt','tint=Color.White.copy(alpha=if(supported)1f else .38f)','tint=if(item in active)Color(0xFF08111E) else Color.White.copy(alpha=if(supported)1f else .38f)')
edit('ui/PlayerControls.kt','else Icon(if(playing)Icons.Default.Pause else Icons.Default.PlayArrow,if(playing)"Pause" else "Play",Modifier.size(40.dp))','else VXPlayPauseIcon(playing,Modifier.size(40.dp))')
edit('player/PlayerScreen.kt','Modifier.graphicsLayer { alpha = opacity }','Modifier.graphicsLayer { alpha = opacity; translationY = (1f-opacity)*8.dp.toPx() }') if 'Modifier.graphicsLayer { alpha = opacity }' in (src/'player/PlayerScreen.kt').read_text() else None
edit('player/PlayerScreen.kt','android.widget.Toast.makeText(context,"Saved to Pictures/VXPlayer",android.widget.Toast.LENGTH_SHORT).show()','feedback("Saved to Pictures/VXPlayer")')
edit('player/PlayerScreen.kt','.padding(24.dp).size((72 + 48 * pulse.value).dp).background(Color.White.copy(alpha = .22f * (1f - pulse.value)), CircleShape)', '.padding(24.dp).size(96.dp).graphicsLayer {scaleX=.75f+pulse.value*.5f;scaleY=scaleX;alpha=1f-pulse.value}.background(Color.White.copy(alpha = .22f), CircleShape)')
# The confirmation remains a small isolated composable; gesture ticks never invalidate video content.
edit('player/PlayerScreen.kt','modifier.background(Color.Black.copy(alpha = .8f), RoundedCornerShape(12.dp)).padding(16.dp)','modifier.background(Color.Black.copy(alpha = .8f), CircleShape).padding(horizontal=20.dp,vertical=12.dp), style=MaterialTheme.typography.labelLarge')
edit('player/PlayerScreen.kt','GestureFeedback({ indicator }, { model.audioEnhancer.percent > 100 }, Modifier.align(Alignment.Center))','GestureFeedback({ indicator }, { model.audioEnhancer.percent > 100 }, Modifier.align(Alignment.TopCenter).safeDrawingPadding().padding(top=72.dp,start=16.dp,end=16.dp))')
(src/'ui/PlaybackIcon.kt').write_text('''package com.vxplayer.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.material3.LocalContentColor
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.semantics.*

/** Two vector paths with matching vertices morph without swapping icon compositions. */
@Composable
fun VXPlayPauseIcon(playing:Boolean,modifier:Modifier=Modifier) {
    val fraction=animateFloatAsState(if(playing)1f else 0f,tween(VXMotion.Standard,easing=VXMotion.Move),label="Play pause morph")
    val color=LocalContentColor.current
    Canvas(modifier.semantics {contentDescription=if(playing)"Pause" else "Play"}) {
        val play=listOf(listOf(Offset(6f,4f),Offset(12f,7.5f),Offset(12f,16.5f),Offset(6f,20f)),listOf(Offset(12f,7.5f),Offset(20f,12f),Offset(20f,12f),Offset(12f,16.5f)))
        val pause=listOf(listOf(Offset(6f,5f),Offset(10f,5f),Offset(10f,19f),Offset(6f,19f)),listOf(Offset(14f,5f),Offset(18f,5f),Offset(18f,19f),Offset(14f,19f)))
        scale(size.width/24f,size.height/24f,pivot=Offset.Zero) {
            repeat(2) { half ->
                val path=Path()
                repeat(4) { index ->
                    val a=play[half][index];val b=pause[half][index];val v=a+(b-a)*fraction.value
                    if(index==0)path.moveTo(v.x,v.y) else path.lineTo(v.x,v.y)
                }
                path.close();drawPath(path,color)
            }
        }
    }
}
''')
# Buffer polling belongs exclusively in the timeline.
edit('player/PlaybackTimeline.kt','import androidx.compose.foundation.layout.*','import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.Canvas\nimport androidx.compose.foundation.background\nimport androidx.compose.foundation.shape.CircleShape\nimport androidx.compose.ui.geometry.Offset\nimport androidx.compose.ui.geometry.Size\nimport androidx.compose.ui.graphics.Brush\nimport androidx.compose.ui.graphics.graphicsLayer\nimport com.vxplayer.ui.*')
edit('player/PlaybackTimeline.kt','    var duration by remember','    var buffered by remember { mutableLongStateOf(0) }\n    var duration by remember')
edit('player/PlaybackTimeline.kt','            if (position != next)','            buffered = current?.bufferedPosition?.coerceAtLeast(0) ?: 0\n            if (position != next)')
edit('player/PlaybackTimeline.kt','        SmoothPositionSlider(position, duration, preview,','        SmoothPositionSlider(position, duration, buffered, preview,')
edit('player/PlaybackTimeline.kt','private fun SmoothPositionSlider(position: Long, duration: Long, preview: Float?','private fun SmoothPositionSlider(position: Long, duration: Long, buffered: Long, preview: Float?')
old='''    Slider(value=(preview ?: animated).coerceIn(0f,end),onValueChange=onValueChange,
        onValueChangeFinished=onValueChangeFinished,valueRange=0f..end,enabled=enabled,
        colors=SliderDefaults.colors(thumbColor=Color.White,activeTrackColor=Color.White),modifier=modifier)'''
new='''    val growth=animateFloatAsState(if(preview==null)1f else 2f,tween(VXMotion.Quick),label="Seek track emphasis")
    Box(modifier.heightIn(min=48.dp),contentAlignment=Alignment.Center) {
        Canvas(Modifier.fillMaxWidth().height(2.dp).graphicsLayer {scaleY=growth.value}) {
            drawRect(Color.White.copy(alpha=.16f))
            drawRect(Color.White.copy(alpha=.35f),size=Size(size.width*(buffered/end).coerceIn(0f,1f),size.height))
            drawRect(VXBrand.gradient,size=Size(size.width*((preview ?: animated)/end).coerceIn(0f,1f),size.height))
        }
        Slider(value=(preview ?: animated).coerceIn(0f,end),onValueChange=onValueChange,
            onValueChangeFinished=onValueChangeFinished,valueRange=0f..end,enabled=enabled,
            colors=SliderDefaults.colors(thumbColor=Color.White,activeTrackColor=Color.Transparent,inactiveTrackColor=Color.Transparent),modifier=Modifier.fillMaxWidth())
        preview?.let { target ->
            Text(formatDuration(target.toLong()),color=Color.White,style=MaterialTheme.typography.labelMedium,
                modifier=Modifier.align(Alignment.TopCenter).graphicsLayer {translationY=-28.dp.toPx()}.background(Color.Black.copy(alpha=.85f),CircleShape).padding(horizontal=12.dp,vertical=8.dp))
        }
    }'''
edit('player/PlaybackTimeline.kt',old,new)
print('Player presentation applied')
