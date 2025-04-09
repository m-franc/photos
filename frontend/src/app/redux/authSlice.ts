import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  id: string | null;
  username: string | null;
  role: string | null;
}

const initialState: AuthState = {
  id: null,
  username: null,
  role: null
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action: PayloadAction<{  id: string; username: string; role: string }>) => {
      state.id = action.payload.id;
      state.username = action.payload.username;
      state.role = action.payload.role;
    },
    logout: (state) => {
      state.id = null;
      state.username = null;
      state.role = null;
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
