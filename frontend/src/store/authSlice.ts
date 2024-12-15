import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiFetch } from '../utils/api';

interface AuthState {
  isLoggedIn: boolean;
  mfaRequired: boolean;
  username: string;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  isLoggedIn: false,
  mfaRequired: false,
  username: '',
  loading: false,
  error: null
};

export const login = createAsyncThunk(
  'auth/login',
  async ({username,password}:{username:string,password:string}, {rejectWithValue}) => {
    try {
      const res = await apiFetch('/login/', {
        method: 'POST',
        body: JSON.stringify({username, password})
      });
      return res;
    } catch(e:any) {
      return rejectWithValue(e.message);
    }
  }
);

export const mfaConfirm = createAsyncThunk(
  'auth/mfaConfirm',
  async (token:string, {rejectWithValue}) => {
    try {
      const res = await apiFetch('/mfa-confirm/', {
        method: 'POST',
        body: JSON.stringify({token})
      });
      return res;
    } catch(e:any) {
      return rejectWithValue(e.message);
    }
  }
);

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      state.isLoggedIn = false;
      state.mfaRequired = false;
      state.username = '';
    }
  },
  extraReducers: (builder) => {
    builder.addCase(login.fulfilled, (state,action) => {
      if (action.payload.mfa_required) {
        state.mfaRequired = true;
      } else {
        state.isLoggedIn = true;
      }
      state.loading = false;
      state.error = null;
    });
    builder.addCase(login.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(login.rejected, (state,action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
    builder.addCase(mfaConfirm.fulfilled, (state) => {
      state.mfaRequired = false;
      state.isLoggedIn = true;
      state.loading = false;
      state.error = null;
    });
    builder.addCase(mfaConfirm.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(mfaConfirm.rejected, (state,action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
  }
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
