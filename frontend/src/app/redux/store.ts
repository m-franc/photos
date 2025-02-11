import { configureStore } from '@reduxjs/toolkit'
import authReducer from './authSlice'
import storage from 'redux-persist/lib/storage';
import { persistReducer, persistStore } from 'redux-persist';
import { WebStorage } from 'redux-persist/lib/types';
// import { serialize } from 'v8';

interface CustomPersistConfig {
  key: string;
  storage: WebStorage;
  whitelist: string[];
}

const persistConfig: CustomPersistConfig = {
  key: 'auth',
  storage,
  whitelist: ['auth'],

};

const persistedReducer = persistReducer(persistConfig, authReducer);

export const store = configureStore({
  reducer: {
    auth: persistedReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE', 'persist/REGISTER'],
        // Ignorer les vérifications de sérialisation pour certains chemins si nécessaire
        ignoredPaths: ['auth.register']
      },
    }),
});

// Infer the type of makeStore
export type AppStore = typeof store;
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']
export const persistor = persistStore(store);
