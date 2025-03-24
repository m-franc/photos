'use client'

import * as React from "react"
import { useForm } from "react-hook-form"
import { useRouter } from 'next/navigation'

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
  const onSubmit = handleSubmit( async (data) => {
    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        credentials: 'include',
      });
      console.log('Réponse :', await response.json());
      console.log('DATA :', await data);
    } catch (error) {
      console.error('Erreur :', error);
    }
    router.push("../login")
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
        CREER SON COMPTE
      </button>
    </form>
  )
}
