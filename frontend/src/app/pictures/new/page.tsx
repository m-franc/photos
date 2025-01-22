'use client'

import * as React from "react"
import { useController, useForm, Control } from "react-hook-form"
import { redirect } from 'next/navigation'
import Link from 'next/link';
import { useAppSelector } from "@/app/redux/hook";

type FormData = {
  title: string,
  description: string,
  path: File
  author_id: string
}

type FileInputProps = {
  name: keyof FormData;
  control: Control<FormData>;
}

const FileInput: React.FC<FileInputProps> = ({ name, control }) => {
  const { field } = useController({ name, control });
  // const value = useForm<FormData>()
  return (
    <input
      type="file"
      onChange={(e) => {
        if (e.target.files?.[0]) {
          field.onChange(e.target.files[0]);
        }
      }}
    />
  );
};


export default function App() {

  const {
    register,
    control,
    handleSubmit,
  } = useForm<FormData>()

  const userId = useAppSelector((state) => state.auth.id);
  console.log(userId);

  const onSubmit = handleSubmit( async (data) => {

    try {
      const formData = new FormData();
      formData.append('title', data.title)
      formData.append('description', data.description)
      formData.append('path', data.path)
      formData.append('author_id', userId)
      const response = await fetch('http://127.0.0.1:5000/create', {
        method: 'POST',
        body: formData,
      });
    } catch (error) {
      console.error('Erreur :', error);
    }
    redirect('/pictures')
  });
  // firstName and lastName will have correct type

  return (
    <div>
      <Link href={`/pictures/`}><h1>Retour à la galerie</h1></Link>
      <form onSubmit={handleSubmit(onSubmit)} className="form" method="post">
        <label>Titre</label>
        <input {...register("title")} />
        <label>Description</label>
        <input {...register("description")} />
        <label>Photo</label>
        <FileInput name="path" control={control} />
        {/* /* <input
          type="file"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              setValue('path', e.target.files[0]);
            }
          }}
        /> */}
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
