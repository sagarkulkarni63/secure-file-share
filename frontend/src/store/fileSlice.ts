import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiFetch } from '../utils/api';

interface FileItem {
  id:number;
  filename:string;
  owner:number;
  created_at:string;
}

interface FileState {
  list: FileItem[];
  loading: boolean;
  error: string|null;
}

const initialState: FileState = {
  list: [],
  loading: false,
  error: null
};

export const fetchFiles = createAsyncThunk('files/fetch', async (_, {rejectWithValue}) => {
  try {
    const res = await apiFetch('/files/');
    return res;
  } catch(e:any) {
    return rejectWithValue(e.message);
  }
});

export const fileSlice = createSlice({
  name: 'files',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder.addCase(fetchFiles.fulfilled, (state,action) => {
      state.list = action.payload;
      state.loading = false;
      state.error = null;
    });
    builder.addCase(fetchFiles.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(fetchFiles.rejected, (state,action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
  }
});

export default fileSlice.reducer;
