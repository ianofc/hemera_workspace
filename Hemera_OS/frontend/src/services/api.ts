import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const authService = {
  login: async (credentials: any) => {
    try {
      const response = await axios.post(`${API_URL}/api/status/login/`, {
        email: credentials.username,
        password: credentials.password
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 401) {
        throw new Error('Credenciais inválidas. Verifique seu email e senha.');
      }
      throw new Error('Erro ao conectar com o servidor.');
    }
  },

  register: async (userData: any) => {
    // Para simplificar, mantemos mock ou você pode apontar para API de registro real no futuro
    await new Promise(resolve => setTimeout(resolve, 800));
    return {
      token: 'mock-jwt-token-beta-new-user',
      user: { id: Math.floor(Math.random() * 1000), name: userData.name || userData.username, role: 'user' }
    };
  }
};
