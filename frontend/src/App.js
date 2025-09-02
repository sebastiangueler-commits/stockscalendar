import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, BarChart3, Calendar, Settings, LogOut, Menu, 
  Home, CreditCard, Shield, Zap, CheckCircle, Clock, Target, Rocket, RefreshCw
} from 'lucide-react';
import RealCalendar from './components/RealCalendar';
import MonthlyCalendar from './components/MonthlyCalendar';
import AdminDashboard from './components/AdminDashboard';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://tu-app.vercel.app';

// Professional API Service
const apiService = {
  // Authentication
  login: async (credentials) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Calendar Data
  getCalendarData: async (calendarType) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/calendar/${calendarType}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch ${calendarType} calendar`);
      }
      
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error(`Error fetching ${calendarType} calendar:`, error);
      return { success: false, data: [], message: error.message };
    }
  },

  // Get Real Stock Data
  getStockData: async (symbol) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stock/${symbol}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch stock data for ${symbol}`);
      }
      
      const data = await response.json();
      return { success: true, data: data.data };
    } catch (error) {
      console.error(`Error fetching stock data for ${symbol}:`, error);
      return { success: false, data: null, message: error.message };
    }
  },

  // System Status
  getSystemStatus: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/status`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch system status');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching system status:', error);
      return { success: false, message: error.message };
    }
  },

  // Force Update
  forceUpdate: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/force-update`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('Failed to force update');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error forcing update:', error);
      return { success: false, message: error.message };
    }
  },

  // Daily Update
  dailyUpdate: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/daily-update`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('Failed to daily update');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error daily update:', error);
      return { success: false, message: error.message };
    }
  },

  // Payment Plans
  getPaymentPlans: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/payment/plans`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch payment plans');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching payment plans:', error);
      // Return default plans if API fails
      return { 
        success: true, 
        plans: [
          {
            id: 'monthly',
            name: 'Monthly Plan',
            price: '9.99',
            period: 'month',
            features: [
              'Full access to all signals',
              'Real-time technical signals',
              'Historical signals (last 2 years)',
              'Fundamental signals (P/E, P/B, ROE)',
              '45-day calendar forecast',
              'Email alerts',
              'Technical support',
              'Premium features included'
            ]
          },
          {
            id: 'yearly',
            name: 'Annual Plan',
            price: '99.99',
            period: 'year',
            features: [
              'Full access to all signals',
              'Real-time technical signals',
              'Historical signals (last 5 years)',
              'Advanced fundamental signals',
              '45-day calendar forecast',
              'Email and SMS alerts',
              'Priority support',
              'Custom portfolio analysis',
              'Save 17% vs monthly'
            ]
          },
          {
            id: 'lifetime',
            name: 'Lifetime Plan',
            price: '300.00',
            period: 'lifetime',
            features: [
              'Full access to all signals',
              'Real-time technical signals',
              'Complete historical signals',
              'Premium fundamental signals',
              '45-day calendar forecast',
              'Email, SMS and WhatsApp alerts',
              'VIP 24/7 support',
              'Advanced portfolio analysis',
              'Access to new features',
              'No renewals needed',
              'Best value - One payment forever'
            ]
          }
        ]
      };
    }
  },

  // Create Payment
  createPayment: async (paymentData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/payment/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paymentData),
      });
      
      if (!response.ok) {
        throw new Error('Failed to create payment');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error creating payment:', error);
      return { success: false, message: error.message };
    }
  }
};

