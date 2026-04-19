import React from "react";
import { User, Settings, Shield, Bell, Key, LogOut } from "lucide-react";

const Profile: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4">
      <div className="w-full max-w-4xl bg-white shadow-xl rounded-2xl overflow-hidden animate-fade-in">
        {/* Header Section */}
        <div className="bg-gradient-to-r from-[#211E55] to-[#2A2665] h-32 relative">
          <div className="absolute -bottom-12 left-8 border-4 border-white rounded-full bg-white shadow-md">
            <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center text-[#211E55]">
              <User size={48} />
            </div>
          </div>
        </div>

        {/* Profile Info */}
        <div className="mt-14 px-8 pb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Meu Perfil</h1>
              <p className="text-gray-500 mt-1">Gerencie suas informações e preferências</p>
            </div>
            <button className="px-4 py-2 bg-[#211E55] text-white rounded-lg hover:bg-opacity-90 transition shadow-sm font-medium">
              Editar Perfil
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            {/* Nav Menu */}
            <div className="col-span-1 border-r border-gray-100 pr-6">
              <nav className="space-y-2">
                <a href="#dados" className="flex items-center gap-3 px-4 py-3 bg-[#EEF2FF] text-[#211E55] rounded-xl font-medium transition">
                  <User size={20} />
                  Dados Pessoais
                </a>
                <a href="#seguranca" className="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-gray-50 rounded-xl font-medium transition">
                  <Shield size={20} />
                  Segurança
                </a>
                <a href="#notificacoes" className="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-gray-50 rounded-xl font-medium transition">
                  <Bell size={20} />
                  Notificações
                </a>
                <div className="pt-4 mt-4 border-t border-gray-100">
                  <button className="w-full flex items-center gap-3 px-4 py-3 text-red-500 hover:bg-red-50 rounded-xl font-medium transition">
                    <LogOut size={20} />
                    Sair da conta
                  </button>
                </div>
              </nav>
            </div>

            {/* Content Area */}
            <div className="col-span-2">
              <h2 className="text-xl font-semibold text-gray-800 mb-6">Informações Pessoais</h2>
              
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-500 mb-1">Nome Completo</label>
                    <div className="w-full bg-gray-50 border border-gray-200 px-4 py-2 rounded-lg text-gray-800">
                      Usuário Hemera
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500 mb-1">E-mail</label>
                    <div className="w-full bg-gray-50 border border-gray-200 px-4 py-2 rounded-lg text-gray-800">
                      usuario@hemera.os
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500 mb-1">Telefone</label>
                    <div className="w-full bg-gray-50 border border-gray-200 px-4 py-2 rounded-lg text-gray-800">
                      (XX) XXXXX-XXXX
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-500 mb-1">Cargo / Função</label>
                    <div className="w-full bg-gray-50 border border-gray-200 px-4 py-2 rounded-lg text-gray-800">
                      Administrador
                    </div>
                  </div>
                </div>

                <div className="pt-6 border-t border-gray-100">
                  <h3 className="text-lg font-medium text-gray-800 mb-4 flex items-center gap-2">
                    <Key size={18} className="text-[#211E55]" />
                    Alterar Senha
                  </h3>
                  <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition shadow-sm font-medium">
                    Atualizar credenciais
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
