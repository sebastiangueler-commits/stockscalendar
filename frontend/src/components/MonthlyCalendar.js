import React, { useState, useEffect } from 'react';
import { Calendar, TrendingUp, TrendingDown, Star, Target, AlertCircle } from 'lucide-react';

const MonthlyCalendar = ({ calendarData, onSignalClick }) => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedSignal, setSelectedSignal] = useState(null);

  // Obtener datos del calendario mensual
  const getMonthlyData = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/calendar/monthly');
      const data = await response.json();
      return data.monthly_calendar;
    } catch (error) {
      console.error('Error fetching monthly calendar:', error);
      return null;
    }
  };

  const [monthlyData, setMonthlyData] = useState(null);

  useEffect(() => {
    const loadMonthlyData = async () => {
      const data = await getMonthlyData();
      setMonthlyData(data);
    };
    loadMonthlyData();
  }, []);

  // Generar días desde hoy hasta 45 días
  const generateDays = () => {
    const days = [];
    const today = new Date();
    
    for (let i = 0; i < 45; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const year = date.getFullYear();
      const fullDate = `${year}-${month}-${day}`;
      
      days.push({
        day: day,
        month: month,
        year: year,
        fullDate: fullDate,
        date: date
      });
    }
    return days;
  };

  const days = generateDays();

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value);
  };

  const getSignalColor = (type) => {
    return type === 'BUY' ? 'text-green-400' : 'text-red-400';
  };

  const getSignalBgColor = (type) => {
    return type === 'BUY' ? 'bg-green-900/30' : 'bg-red-900/30';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence > 0.8) return 'text-green-400';
    if (confidence > 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const handleDayClick = (day) => {
    setSelectedDate(day);
    setSelectedSignal(null);
  };

  // Obtener todas las señales del día seleccionado
  const getDaySignals = () => {
    if (!selectedDate || !monthlyData) return [];
    const dayData = monthlyData.days[selectedDate];
    return dayData ? dayData.signals : [];
  };

  const handleSignalClick = (signal) => {
    setSelectedSignal(signal);
    if (onSignalClick) {
      onSignalClick(signal);
    }
  };

  if (!monthlyData) {
    return (
      <div className="text-center py-12">
        <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-400 mb-4">Cargando calendario mensual...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header del Calendario */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white mb-2">
            Calendario de Trading - Próximos 45 Días
          </h1>
          <div className="flex justify-center space-x-8 text-sm text-gray-400">
            <div className="flex items-center">
              <TrendingUp className="w-4 h-4 text-green-400 mr-1" />
              <span>{monthlyData.total_buy} BUY</span>
            </div>
            <div className="flex items-center">
              <TrendingDown className="w-4 h-4 text-red-400 mr-1" />
              <span>{monthlyData.total_sell} SELL</span>
            </div>
            <div className="flex items-center">
              <Target className="w-4 h-4 text-yellow-400 mr-1" />
              <span>{monthlyData.total_signals} Total</span>
            </div>
          </div>
        </div>
      </div>

      {/* Calendario Mensual */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="grid grid-cols-7 gap-2">
          {/* Días de la semana */}
          {['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'].map((day) => (
            <div key={day} className="text-center p-2 text-gray-400 font-semibold text-sm">
              {day}
            </div>
          ))}

          {/* Días del mes */}
          {days.map((dayInfo) => {
            const dayData = monthlyData.days[dayInfo.day];
            const hasSignals = dayData && dayData.signals && dayData.signals.length > 0;
            const buySignals = hasSignals ? dayData.signals.filter(s => s.type === 'BUY') : [];
            const sellSignals = hasSignals ? dayData.signals.filter(s => s.type === 'SELL') : [];
            const isToday = dayInfo.fullDate === new Date().toISOString().split('T')[0];

            return (
              <div
                key={dayInfo.fullDate}
                className={`min-h-[120px] p-2 border border-gray-700 rounded-lg cursor-pointer transition-all hover:border-gray-600 ${
                  selectedDate === dayInfo.day ? 'ring-2 ring-yellow-400' : ''
                } ${hasSignals ? 'bg-gray-750' : 'bg-gray-800'} ${isToday ? 'ring-2 ring-blue-400' : ''}`}
                onClick={() => handleDayClick(dayInfo.day)}
              >
                {/* Número del día */}
                <div className="text-center mb-2">
                  <span className={`text-lg font-bold ${hasSignals ? 'text-white' : 'text-gray-500'} ${isToday ? 'text-blue-400' : ''}`}>
                    {dayInfo.day}
                  </span>
                  <div className="text-xs text-gray-400">
                    {dayInfo.month}/{dayInfo.year}
                  </div>
                </div>

                {/* Señales del día */}
                {hasSignals && (
                  <div className="space-y-1">
                    {/* Señales BUY */}
                    {buySignals.slice(0, 2).map((signal, index) => (
                      <div
                        key={`buy-${index}`}
                        className={`p-1 rounded text-xs cursor-pointer transition-all hover:scale-105 ${getSignalBgColor('BUY')} border border-green-600`}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleSignalClick(signal);
                        }}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-green-400">{signal.symbol}</span>
                          <span className="text-green-400">BUY</span>
                        </div>

                      </div>
                    ))}

                    {/* Señales SELL */}
                    {sellSignals.slice(0, 2).map((signal, index) => (
                      <div
                        key={`sell-${index}`}
                        className={`p-1 rounded text-xs cursor-pointer transition-all hover:scale-105 ${getSignalBgColor('SELL')} border border-red-600`}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleSignalClick(signal);
                        }}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-red-400">{signal.symbol}</span>
                          <span className="text-red-400">SELL</span>
                        </div>

                      </div>
                    ))}

                    {/* Contador de señales adicionales */}
                    {dayData.signals.length > 4 && (
                      <div className="text-center text-xs text-gray-400">
                        +{dayData.signals.length - 4} más
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Todas las señales del día seleccionado */}
      {selectedDate && (
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <Calendar className="w-5 h-5 mr-2 text-blue-400" />
            All Signals for Day {selectedDate}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {getDaySignals().map((signal, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border cursor-pointer transition-all hover:scale-105 ${
                  signal.type === 'BUY' 
                    ? 'bg-green-900/30 border-green-600' 
                    : 'bg-red-900/30 border-red-600'
                }`}
                onClick={() => handleSignalClick(signal)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-lg font-bold text-white">{signal.symbol}</span>
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    signal.type === 'BUY' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                  }`}>
                    {signal.type}
                  </span>
                </div>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Confidence:</span>
                    <span className={`font-bold ${getConfidenceColor(signal.confidence)}`}>
                      {(signal.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Source:</span>
                    <span className="text-blue-400 capitalize">{signal.source}</span>
                  </div>
                  {signal.reason && (
                    <div className="text-gray-300 text-xs mt-2">
                      {signal.reason.length > 50 ? signal.reason.substring(0, 50) + '...' : signal.reason}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
          {getDaySignals().length === 0 && (
            <div className="text-center py-8">
              <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-400">No signals for this day</p>
            </div>
          )}
        </div>
      )}

      {/* Detalles de la señal seleccionada */}
      {selectedSignal && (
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <Star className="w-5 h-5 mr-2 text-yellow-400" />
            Detalles de la Señal
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-2xl font-bold text-white">{selectedSignal.symbol}</span>
                <span className={`px-3 py-1 rounded text-sm font-bold ${
                  selectedSignal.type === 'BUY' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                }`}>
                  {selectedSignal.type}
                </span>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-400">Razón:</span>
                  <span className="text-white font-bold">{selectedSignal.reason || 'Análisis fundamental'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Confianza:</span>
                  <span className={`font-bold ${getConfidenceColor(selectedSignal.confidence)}`}>
                    {(selectedSignal.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Volumen:</span>
                  <span className="text-white">{selectedSignal.volume.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Fuente:</span>
                  <span className="text-blue-400 capitalize">{selectedSignal.source}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="text-lg font-bold text-white mb-3">Razón del Análisis</h4>
              <p className="text-gray-300 text-sm leading-relaxed">
                {selectedSignal.reason}
              </p>
              
              <div className="mt-4 p-3 bg-gray-700 rounded-lg">
                <h5 className="text-sm font-bold text-white mb-2">Resumen</h5>
                <div className="text-xs text-gray-400 space-y-1">
                  <div>• Símbolo: {selectedSignal.symbol}</div>
                  <div>• Tipo: {selectedSignal.type}</div>
                  <div>• Confianza: {(selectedSignal.confidence * 100).toFixed(0)}%</div>
                  <div>• Fuente: {selectedSignal.source === 'fundamental' ? 'Fundamental' : 'Técnico'}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Estadísticas del mes */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center">
          <Target className="w-5 h-5 mr-2 text-yellow-400" />
          Estadísticas del Mes
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{monthlyData.total_days}</div>
            <div className="text-gray-400 text-sm">Días con Señales</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">{monthlyData.total_buy}</div>
            <div className="text-gray-400 text-sm">Señales BUY</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-400">{monthlyData.total_sell}</div>
            <div className="text-gray-400 text-sm">Señales SELL</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">{monthlyData.total_signals}</div>
            <div className="text-gray-400 text-sm">Total Señales</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MonthlyCalendar;
