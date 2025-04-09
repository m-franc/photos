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
  debug: boolean;
}

const persistConfig: CustomPersistConfig | null = {
  key: 'root',
  storage,
  whitelist: ['auth'],
  debug: true,
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

console.log('Initial state:', store.getState());


// Infer the type of makeStore
export type AppStore = typeof store;
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export const isClient = typeof window !== 'undefined';
export const shouldPersist = isClient && process.env.NEXT_PUBLIC_REDUX_PERSIST === 'true';
export const persistor = shouldPersist ? persistStore(store) : null;
