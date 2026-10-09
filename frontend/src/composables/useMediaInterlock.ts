import { watch, type Ref } from 'vue'
import { useAudioPlayerStore } from '@/stores/audioPlayer'

export function useMediaInterlock(isTVPlaying: Ref<boolean>) {
  const audioStore = useAudioPlayerStore()
  
  const onTVPlay = () => {
    if (audioStore.isPlaying && !audioStore.isMuted) {
      audioStore.muteForTV()
    }
  }

  const onTVPause = () => {
    audioStore.unmuteFromTV()
  }

  watch(isTVPlaying, (playing) => {
    if (playing) {
      onTVPlay()
    } else {
      onTVPause()
    }
  })

  return {
    onTVPlay,
    onTVPause
  }
}
