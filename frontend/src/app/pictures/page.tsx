async function getImageData() {
  const res = await fetch('http://127.0.0.1:5000/', {
      cache: 'no-store', // Désactive le cache si nécessaire
  });

  if (!res.ok) {
      throw new Error('Erreur lors de la récupération des données Flask');
  }

  return res.json();
}

export default async function Home() {
  const data = await getImageData();
  console.log(data);
  return (
      <div>
          <h1>Intégration Flask x Next.js (SSR)</h1>
          <p><strong>ID :</strong> {data.id}</p>
          <img src={data.url} alt="Image depuis Flask" />
          <h2>EXIF Data</h2>
          <ul>
              {Object.entries(data).map(([key, value]) => (
                  <li key={key}><strong>{key}:</strong> {value}</li>
              ))}
          </ul>
      </div>
  );
}
