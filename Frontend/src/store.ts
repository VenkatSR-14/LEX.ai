import { configureStore } from '@reduxjs/toolkit';
import loginReducer from './Slices/loginSlice';

export const store = configureStore({
  reducer: { counter: loginReducer }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;