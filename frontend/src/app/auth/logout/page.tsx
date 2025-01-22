"use client"

import { useAppDispatch } from '../../redux/hook';
import { logout } from '../../redux/authSlice';
import { redirect } from 'next/navigation'

const Logout = () => {
  const dispatch = useAppDispatch();

  const handleLogout = async () => {
    const response = await fetch('http://localhost:5000/auth/logout', {
      method: 'POST',
      credentials: 'include', // Inclure les cookies
    });

    if (response.ok) {
      console.log('Déconnecté avec succès');
      dispatch(logout()); // Réinitialise l'état Redux
      redirect('auth/login'); // Redirige vers la page de connexion
    } else {
      console.error('Erreur lors de la déconnexion');
    }
  };

  // Appelle directement la déconnexion
  handleLogout();

  return null; // Cette page n’affiche rien
};

export default Logout;
