import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiFetch } from '../utils/api';

interface ShareState {
  shareUrl: string|null;
  loading: boolean;
  error: string|null;
}

const initialState: ShareState = {
  shareUrl: null,
  loading: false,
  error: null
};

export const shareFile = createAsyncThunk(
  'share/shareFile',
  async ({file_id,permission,validity}:{file_id:number,permission:string,validity:number}, {rejectWithValue}) => {
    try {
      const res = await apiFetch('/share/', {
        method:'POST',
        body: JSON.stringify({file_id, permission, validity})
      });
      return res;
    } catch(e:any) {
      return rejectWithValue(e.message);
    }
  }
);

const shareSlice = createSlice({
  name: 'share',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder.addCase(shareFile.fulfilled, (state,action) => {
      state.shareUrl = action.payload.share_url;
      state.loading = false;
      state.error = null;
    });
    builder.addCase(shareFile.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(shareFile.rejected, (state,action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
  }
});

export default shareSlice.reducer;
