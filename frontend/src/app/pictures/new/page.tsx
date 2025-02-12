'use client'

import * as React from "react"
import { useController, useForm, Control, SubmitHandler } from "react-hook-form"
import { useRouter } from 'next/navigation'
import Link from 'next/link';
import { useAppSelector } from "@/app/redux/hook";

type FormData = {
  title: string;
  description: string;
  path: File;
  author_id: string | null;
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

  const router = useRouter()
  const {
    register,
    control,
    handleSubmit,
  } = useForm<FormData>()

  const userId: string | null = useAppSelector((state) => state.auth.id);
  if (!userId)
    throw new Error("User ID is required");

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    try {
      const formData = new FormData();
      formData.append('title', data.title)
      formData.append('description', data.description)
      formData.append('path', data.path)
      formData.append('author_id', userId)
      const response = await fetch('http://localhost:5000/blog/create', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });
      console.log(response);
    } catch (error) {
      console.error('Erreur :', error);
    }
    router.push("/pictures")
  };
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
