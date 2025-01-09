import * as React from "react"
import Link from 'next/link';


export default function App() {


  return (
    <div>
      <Link href={`/auth/login/`}><h1>Se connecter</h1></Link>
      <Link href={`/auth/signin/`}><h1>Se créer un compte</h1></Link>
    </div>

  )
}
