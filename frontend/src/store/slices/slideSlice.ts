import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { Slide } from '../../types'

interface SlideState {
  slides: Slide[]
  currentSlide: Slide | null
  isLoading: boolean
  error: string | null
}

const initialState: SlideState = {
  slides: [],
  currentSlide: null,
  isLoading: false,
  error: null,
}

const slideSlice = createSlice({
  name: 'slide',
  initialState,
  reducers: {
    setSlides: (state, action: PayloadAction<Slide[]>) => {
      state.slides = action.payload
    },
    setCurrentSlide: (state, action: PayloadAction<Slide | null>) => {
      state.currentSlide = action.payload
    },
    addSlide: (state, action: PayloadAction<Slide>) => {
      state.slides.push(action.payload)
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
  },
})

export const { setSlides, setCurrentSlide, addSlide, setLoading, setError } = slideSlice.actions
export default slideSlice.reducer
