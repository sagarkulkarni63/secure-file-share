import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import fileReducer from './fileSlice';
import shareReducer from './shareSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    files: fileReducer,
    share: shareReducer
  }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