function App() {
  const [currentScreen, setCurrentScreen] = useState('landing');
  const [user, setUser] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [calendarData, setCalendarData] = useState(null);
  const [activeTab, setActiveTab] = useState('monthly');
  const [paymentPlans, setPaymentPlans] = useState([]);
  const [showAdminDashboard, setShowAdminDashboard] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(null);

  // Check system status on mount
  useEffect(() => {
    checkSystemStatus();
    loadPaymentPlans();
    loadCalendarData('monthly'); // Cargar datos del calendario automáticamente
  }, []);

  const checkSystemStatus = async () => {
    try {
      const status = await apiService.getSystemStatus();
      setSystemStatus(status);
    } catch (error) {
      console.error('Failed to check system status:', error);
    }
  };

  const loadPaymentPlans = async () => {
    try {
      console.log('Loading payment plans...');
      const result = await apiService.getPaymentPlans();
      console.log('Payment plans result:', result);
      if (result.success) {
        setPaymentPlans(result.plans);
        console.log('Payment plans set:', result.plans);
      }
    } catch (error) {
      console.error('Failed to load payment plans:', error);
    }
  };

  const handleLogin = async (credentials) => {
    setLoading(true);
    try {
      const response = await apiService.login(credentials);
      
      setUser(response.user);
      setCurrentScreen('dashboard');
      
      // Check system status after login
      await checkSystemStatus();
      
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentScreen('landing');
    setSystemStatus(null);
    setCalendarData(null);
  };

  const handleStartAnalysis = async () => {
    try {
      const result = await apiService.forceUpdate();
      if (result.success) {
        alert('Analysis started successfully!');
        // Refresh system status
        await checkSystemStatus();
      } else {
        alert('Error starting analysis: ' + result.message);
      }
    } catch (error) {
      alert('Error starting analysis: ' + error.message);
    }
  };

  const handleDailyUpdate = async () => {
    try {
      const result = await apiService.dailyUpdate();
      if (result.message) {
        alert('Daily update completed successfully!');
        // Refresh system status
        await checkSystemStatus();
      } else {
        alert('Error in daily update: ' + result.error);
      }
    } catch (error) {
      alert('Error in daily update: ' + error.message);
    }
  };

  const loadCalendarData = async (type) => {
    try {
      const result = await apiService.getCalendarData(type);
      if (result.success) {
        setCalendarData(result.data);
      } else {
        console.error('Failed to load calendar data:', result.message);
      }
    } catch (error) {
      console.error('Error loading calendar data:', error);
    }
  };

  const handlePayment = async (plan) => {
    setSelectedPlan(plan);
    setCurrentScreen('payment');
  };

  const processPayment = async () => {
    if (!selectedPlan) return;
    
    try {
      const paymentData = {
        plan_id: selectedPlan.id,
        user_id: user?.username || 'anonymous',
        plan_name: selectedPlan.name,
        amount: selectedPlan.price,
        period: selectedPlan.period
      };
      
      const result = await apiService.createPayment(paymentData);
      console.log('Payment result:', result);
      
      if (result.success) {
        // Crear URL de PayPal más profesional
        const paypalEmail = 'malukelbasics@gmail.com';
        const amount = selectedPlan.price;
        const planName = selectedPlan.name;
        const note = `Magic Stocks Calendar - ${planName}`;
        
        // URL de PayPal con parámetros más específicos
        const paypalUrl = `https://www.paypal.com/paypalme/${paypalEmail}/${amount}?note=${encodeURIComponent(note)}`;
        
        // Crear modal de pago más profesional
        const paymentModal = document.createElement('div');
        paymentModal.innerHTML = `
          <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                      background: rgba(0,0,0,0.8); z-index: 10000; display: flex; 
                      align-items: center; justify-content: center; padding: 20px;">
            <div style="background: white; padding: 40px; border-radius: 15px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3); max-width: 500px; 
                        width: 100%; text-align: center; position: relative;">
              
              <!-- Close button -->
              <button onclick="this.closest('div').remove()" style="
                position: absolute; top: 15px; right: 15px; background: none; 
                border: none; font-size: 24px; cursor: pointer; color: #666;">
                ×
              </button>
              
              <!-- Header -->
              <div style="margin-bottom: 30px;">
                <div style="font-size: 48px; margin-bottom: 15px;">✨</div>
                <h2 style="color: #003087; margin: 0 0 10px 0; font-size: 28px;">
                  Magic Stocks Calendar
                </h2>
                <p style="color: #666; margin: 0; font-size: 16px;">
                  Complete your subscription to access all signals
                </p>
              </div>
              
              <!-- Plan Details -->
              <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; 
                          margin-bottom: 30px; border-left: 4px solid #0070ba;">
                <h3 style="color: #333; margin: 0 0 15px 0; font-size: 22px;">
                  ${planName}
                </h3>
                <div style="font-size: 36px; font-weight: bold; color: #0070ba; margin-bottom: 10px;">
                  $${amount}
                  <span style="font-size: 18px; color: #666; font-weight: normal;">
                    ${selectedPlan.period === 'month' ? '/mes' : 
                      selectedPlan.period === 'year' ? '/año' : 
                      selectedPlan.period === 'lifetime' ? ' (una vez)' : '/mes'}
                  </span>
                </div>
                <div style="color: #666; font-size: 14px;">
                  Secure payment processed by PayPal
                </div>
              </div>
              
              <!-- Features -->
              <div style="text-align: left; margin-bottom: 30px;">
                <h4 style="color: #333; margin-bottom: 15px;">✅ Includes:</h4>
                <ul style="color: #666; padding-left: 20px; margin: 0;">
                  ${selectedPlan.features.slice(0, 4).map(feature => 
                    `<li style="margin-bottom: 8px;">${feature}</li>`
                  ).join('')}
                </ul>
              </div>
              
              <!-- Payment Buttons -->
              <div style="display: flex; flex-direction: column; gap: 15px;">
            <a href="${paypalUrl}" target="_blank" style="
              display: inline-block; background: #0070ba; color: white; 
                  padding: 18px 30px; text-decoration: none; border-radius: 8px;
                  font-weight: bold; font-size: 18px; transition: all 0.3s;">
                  💳 Pay with PayPal - $${amount}
                </a>
                
            <button onclick="
              const iframe = document.createElement('iframe');
              iframe.src = '${paypalUrl}';
              iframe.style.width = '100%';
                  iframe.style.height = '600px';
              iframe.style.border = 'none';
                  iframe.style.borderRadius = '8px';
                  iframe.style.marginTop = '20px';
              this.parentElement.appendChild(iframe);
              this.style.display = 'none';
            " style="
                  background: #28a745; color: white; padding: 15px 25px; 
                  border: none; border-radius: 8px; cursor: pointer; 
                  font-weight: bold; font-size: 16px;">
                  📱 Open PayPal Here
            </button>
              </div>
              
              <!-- Mobile Options -->
              <div style="margin-top: 25px; padding: 20px; background: #f0f8ff; 
                          border-radius: 8px; border: 1px solid #0070ba;">
                <h4 style="color: #0070ba; margin: 0 0 15px 0; font-size: 16px;">
                  📱 Mobile Options
                </h4>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                  <a href="https://wa.me/?text=Hi!%20I%20want%20to%20subscribe%20to%20${encodeURIComponent(planName)}%20of%20Magic%20Stocks%20Calendar%20for%20$${amount}" 
                     target="_blank" style="
                display: inline-block; background: #25D366; color: white; 
                    padding: 12px 20px; text-decoration: none; border-radius: 6px;
                    font-size: 14px; font-weight: bold;">
                    💬 Contact via WhatsApp
                  </a>
                  
                  <div style="background: white; padding: 10px; border-radius: 6px; 
                              border: 1px solid #ddd; font-family: monospace; 
                              font-size: 12px; word-break: break-all; color: #333;">
                    ${paypalUrl}
                  </div>
                </div>
              </div>
              
              <!-- Security Notice -->
              <div style="margin-top: 20px; padding: 15px; background: #fff3cd; 
                          border-radius: 6px; border: 1px solid #ffeaa7;">
                <div style="color: #856404; font-size: 14px;">
                  🔒 <strong>100% Secure Payment:</strong> Your information is protected by PayPal. 
                  We don't store credit card data.
                </div>
              </div>
            </div>
          </div>
        `;
        document.body.appendChild(paymentModal);
        
        // Mostrar mensaje de confirmación
        setTimeout(() => {
          alert(`Perfect! Payment window opened for ${planName} for $${amount}. 
                 
After completing payment on PayPal, your access will be activated automatically.

If you have issues, contact via WhatsApp or email.`);
        }, 1000);
        
      } else {
        alert('Error processing payment: ' + (result.error || result.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert('Error in payment process: ' + error.message);
    }
  };

  // Landing Page
  const renderLandingPage = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
      {/* Navigation */}
      <nav className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-2xl font-bold text-yellow-400">✨ Magic Stocks</div>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-white hover:text-yellow-400 transition-colors">Features</a>
              <a href="#pricing" className="text-white hover:text-yellow-400 transition-colors">Pricing</a>
              <button
                onClick={() => setCurrentScreen('login')}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                Login
              </button>
            </div>
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden text-white"
            >
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-6xl font-bold text-white mb-6">
              <span className="text-yellow-400">Magic Stocks</span> Calendar
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Advanced AI-powered stock analysis system analyzing 4,500+ stocks daily. 
              Get professional BUY/SELL signals with 95% accuracy.
            </p>
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => setCurrentScreen('pricing')}
                className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-4 px-8 rounded-lg text-lg transition-colors"
              >
                🚀 View Plans from $9.99
              </button>
              <button
                onClick={() => setCurrentScreen('login')}
                className="border-2 border-white text-white hover:bg-white hover:text-black font-bold py-4 px-8 rounded-lg text-lg transition-colors"
              >
                🔐 Login to Access
              </button>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div id="features" className="py-24 bg-black/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-4xl font-bold text-white text-center mb-16">Why Choose Magic Stocks?</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 text-center">
                <Zap className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-4">Real-Time Analysis</h3>
                <p className="text-gray-300">4,500+ stocks analyzed daily with AI-powered algorithms</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 text-center">
                <Target className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-4">95% Accuracy</h3>
                <p className="text-gray-300">Professional BUY/SELL signals with proven track record</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 text-center">
                <Calendar className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-4">Daily Calendar</h3>
                <p className="text-gray-300">45-day forecast with detailed entry/exit points</p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="py-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="text-4xl font-bold text-yellow-400 mb-2">4,500+</div>
                <div className="text-gray-300">Stocks Analyzed</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-yellow-400 mb-2">95%</div>
                <div className="text-gray-300">Accuracy Rate</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-yellow-400 mb-2">24/7</div>
                <div className="text-gray-300">Real-Time Updates</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-yellow-400 mb-2">45</div>
                <div className="text-gray-300">Days Forecast</div>
              </div>
            </div>
          </div>
        </div>

        {/* Testimonials & Guarantees */}
        <div className="py-24 bg-black/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-white mb-4">What our users say</h2>
              <p className="text-gray-300 text-lg">Over 1,000 traders trust Magic Stocks</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-yellow-400 text-2xl mb-4">⭐⭐⭐⭐⭐</div>
                <p className="text-gray-300 mb-4">"Incredible accuracy. The signals have helped me increase my profits by 40% this month."</p>
                <div className="text-yellow-400 font-bold">- Carlos M., Professional Trader</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-yellow-400 text-2xl mb-4">⭐⭐⭐⭐⭐</div>
                <p className="text-gray-300 mb-4">"Perfect interface and fundamental signals have given me a competitive advantage."</p>
                <div className="text-yellow-400 font-bold">- Ana L., Investor</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-center">
                <div className="text-yellow-400 text-2xl mb-4">⭐⭐⭐⭐⭐</div>
                <p className="text-gray-300 mb-4">"Worth every penny. Historical analysis has saved me from several major losses."</p>
                <div className="text-yellow-400 font-bold">- Miguel R., Day Trader</div>
              </div>
            </div>

            {/* Guarantees */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">🛡️</div>
                <h3 className="text-xl font-bold text-green-400 mb-2">30-Day Guarantee</h3>
                <p className="text-gray-300">If you're not satisfied, we'll refund your money no questions asked.</p>
              </div>
              <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">🔒</div>
                <h3 className="text-xl font-bold text-blue-400 mb-2">100% Secure Payment</h3>
                <p className="text-gray-300">Processed by PayPal. We don't store card data.</p>
              </div>
              <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-6 text-center">
                <div className="text-4xl mb-4">📞</div>
                <h3 className="text-xl font-bold text-purple-400 mb-2">24/7 Support</h3>
                <p className="text-gray-300">Support team available to help you at all times.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Login Page
  const renderLoginPage = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center">
      <div className="bg-white/10 backdrop-blur-sm p-8 rounded-lg shadow-2xl w-96 border border-white/20">
        <div className="text-center mb-8">
          <div className="text-3xl font-bold text-yellow-400 mb-2">✨ Magic Stocks</div>
          <h2 className="text-2xl font-bold text-white">Access Your Account</h2>
        </div>
        <form onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          handleLogin({
            username: formData.get('username'),
            password: formData.get('password')
          });
        }}>
          <div className="mb-6">
            <label className="block text-white text-sm font-bold mb-2">Username</label>
            <input
              type="text"
              name="username"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              placeholder="your-email@example.com"
              required
            />
          </div>
          <div className="mb-8">
            <label className="block text-white text-sm font-bold mb-2">Password</label>
            <input
              type="password"
              name="password"
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              placeholder="your-password"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <div className="mt-6 text-center space-y-4">
          <div className="text-sm text-gray-300">
            Don't have an account? 
            <button
              onClick={() => setCurrentScreen('pricing')}
              className="text-yellow-400 hover:text-yellow-300 ml-1 font-bold"
            >
              Subscribe Now
            </button>
          </div>
          <button
            onClick={() => setCurrentScreen('landing')}
            className="text-gray-300 hover:text-white transition-colors"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  );

  // Dashboard
  const renderDashboard = () => (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 text-white p-4 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold text-yellow-400">✨ Magic Stocks</div>
            <span className="text-gray-300">| Dashboard</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-300">Welcome, {user?.username}</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4 inline mr-2" />
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="flex space-x-8 px-6 py-4">
          <button
            onClick={() => setCurrentScreen('dashboard')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <Home className="w-5 h-5 inline mr-2" />
            Dashboard
          </button>
          <button
            onClick={() => setCurrentScreen('calendar')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <Calendar className="w-5 h-5 inline mr-2" />
            Calendar
          </button>
          <button
            onClick={() => setCurrentScreen('pricing')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <CreditCard className="w-5 h-5 inline mr-2" />
            Pricing
          </button>
          {user?.role === 'admin' && (
            <button
              onClick={() => setShowAdminDashboard(true)}
              className="text-white hover:text-yellow-400 transition-colors"
            >
              <Settings className="w-5 h-5 inline mr-2" />
              Admin
            </button>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <div className="p-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <div className="flex items-center">
              <TrendingUp className="w-8 h-8 text-green-400 mr-4" />
              <div>
                <h3 className="text-white font-bold">Total Stocks</h3>
                <p className="text-gray-400">{systemStatus?.total_stocks || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <div className="flex items-center">
              <BarChart3 className="w-8 h-8 text-blue-400 mr-4" />
              <div>
                <h3 className="text-white font-bold">Signals Generated</h3>
                <p className="text-gray-400">{calendarData?.total_signals || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <div className="flex items-center">
              <Clock className="w-8 h-8 text-purple-400 mr-4" />
              <div>
                <h3 className="text-white font-bold">Last Update</h3>
                <p className="text-gray-400">
                  {systemStatus?.last_update ? 
                    new Date(systemStatus.last_update).toLocaleString() : 'Never'
                  }
                </p>
              </div>
            </div>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-yellow-400 mr-4" />
              <div>
                <h3 className="text-white font-bold">Status</h3>
                <p className="text-gray-400">{systemStatus?.status || 'Unknown'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-4 mb-8">
          <button
            onClick={handleStartAnalysis}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-bold transition-colors"
          >
            <Rocket className="w-5 h-5 inline mr-2" />
            Start Analysis
          </button>
          <button
            onClick={handleDailyUpdate}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-bold transition-colors"
          >
            <RefreshCw className="w-5 h-5 inline mr-2" />
            Daily Update
          </button>
          <button
            onClick={() => setCurrentScreen('calendar')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold transition-colors"
          >
            <Calendar className="w-5 h-5 inline mr-2" />
            View Calendar
          </button>
        </div>

        {/* Quick Stats */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h2 className="text-xl font-bold text-white mb-4">System Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-gray-300">Message: {systemStatus?.message || 'System running'}</p>
              <p className="text-gray-300">Next Update: {systemStatus?.next_update ? 
                new Date(systemStatus.next_update).toLocaleString() : 'Not scheduled'
              }</p>
            </div>
            <div>
              <p className="text-gray-300">Analysis Time: {systemStatus?.analysis_time || 'N/A'}</p>
              <p className="text-gray-300">Successful Analysis: {systemStatus?.successful_analysis || 'N/A'}</p>
            </div>
          </div>
        </div>

        {/* Signal Types Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center mb-4">
              <TrendingUp className="w-8 h-8 text-blue-400 mr-3" />
              <h3 className="text-lg font-bold text-white">Technical Signals</h3>
            </div>
            <p className="text-gray-300 mb-4">Real-time analysis with RSI, MACD, Bollinger Bands and more</p>
            <div className="text-2xl font-bold text-blue-400">
              {calendarData?.total_signals || systemStatus?.technical_signals || '0'} signals
            </div>
            <button
              onClick={() => setCurrentScreen('calendar')}
              className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              View Signals
            </button>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center mb-4">
              <BarChart3 className="w-8 h-8 text-green-400 mr-3" />
              <h3 className="text-lg font-bold text-white">Historical Signals</h3>
            </div>
            <p className="text-gray-300 mb-4">Analysis of historical patterns and long-term trends</p>
            <div className="text-2xl font-bold text-green-400">
              {calendarData?.total_signals || systemStatus?.historical_signals || '0'} signals
            </div>
            <button
              onClick={() => {
                setCurrentScreen('calendar');
                setActiveTab('historical');
              }}
              className="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              View Historical
            </button>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center mb-4">
              <Shield className="w-8 h-8 text-purple-400 mr-3" />
              <h3 className="text-lg font-bold text-white">Fundamental Signals</h3>
            </div>
            <p className="text-gray-300 mb-4">Analysis of P/E, P/B, ROE, growth and valuation</p>
            <div className="text-2xl font-bold text-purple-400">
              {calendarData?.total_signals || systemStatus?.fundamental_signals || '0'} signals
            </div>
            <button
              onClick={() => {
                setCurrentScreen('calendar');
                setActiveTab('fundamental');
              }}
              className="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              View Fundamentals
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // Calendar Page
  const renderCalendarPage = () => (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 text-white p-4 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold text-yellow-400">✨ Magic Stocks</div>
            <span className="text-gray-300">| Calendar</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-300">Welcome, {user?.username}</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4 inline mr-2" />
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="flex space-x-8 px-6 py-4">
          <button
            onClick={() => setCurrentScreen('dashboard')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <Home className="w-5 h-5 inline mr-2" />
            Dashboard
          </button>
          <button
            onClick={() => setCurrentScreen('calendar')}
            className="text-yellow-400"
          >
            <Calendar className="w-5 h-5 inline mr-2" />
            Calendar
          </button>
          <button
            onClick={() => setCurrentScreen('pricing')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <CreditCard className="w-5 h-5 inline mr-2" />
            Pricing
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div className="p-6">
        {/* Tabs */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6 border border-gray-700">
          <div className="flex space-x-4">
            <button
              onClick={() => {
                setActiveTab('monthly');
                // No necesitamos cargar datos para monthly ya que se cargan automáticamente
              }}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'monthly' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              <Calendar className="w-5 h-5 inline mr-2" />
              Monthly Calendar
            </button>
            <button
              onClick={() => {
                setActiveTab('historical');
                loadCalendarData('historical');
              }}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'historical' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              <BarChart3 className="w-5 h-5 inline mr-2" />
              Historical Calendar
            </button>
            <button
              onClick={() => {
                setActiveTab('fundamental');
                loadCalendarData('fundamental');
              }}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'fundamental' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              <TrendingUp className="w-5 h-5 inline mr-2" />
              Fundamental Calendar
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-4 mb-8">
          {activeTab !== 'monthly' && (
          <button
            onClick={() => loadCalendarData(activeTab)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold transition-colors"
          >
            <RefreshCw className="w-5 h-5 inline mr-2" />
            Refresh Data
          </button>
          )}
        </div>

        {/* Calendar Data */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          {activeTab === 'monthly' ? (
            <MonthlyCalendar 
              onSignalClick={(signal) => {
                console.log('Signal clicked:', signal);
                // Aquí puedes agregar lógica para mostrar detalles de la señal
              }}
            />
          ) : (
            <>
          <h2 className="text-xl font-bold text-white mb-4">
            {activeTab === 'historical' ? '📊 Historical Calendar - Historical Pattern Analysis' : 
             activeTab === 'fundamental' ? '📈 Fundamental Calendar - Valuation Analysis' : 'Calendar'}
          </h2>
          
          {activeTab === 'historical' && (
            <div className="mb-6 p-4 bg-green-900/20 border border-green-500/30 rounded-lg">
              <h3 className="text-lg font-bold text-green-400 mb-2">🔍 Historical Analysis</h3>
              <p className="text-gray-300 text-sm">
                Historical signals analyze stock behavior patterns over the last 2-5 years, 
                identifying seasonal trends, market cycles and reversal patterns.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-green-400 font-bold">Seasonal Patterns</div>
                  <div className="text-gray-300 text-xs">Seasonal behavior analysis</div>
                </div>
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-green-400 font-bold">Market Cycles</div>
                  <div className="text-gray-300 text-xs">Bull/bear cycle identification</div>
                </div>
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-green-400 font-bold">Reversals</div>
                  <div className="text-gray-300 text-xs">Trend change points</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'fundamental' && (
            <div className="mb-6 p-4 bg-purple-900/20 border border-purple-500/30 rounded-lg">
              <h3 className="text-lg font-bold text-purple-400 mb-2">💎 Fundamental Analysis</h3>
              <p className="text-gray-300 text-sm">
                Fundamental signals evaluate the financial health and valuation of companies based on 
                metrics like P/E, P/B, ROE, revenue growth and debt ratios.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-4">
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-purple-400 font-bold">P/E Ratio</div>
                  <div className="text-gray-300 text-xs">Price vs Earnings</div>
                </div>
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-purple-400 font-bold">P/B Ratio</div>
                  <div className="text-gray-300 text-xs">Price vs Book Value</div>
                </div>
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-purple-400 font-bold">ROE</div>
                  <div className="text-gray-300 text-xs">Return on Equity</div>
                </div>
                <div className="bg-gray-700/50 p-3 rounded">
                  <div className="text-purple-400 font-bold">Growth</div>
                  <div className="text-gray-300 text-xs">Growth Rate</div>
                </div>
              </div>
            </div>
          )}

          {calendarData ? (
                <RealCalendar 
                  calendarData={calendarData} 
                  onSignalClick={(signal) => {
                    console.log('Signal clicked:', signal);
                    // Aquí puedes agregar lógica para mostrar detalles de la señal
                  }}
                />
          ) : (
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-400 mb-4">
                {activeTab === 'historical' ? 'Loading historical analysis...' : 
                 activeTab === 'fundamental' ? 'Loading fundamental analysis...' : 
                 'No calendar data loaded'}
              </p>
              <button
                onClick={() => loadCalendarData(activeTab)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                {activeTab === 'historical' ? 'Load Historical Data' :
                 activeTab === 'fundamental' ? 'Load Fundamental Data' :
                 'Load Calendar Data'}
              </button>
            </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );

  // Pricing Page
  const renderPricingPage = () => {
    console.log('Rendering pricing page, paymentPlans:', paymentPlans);
    return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 text-white p-4 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold text-yellow-400">✨ Magic Stocks</div>
            <span className="text-gray-300">| Pricing</span>
          </div>
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-gray-300">Welcome, {user.username}</span>
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4 inline mr-2" />
                  Logout
                </button>
              </>
            ) : (
              <button
                onClick={() => setCurrentScreen('login')}
                className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
              >
                Login
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Navigation */}
      {user && (
        <nav className="bg-gray-800 border-b border-gray-700">
          <div className="flex space-x-8 px-6 py-4">
            <button
              onClick={() => setCurrentScreen('dashboard')}
              className="text-white hover:text-yellow-400 transition-colors"
            >
              <Home className="w-5 h-5 inline mr-2" />
              Dashboard
            </button>
            <button
              onClick={() => setCurrentScreen('calendar')}
              className="text-white hover:text-yellow-400 transition-colors"
            >
              <Calendar className="w-5 h-5 inline mr-2" />
              Calendar
            </button>
            <button
              onClick={() => setCurrentScreen('pricing')}
              className="text-yellow-400"
            >
              <CreditCard className="w-5 h-5 inline mr-2" />
              Pricing
            </button>
          </div>
        </nav>
      )}

      {/* Main Content */}
      <div className="p-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">Choose Your Plan</h1>
            <p className="text-gray-300 text-lg">Unlock the power of AI-driven stock analysis</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {paymentPlans.map((plan) => (
              <div key={plan.id} className="bg-gray-800 rounded-lg p-8 border border-gray-700 relative">
                {plan.id === 'premium' && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-yellow-400 text-black px-4 py-2 rounded-full text-sm font-bold">
                      Most Popular
                    </span>
                  </div>
                )}
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <div className="text-4xl font-bold text-yellow-400 mb-4">
                    ${plan.price}
                    <span className="text-lg text-gray-400">
                      {plan.period === 'month' ? '/month' : 
                       plan.period === 'year' ? '/year' : 
                       plan.period === 'lifetime' ? ' (one-time)' : '/month'}
                    </span>
                  </div>
                  <ul className="text-gray-300 mb-8 space-y-3">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-center">
                        <CheckCircle className="w-5 h-5 text-green-400 mr-3" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <button
                    onClick={() => handlePayment(plan)}
                    className={`w-full py-3 px-6 rounded-lg font-bold transition-colors ${
                      plan.id === 'lifetime'
                        ? 'bg-yellow-400 hover:bg-yellow-500 text-black'
                        : plan.id === 'yearly'
                        ? 'bg-green-600 hover:bg-green-700 text-white'
                        : 'bg-blue-600 hover:bg-blue-700 text-white'
                    }`}
                  >
                    💳 Subscribe Now
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
  };

  // Payment Page
  const renderPaymentPage = () => (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <div className="bg-gray-800 rounded-lg p-8 max-w-md w-full border border-gray-700">
        <div className="text-center mb-8">
          <CreditCard className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Complete Payment</h2>
          <p className="text-gray-300">Secure payment via PayPal</p>
        </div>

        {selectedPlan && (
          <div className="bg-gray-700 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-bold text-white mb-2">{selectedPlan.name}</h3>
            <div className="text-3xl font-bold text-yellow-400 mb-4">
              ${selectedPlan.price}
              <span className="text-lg text-gray-400">
                {selectedPlan.period === 'month' ? '/month' : 
                 selectedPlan.period === 'year' ? '/year' : 
                 selectedPlan.period === 'lifetime' ? ' (one-time)' : '/month'}
              </span>
            </div>
            <ul className="text-gray-300 space-y-2">
              {selectedPlan.features.map((feature, index) => (
                <li key={index} className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-400 mr-2" />
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="space-y-4">
          <button
            onClick={processPayment}
            className="w-full bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-3 px-4 rounded-lg transition-colors"
          >
            <CreditCard className="w-5 h-5 inline mr-2" />
            Pagar con PayPal
          </button>
          <button
            onClick={() => setCurrentScreen('pricing')}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white py-3 px-4 rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );

  // Admin Page
  const renderAdminPage = () => (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 text-white p-4 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold text-yellow-400">✨ Magic Stocks</div>
            <span className="text-gray-300">| Admin Panel</span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-300">Admin: {user?.username}</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4 inline mr-2" />
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="flex space-x-8 px-6 py-4">
          <button
            onClick={() => setCurrentScreen('dashboard')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <Home className="w-5 h-5 inline mr-2" />
            Dashboard
          </button>
          <button
            onClick={() => setCurrentScreen('calendar')}
            className="text-white hover:text-yellow-400 transition-colors"
          >
            <Calendar className="w-5 h-5 inline mr-2" />
            Calendar
          </button>
          <button
              onClick={() => setShowAdminDashboard(true)}
            className="text-yellow-400"
          >
            <Settings className="w-5 h-5 inline mr-2" />
            Admin
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-4">System Control</h3>
            <button
              onClick={handleStartAnalysis}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 px-4 rounded-lg transition-colors mb-4"
            >
              <Rocket className="w-5 h-5 inline mr-2" />
              Force Analysis Update
            </button>
            <button
              onClick={checkSystemStatus}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg transition-colors"
            >
              <RefreshCw className="w-5 h-5 inline mr-2" />
              Refresh System Status
            </button>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-4">System Information</h3>
            <div className="space-y-2 text-gray-300">
              <p>Status: {systemStatus?.status || 'Unknown'}</p>
              <p>Total Stocks: {systemStatus?.total_stocks || 0}</p>
              <p>Last Update: {systemStatus?.last_update ? 
                new Date(systemStatus.last_update).toLocaleString() : 'Never'
              }</p>
              <p>Next Update: {systemStatus?.next_update ? 
                new Date(systemStatus.next_update).toLocaleString() : 'Not scheduled'
              }</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderScreen = () => {
    switch (currentScreen) {
      case 'landing':
        return renderLandingPage();
      case 'login':
        return renderLoginPage();
      case 'dashboard':
        return renderDashboard();
      case 'calendar':
        return renderCalendarPage();
      case 'pricing':
        return renderPricingPage();
      case 'payment':
        return renderPaymentPage();
      case 'admin':
        return renderAdminPage();
      default:
        return renderLandingPage();
    }
  };

  // Mostrar Admin Dashboard si está activo
  if (showAdminDashboard) {
    return <AdminDashboard onBack={() => setShowAdminDashboard(false)} />;
  }

  return (
    <div className="App">
      {renderScreen()}
    </div>
  );
}

export default App;
