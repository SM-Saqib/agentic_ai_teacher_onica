import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { AvatarConfig } from '../../types'

interface AvatarState {
  config: AvatarConfig | null
  isVisible: boolean
  isAnimating: boolean
}

const initialState: AvatarState = {
  config: null,
  isVisible: false,
  isAnimating: false,
}

const avatarSlice = createSlice({
  name: 'avatar',
  initialState,
  reducers: {
    setAvatarConfig: (state, action: PayloadAction<AvatarConfig>) => {
      state.config = action.payload
    },
    setAvatarVisible: (state, action: PayloadAction<boolean>) => {
      state.isVisible = action.payload
    },
    setAnimating: (state, action: PayloadAction<boolean>) => {
      state.isAnimating = action.payload
    },
  },
})

export const { setAvatarConfig, setAvatarVisible, setAnimating } = avatarSlice.actions
export default avatarSlice.reducer
