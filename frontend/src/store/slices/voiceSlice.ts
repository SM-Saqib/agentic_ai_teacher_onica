import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { VoiceConfig } from '../../types'

interface VoiceState {
  config: VoiceConfig
  isRecording: boolean
  transcript: string
}

const initialState: VoiceState = {
  config: {
    enabled: false,
    language: 'en-US',
    voice_quality: 'high',
  },
  isRecording: false,
  transcript: '',
}

const voiceSlice = createSlice({
  name: 'voice',
  initialState,
  reducers: {
    setVoiceConfig: (state, action: PayloadAction<Partial<VoiceConfig>>) => {
      state.config = { ...state.config, ...action.payload }
    },
    setRecording: (state, action: PayloadAction<boolean>) => {
      state.isRecording = action.payload
    },
    setTranscript: (state, action: PayloadAction<string>) => {
      state.transcript = action.payload
    },
  },
})

export const { setVoiceConfig, setRecording, setTranscript } = voiceSlice.actions
export default voiceSlice.reducer
