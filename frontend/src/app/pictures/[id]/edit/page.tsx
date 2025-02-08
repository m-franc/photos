'use client'

import * as React from "react"
import { useForm } from "react-hook-form"
import { redirect } from 'next/navigation'
import Link from 'next/link';
import { useAppSelector } from "@/app/redux/hook";
import { useParams } from 'next/navigation'

type FormData = {
  title: string,
  description: string,
  author_id: string
}

export default function App() {

  const params = useParams<{ id: string }>()
  const {
    register,
    handleSubmit,
  } = useForm<FormData>()

  const userId = useAppSelector((state) => state.auth.id);

  const handleSubmit = async (data) => {

    try {
      const formData = new FormData();
      formData.append('title', data.title)
      formData.append('description', data.description)
      formData.append('author_id', userId)
      const response = await fetch(`http://localhost:5000/${params.id}/update`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });
      console.log(response);
    } catch (error) {
      console.error('Erreur :', error);
    }
    redirect(`/pictures/${params.id}`)
  });
  // firstName and lastName will have correct type

  return (
    <div>
      <Link href={`/pictures/`}><h1>Retour à la galerie</h1></Link>
      <form onSubmit={handleSubmit} className="form" method="post">
        <label>Titre</label>
        <input {...register("title")} />
        <label>Description</label>
        <input {...register("description")} />
        <button
          type="submit"
          // onClick={() => {
          //   setValue("title", "value") // ✅
          //   setValue("description", "value")
          //   setValue("path", "value") // ❌: true is not string
          //   errors.bill // ❌: property bill does not exist
          // }}
        >
          SetValue
        </button>
      </form>
    </div>
  )
}
