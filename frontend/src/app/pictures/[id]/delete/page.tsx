'use client'

import { useEffect } from 'react';
import { redirect } from 'next/navigation'
import { useParams } from 'next/navigation'

export default function App() {

  const params = useParams<{ id: string }>()
  // const userId = useAppSelector((state) => state.auth.id); will be use letter to verifying if the user is the author of the picture !
  useEffect(() => {
    try {
      const response = fetch(`http://backend:8000/blog/${params.id}/delete`, {
        method: 'POST',
        body: params.id,
        credentials: 'include'
      });
      console.log(response);
    } catch (error) {
      console.error('Erreur :', error);
    }
    redirect(`/pictures/`)

  })
};
  // firstName and lastName will have correct type
