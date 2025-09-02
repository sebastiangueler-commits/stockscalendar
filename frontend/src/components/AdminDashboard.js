import React, { useState, useEffect } from 'react';
import { Users, UserPlus, Trash2, Edit, Shield, Settings, CreditCard, Eye, EyeOff } from 'lucide-react';

const AdminDashboard = ({ onBack }) => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    role: 'user',
    plan: 'basic'
  });
  const [paypalConfig, setPaypalConfig] = useState({
    paypal_email: '',
    paypal_merchant_id: '',
    paypal_client_id: '',
    paypal_secret: ''
  });
  const [showPaypalSecret, setShowPaypalSecret] = useState(false);
  const [activeTab, setActiveTab] = useState('users');

  useEffect(() => {
    loadUsers();
    loadPaypalConfig();
  }, []);

  const loadUsers = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/admin/users');
      const data = await response.json();
      setUsers(data.users || []);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const loadPaypalConfig = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/admin/paypal-config');
      const data = await response.json();
      if (data.success) {
        setPaypalConfig(data.config);
      }
    } catch (error) {
      console.error('Error loading PayPal config:', error);
    }
  };

  const createUser = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8001/api/admin/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      });
      
      if (response.ok) {
        setNewUser({ username: '', email: '', password: '', role: 'user', plan: 'basic' });
        loadUsers();
        alert('Usuario creado exitosamente');
      } else {
        const error = await response.json();
        alert('Error: ' + error.detail);
      }
    } catch (error) {
      alert('Error creando usuario: ' + error.message);
    }
  };

  const deleteUser = async (username) => {
    if (window.confirm(`¿Estás seguro de eliminar al usuario ${username}?`)) {
      try {
        const response = await fetch(`http://localhost:8001/api/admin/users/${username}`, {
          method: 'DELETE',
        });
        
        if (response.ok) {
          loadUsers();
          alert('Usuario eliminado exitosamente');
        } else {
          alert('Error eliminando usuario');
        }
      } catch (error) {
        alert('Error eliminando usuario: ' + error.message);
      }
    }
  };

  const updateUserPlan = async (username, newPlan) => {
    try {
      const response = await fetch(`http://localhost:8001/api/admin/users/${username}/plan`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ plan: newPlan })
      });
      
      if (response.ok) {
        loadUsers();
        alert(`Plan actualizado a ${newPlan} para ${username}`);
      } else {
        alert('Error al actualizar plan');
      }
    } catch (error) {
      console.error('Error updating user plan:', error);
      alert('Error al actualizar plan');
    }
  };

  const savePaypalConfig = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8001/api/admin/paypal-config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(paypalConfig),
      });
      
      if (response.ok) {
        alert('Configuración de PayPal guardada exitosamente');
      } else {
        alert('Error guardando configuración');
      }
    } catch (error) {
      alert('Error guardando configuración: ' + error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-3">
            <Shield className="w-8 h-8 text-yellow-400" />
            <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          </div>
          <button
            onClick={onBack}
            className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg transition-colors"
          >
            Volver al Dashboard
          </button>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 mb-8 bg-gray-800 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('users')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
              activeTab === 'users' ? 'bg-yellow-400 text-black' : 'text-gray-400 hover:text-white'
            }`}
          >
            <Users className="w-4 h-4" />
            <span>Gestión de Usuarios</span>
          </button>
          <button
            onClick={() => setActiveTab('paypal')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
              activeTab === 'paypal' ? 'bg-yellow-400 text-black' : 'text-gray-400 hover:text-white'
            }`}
          >
            <CreditCard className="w-4 h-4" />
            <span>Configuración PayPal</span>
          </button>
        </div>

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="space-y-6">
            {/* Create User Form */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <UserPlus className="w-5 h-5 mr-2" />
                Crear Nuevo Usuario
              </h2>
              <form onSubmit={createUser} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Username</label>
                  <input
                    type="text"
                    value={newUser.username}
                    onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input
                    type="email"
                    value={newUser.email}
                    onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Password</label>
                  <input
                    type="password"
                    value={newUser.password}
                    onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Rol</label>
                  <select
                    value={newUser.role}
                    onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                  >
                    <option value="user">Usuario</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Plan</label>
                  <select
                    value={newUser.plan}
                    onChange={(e) => setNewUser({...newUser, plan: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                  >
                    <option value="basic">Basic</option>
                    <option value="premium">Premium</option>
                    <option value="pro">Pro</option>
                  </select>
                </div>
                <div className="md:col-span-2 lg:col-span-4">
                  <button
                    type="submit"
                    className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-2 px-6 rounded-lg transition-colors"
                  >
                    Crear Usuario
                  </button>
                </div>
              </form>
            </div>

            {/* Users List */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-semibold mb-4">Usuarios Registrados</h2>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-700">
                      <th className="text-left py-3">Username</th>
                      <th className="text-left py-3">Email</th>
                      <th className="text-left py-3">Rol</th>
                      <th className="text-left py-3">Plan</th>
                      <th className="text-left py-3">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((user, index) => (
                      <tr key={index} className="border-b border-gray-700">
                        <td className="py-3">{user.username}</td>
                        <td className="py-3">{user.email}</td>
                        <td className="py-3">
                          <span className={`px-2 py-1 rounded text-xs ${
                            user.role === 'admin' ? 'bg-red-600' : 'bg-blue-600'
                          }`}>
                            {user.role}
                          </span>
                        </td>
                        <td className="py-3">
                          <span className={`px-2 py-1 rounded text-xs ${
                            user.plan === 'pro' ? 'bg-yellow-600' : 
                            user.plan === 'premium' ? 'bg-purple-600' : 'bg-gray-600'
                          }`}>
                            {user.plan || 'basic'}
                          </span>
                        </td>
                        <td className="py-3">
                          <div className="flex space-x-2">
                            <select
                              value={user.plan || 'basic'}
                              onChange={(e) => updateUserPlan(user.username, e.target.value)}
                              className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-xs"
                            >
                              <option value="basic">Basic</option>
                              <option value="premium">Premium</option>
                              <option value="pro">Pro</option>
                            </select>
                            <button
                              onClick={() => deleteUser(user.username)}
                              className="text-red-400 hover:text-red-300 p-1"
                              title="Eliminar usuario"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* PayPal Tab */}
        {activeTab === 'paypal' && (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <CreditCard className="w-5 h-5 mr-2" />
              Configuración de PayPal
            </h2>
            <form onSubmit={savePaypalConfig} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">PayPal Email</label>
                  <input
                    type="email"
                    value={paypalConfig.paypal_email}
                    onChange={(e) => setPaypalConfig({...paypalConfig, paypal_email: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                    placeholder="tu-email@paypal.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Merchant ID</label>
                  <input
                    type="text"
                    value={paypalConfig.paypal_merchant_id}
                    onChange={(e) => setPaypalConfig({...paypalConfig, paypal_merchant_id: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                    placeholder="Tu Merchant ID de PayPal"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Client ID</label>
                  <input
                    type="text"
                    value={paypalConfig.paypal_client_id}
                    onChange={(e) => setPaypalConfig({...paypalConfig, paypal_client_id: e.target.value})}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2"
                    placeholder="Tu Client ID de PayPal"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Client Secret</label>
                  <div className="relative">
                    <input
                      type={showPaypalSecret ? "text" : "password"}
                      value={paypalConfig.paypal_secret}
                      onChange={(e) => setPaypalConfig({...paypalConfig, paypal_secret: e.target.value})}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 pr-10"
                      placeholder="Tu Client Secret de PayPal"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPaypalSecret(!showPaypalSecret)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
                    >
                      {showPaypalSecret ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              </div>
              <div className="pt-4">
                <button
                  type="submit"
                  className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-2 px-6 rounded-lg transition-colors"
                >
                  Guardar Configuración
                </button>
              </div>
            </form>
            
            <div className="mt-6 p-4 bg-blue-900/20 border border-blue-700 rounded-lg">
              <h3 className="font-semibold text-blue-400 mb-2">Información de PayPal</h3>
              <p className="text-sm text-gray-300">
                Para obtener tu Client ID y Client Secret, ve a <a href="https://developer.paypal.com" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">developer.paypal.com</a> y crea una aplicación.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
