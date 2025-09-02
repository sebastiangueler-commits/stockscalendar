import React, { useState, useEffect } from 'react';
import { Calendar, Filter, Search, TrendingUp, TrendingDown, Star, Clock, Target } from 'lucide-react';

const RealCalendar = ({ calendarData, onSignalClick }) => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [filterType, setFilterType] = useState('all'); // all, buy, sell
  const [sortBy, setSortBy] = useState('confidence'); // confidence, price, volume
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSignals, setSelectedSignals] = useState([]);

  // Obtener fechas de los próximos 45 días
  const getNextDays = (days = 45) => {
    const dates = [];
    const today = new Date();
    for (let i = 0; i < days; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date.toISOString().split('T')[0]);
    }
    return dates;
  };

  const dates = getNextDays();

  // Filtrar y ordenar señales
  const getFilteredSignals = (date) => {
    if (!calendarData?.calendar_data?.[date]) return [];

    let signals = [];
    const dayData = calendarData.calendar_data[date];
    
    // Combinar señales BUY y SELL
    if (filterType === 'all' || filterType === 'buy') {
      const buySignals = dayData.buy_signals || dayData.signals?.filter(s => s.type === 'BUY') || [];
      signals.push(...buySignals.map(s => ({ ...s, signalType: 'BUY' })));
    }
    if (filterType === 'all' || filterType === 'sell') {
      const sellSignals = dayData.sell_signals || dayData.signals?.filter(s => s.type === 'SELL') || [];
      signals.push(...sellSignals.map(s => ({ ...s, signalType: 'SELL' })));
    }

    // Filtrar por búsqueda
    if (searchTerm) {
      signals = signals.filter(signal => 
        signal.symbol.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Ordenar
    signals.sort((a, b) => {
      switch (sortBy) {
        case 'confidence':
          return b.confidence - a.confidence;
        case 'price':
          return b.price - a.price;
        case 'volume':
          return b.volume - a.volume;
        default:
          return b.confidence - a.confidence;
      }
    });

    return signals.slice(0, 6); // Máximo 6 señales por día
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value);
  };

  const formatNumber = (value) => {
    if (value >= 1e9) {
      return `${(value / 1e9).toFixed(1)}B`;
    } else if (value >= 1e6) {
      return `${(value / 1e6).toFixed(1)}M`;
    } else if (value >= 1e3) {
      return `${(value / 1e3).toFixed(1)}K`;
    }
    return value.toLocaleString();
  };

  const getSignalColor = (signalType) => {
    return signalType === 'BUY' ? 'text-green-400' : 'text-red-400';
  };

  const getSignalBgColor = (signalType) => {
    return signalType === 'BUY' ? 'bg-green-900/20' : 'bg-red-900/20';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 0.8) return 'text-green-400';
    if (confidence > 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const handleDateClick = (date) => {
    setSelectedDate(date);
  };

  const handleSignalClick = (signal) => {
    if (onSignalClick) {
      onSignalClick(signal);
    }
  };

  return (
    <div className="space-y-6">
      {/* Filtros y controles */}
      <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
        <div className="flex flex-wrap gap-4 items-center">
          {/* Filtro por tipo */}
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-400" />
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="bg-gray-700 text-white px-3 py-1 rounded border border-gray-600"
            >
              <option value="all">Todas las señales</option>
              <option value="buy">Solo BUY</option>
              <option value="sell">Solo SELL</option>
            </select>
          </div>

          {/* Ordenar por */}
          <div className="flex items-center space-x-2">
            <span className="text-gray-400 text-sm">Ordenar por:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-gray-700 text-white px-3 py-1 rounded border border-gray-600"
            >
              <option value="confidence">Confianza</option>
              <option value="price">Precio</option>
              <option value="volume">Volumen</option>
            </select>
          </div>

          {/* Búsqueda */}
          <div className="flex items-center space-x-2">
            <Search className="w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar símbolo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-gray-700 text-white px-3 py-1 rounded border border-gray-600"
            />
          </div>
        </div>
      </div>

      {/* Calendario */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {dates.map((date) => {
          const signals = getFilteredSignals(date);
          const hasSignals = signals.length > 0;
          const buyCount = signals.filter(s => s.signalType === 'BUY').length;
          const sellCount = signals.filter(s => s.signalType === 'SELL').length;

          return (
            <div
              key={date}
              className={`bg-gray-800 rounded-lg p-4 border border-gray-700 cursor-pointer transition-all hover:border-gray-600 ${
                selectedDate === date ? 'ring-2 ring-yellow-400' : ''
              }`}
              onClick={() => handleDateClick(date)}
            >
              {/* Fecha */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <Calendar className="w-4 h-4 text-gray-400" />
                  <span className="text-white font-semibold">
                    {new Date(date).toLocaleDateString('es-ES', {
                      weekday: 'short',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </span>
                </div>
                {hasSignals && (
                  <div className="flex items-center space-x-1">
                    <span className="text-xs text-green-400">{buyCount} BUY</span>
                    <span className="text-xs text-red-400">{sellCount} SELL</span>
                  </div>
                )}
              </div>

              {/* Señales */}
              {hasSignals ? (
                <div className="space-y-2">
                  {signals.map((signal, index) => (
                    <div
                      key={`${signal.symbol}-${index}`}
                      className={`p-3 rounded-lg border cursor-pointer transition-all hover:scale-105 ${
                        getSignalBgColor(signal.signalType)
                      } border-gray-600`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleSignalClick(signal);
                      }}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="font-bold text-white">{signal.symbol}</span>
                          <span className={`text-xs px-2 py-1 rounded ${
                            signal.signalType === 'BUY' ? 'bg-green-600' : 'bg-red-600'
                          }`}>
                            {signal.signalType}
                          </span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Star className="w-3 h-3 text-yellow-400" />
                          <span className={`text-xs font-bold ${getConfidenceColor(signal.confidence)}`}>
                            {(signal.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>

                      <div className="text-xs text-gray-300">
                        <div className="mb-1">
                          <span className="text-gray-400">Razón:</span>
                          <span className="text-white ml-1">{signal.reason || 'Análisis fundamental'}</span>
                        </div>
                      </div>

                      <div className="mt-2 text-xs text-gray-400">
                        {signal.source === 'fundamental' ? '📊 Fundamental' : '📈 Técnico'}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Clock className="w-8 h-8 text-gray-500 mx-auto mb-2" />
                  <p className="text-gray-500 text-sm">Sin señales</p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Estadísticas */}
      {calendarData && (
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
            <Target className="w-5 h-5 mr-2" />
            Estadísticas del Calendario
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-white">{calendarData.total_signals || 0}</div>
              <div className="text-gray-400 text-sm">Total Señales</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">{calendarData.buy_count || 0}</div>
              <div className="text-gray-400 text-sm">Señales BUY</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-400">{calendarData.sell_count || 0}</div>
              <div className="text-gray-400 text-sm">Señales SELL</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-400">{dates.length}</div>
              <div className="text-gray-400 text-sm">Días Analizados</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RealCalendar;
