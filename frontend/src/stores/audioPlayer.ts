import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAudioPlayerStore = defineStore('audioPlayer', () => {
  const streamUrl = ref('/radio-stream/live')
  const isPlaying = ref(false)
  const isBuffering = ref(false)
  const volume = ref(0.8)
  const isMuted = ref(false)
  const previousMuteState = ref(false)
  
  const currentTrack = ref('Radio UPEC')
  const stationName = ref('Mindalae UPEC 102.3 FM')
  const listenersCount = ref(0)
  const hasError = ref(false)

  function setPlaying(status: boolean) {
    isPlaying.value = status
  }

  function setBuffering(status: boolean) {
    isBuffering.value = status
  }

  function setVolume(val: number) {
    volume.value = Math.max(0, Math.min(1, val))
    if (volume.value > 0 && isMuted.value) {
      isMuted.value = false
    }
  }

  function toggleMute() {
    isMuted.value = !isMuted.value
  }

  function muteForTV() {
    previousMuteState.value = isMuted.value
    isMuted.value = true
  }

  function unmuteFromTV() {
    isMuted.value = previousMuteState.value
  }

  async function updateMetadata() {
    if (!isPlaying.value) return
    try {
      const { data } = await axios.get('/api/radio/status')
      currentTrack.value = `${data.artist ? data.artist + ' - ' : ''}${data.title || 'Radio UPEC'}`
      listenersCount.value = data.listeners || 0
      syncMediaSession()
    } catch (e) {
      // Failed to get metadata, ignore quietly
    }
  }

  function syncMediaSession() {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: currentTrack.value,
        artist: stationName.value,
        album: 'Radio UPEC',
        artwork: [
          { src: '/favicon.ico', sizes: '512x512', type: 'image/png' }
        ]
      })
    }
  }

  return {
    streamUrl,
    isPlaying,
    isBuffering,
    volume,
    isMuted,
    currentTrack,
    stationName,
    listenersCount,
    hasError,
    setPlaying,
    setBuffering,
    setVolume,
    toggleMute,
    muteForTV,
    unmuteFromTV,
    updateMetadata,
    syncMediaSession
  }
})
