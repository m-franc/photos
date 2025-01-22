'use client'

import * as React from "react"
import { useForm } from "react-hook-form"
import { redirect } from 'next/navigation'
import { useAppDispatch } from '../../redux/hook';
import { login } from '../../redux/authSlice';

type FormData = {
  username: string,
  password: string,
}


export default function App() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>()
  const dispatch = useAppDispatch();
  const onSubmit = handleSubmit( async (data) => {
    try {
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        credentials: 'include',
      });
      console.log('Réponse :', await response.json());
      console.log('Réponse !! :', await response.json());
      dispatch(login({ username: 'JohnDoe' }));
    } catch (error) {
      console.error('Erreur :', error);
    }
    console.log(data)
    redirect('/pictures')
  })
  // firstName and lastName will have correct type

  return (
    <form onSubmit={onSubmit} className="form">
      <label>username</label>
      <input {...register("username")} />
      <label>password</label>
      <input type="password" {...register("password")} />
      <button
        type="submit">
        SE CONNECTER
      </button>
    </form>
  )
}
