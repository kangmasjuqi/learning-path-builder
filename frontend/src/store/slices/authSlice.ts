// frontend/src/store/slices/authSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  id: number;
  username: string;
  email: string;
  is_educator: boolean;
  is_active: boolean;
}

interface AuthState {
  isAuthenticated: boolean;
  user: UserState | null;
  accessToken: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  accessToken: null,
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart(state) {
      state.loading = true;
      state.error = null;
    },
    loginSuccess(state, action: PayloadAction<{ user: UserState; accessToken: string }>) {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.accessToken = action.payload.accessToken;
      state.error = null;
      if (typeof window !== 'undefined') {
        localStorage.setItem('accessToken', action.payload.accessToken);
      }
    },
    loginFailure(state, action: PayloadAction<string>) {
      state.loading = false;
      state.isAuthenticated = false;
      state.user = null;
      state.accessToken = null;
      state.error = action.payload;
      if (typeof window !== 'undefined') {
        localStorage.removeItem('accessToken');
      }
    },
    logout(state) {
      state.isAuthenticated = false;
      state.user = null;
      state.accessToken = null;
      state.loading = false;
      state.error = null;
      if (typeof window !== 'undefined') {
        localStorage.removeItem('accessToken');
      }
    },
    setAuthFromStorage(state, action: PayloadAction<{ user: UserState; accessToken: string } | null>) {
      if (action.payload) {
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.accessToken = action.payload.accessToken;
      } else {
        state.isAuthenticated = false;
        state.user = null;
        state.accessToken = null;
      }
    },
  },
});

export const { loginStart, loginSuccess, loginFailure, logout, setAuthFromStorage } = authSlice.actions;
export default authSlice.reducer;