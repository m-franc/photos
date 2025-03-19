
'use client'

import Link from 'next/link';
import { useEffect, useState } from 'react';
import Image from 'next/image'

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

const UPLOAD_FOLDER = 'http://backend-server-1:8000/static/pictures/'

export default function PhotoIndex() {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
      fetch('http://backend-server-1:8000/blog/', {
        credentials: 'include'
      }) // Endpoint Flask
          .then((response) => {
              if (!response.ok) {
                  throw new Error('Erreur réseau');
              }
              return response.json();
          })
          .then((data) => {
              console.log('Photos reçues:', data);
              setPhotos(data);
          })
          .catch((error) => {
              console.error('Erreur API:', error);
              setError(error.message);
          })
          .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>⏳ Chargement des photos...</p>;
  if (error) return <p>❌ Erreur : {error}</p>;
  return (
      <div>
          <span>
            <h1>📸 Galerie de Photos</h1>
          </span>
          <span>
            <Link href={`/pictures/new`}><h1>Ajouter une photo</h1></Link>
          </span>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
              {photos.map((photo) => (
                  <div key={photo.id} style={{ textAlign: 'center' }}>
                      <Image
                         unoptimized
                         src={UPLOAD_FOLDER + photo?.path}
                         alt={photo?.title}
                         style={{ objectFit: 'cover', borderRadius: '8px' }}
                         width={500}
                         height={150} />
                      <Link href={`/pictures/${photo.id}`}><h3>{photo.title}</h3>
                      </Link>
                  </div>
              ))}
          </div>
      </div>
  );
}
