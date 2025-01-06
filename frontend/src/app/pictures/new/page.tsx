'use client'

import * as React from "react"
import { useForm } from "react-hook-form"

type FormData = {
  title: string,
  description: string,
  path: string
}

export default function App() {
  const {
    register,
    setValue,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>()
  const onSubmit = handleSubmit( async (data) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      console.log('Réponse :', await response.json());
    } catch (error) {
      console.error('Erreur :', error);
    }
    console.log(data)
  });
  // firstName and lastName will have correct type

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="form" method="post">
      <label>Titre</label>
      <input {...register("title")} />
      <label>Description</label>
      <input {...register("description")} />
      <label>Photo</label>
      <input type="file" {...register("path")} />
      <button
        type="submit"
        onClick={() => {
          setValue("title", "value") // ✅
          setValue("description", "value")
          setValue("path", "value") // ❌: true is not string
          errors.bill // ❌: property bill does not exist
        }}
      >
        SetValue
      </button>
    </form>
  )
}
