
'use client'

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

const UPLOAD_FOLDER = 'http://127.0.0.1:5000/static/pictures/'

export default function PhotoIndex() {
  const params = useParams<{ tag: string; id: string }>()
  const [photo, setPhotos] = useState<Photo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
      fetch(`http://127.0.0.1:5000/${params.id}`) // Endpoint Flask
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
          <h1>📸 Page de la photo</h1>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                  <div key={photo.id} style={{ textAlign: 'center' }}>
                      <img
                          src={UPLOAD_FOLDER + photo.path}
                          alt={photo.title}
                          style={{ width: '100%', height: '150px', objectFit: 'cover', borderRadius: '8px' }}
                      />
                      <h3>{photo.title}</h3>
                  </div>

          </div>
      </div>
  );
}
