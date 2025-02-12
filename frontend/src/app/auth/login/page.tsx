'use client'

import * as React from "react"
import { useForm } from "react-hook-form"
import { useRouter } from 'next/navigation'
import { useAppDispatch } from '../../redux/hook';
import { login } from '../../redux/authSlice';

type FormData = {
  username: string,
  password: string,
}

export default function App() {

  const router = useRouter()
  const {
    register,
    handleSubmit,
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
      const dataUser = await response.json();
      dispatch(login({id: dataUser.user.id,
                      username: dataUser.user.username}));
    } catch (error) {
      console.error('Erreur :', error);
    }
    console.log(data)
    router.push("/pictures")
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
