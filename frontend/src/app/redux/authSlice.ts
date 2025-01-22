import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  id: string | null;
  username: string | null;
}

const initialState: AuthState = {
  id: null,
  username: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action: PayloadAction<{  id: string; username: string }>) => {
      state.id = action.payload.id;
      state.username = action.payload.username;
    },
    logout: (state) => {
      state = null;
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
