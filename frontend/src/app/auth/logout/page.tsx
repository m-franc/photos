"use client"

import { useAppDispatch } from '../../redux/hook';
import { logout } from '../../redux/authSlice';
import { useRouter } from 'next/navigation'


const Logout = () => {

  const router = useRouter()
  const dispatch = useAppDispatch();

  const handleLogout = async () => {
    const response = await fetch('http://localhost:8000/auth/logout', {
      credentials: 'include', // Inclure les cookies
      method: 'POST'
    });
    console.log("LA REPONSE : ", response)
    if (response.ok) {
      console.log('Déconnecté avec succès');
      dispatch(logout()); // Réinitialise l'état Redux
      router.push("../login"); // Redirige vers la page de connexion
    } else {
      console.error('Erreur lors de la déconnexion');
    }
  };

  // Appelle directement la déconnexion
  handleLogout();

  return null; // Cette page n’affiche rien
};

export default Logout;
