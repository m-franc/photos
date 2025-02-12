
'use client'


import Link from 'next/link';
import Image from 'next/image'
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation'

// async function getImageData() {
//   const res = await fetch('http://127.0.0.1:5000/', {
//       cache: 'no-store', // Désactive le cache si nécessaire
//   });

//   if (!res.ok) {
//       throw new Error('Erreur lors de la récupération des données Flask');
//   }

//   return res.json();
// }

interface Photo {
  author_id: number,
  created: string,
  description: string,
  id: number,
  path: string,
  title: string,
  username: string
}

const UPLOAD_FOLDER = 'http://localhost:5000/static/pictures/'

export default function PhotoIndex() {
  const params = useParams<{ id: string }>()
  const [photo, setPhoto] = useState<Photo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
      fetch(`http://localhost:5000/blog/${params.id}`, {
        credentials: 'include',
      }) // Endpoint Flask
          .then((response) => {
              if (!response.ok) {
                  throw new Error('Erreur réseau');
              }
              return response.json();
          })
          .then((data) => {
              console.log('Photos reçues:', data);
              setPhoto(data);
          })
          .catch((error) => {
              console.error('Erreur API:', error);
              setError(error.message);
          })
          .finally(() => setLoading(false));
  }, [params]);

  if (loading) return <p>⏳ Chargement des photos...</p>;
  if (error) return <p>❌ Erreur : {error}</p>;
  return (
      <div>
          <h1>📸 Page de la photo</h1>
          <Link href={`/pictures/new`}><h1>Ajouter une photo</h1></Link>
          <Link href={`/pictures/`}><h1>Retour à la galerie</h1></Link>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
            <div key={photo?.id} style={{ textAlign: 'center' }}>
              <Image
                unoptimized
                src={UPLOAD_FOLDER + photo?.path}
                alt={photo?.title || 'Photo'}
                style={{ objectFit: 'cover', borderRadius: '8px' }}
                width={500}
                height={150} />
              <h3>{photo?.title}</h3>
              <p>{photo?.description}</p>
              <p>By {photo?.username}</p>
              <Link href={`/pictures/${params.id}/edit`}><h1>edit les infos de la photo</h1></Link>
              <Link href={`/pictures/${params.id}/delete`}><h1>supprimer la photo</h1></Link>
            </div>
          </div>
      </div>
  );
}
